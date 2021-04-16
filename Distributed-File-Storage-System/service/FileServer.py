from concurrent import futures

from threading import Thread
import os
import grpc
import sys

sys.path.append("../generated")
sys.path.append("../utils")
sys.path.append("../proto")
import db
import fileService_pb2_grpc
import fileService_pb2
import heartbeat_pb2_grpc
import heartbeat_pb2
import time
import yaml
import threading
import hashlib
from ShardingHandler import ShardingHandler
from lru import LRU

UPLOAD_SHARD_SIZE = 50 * 1024 * 1024

#
#   *** FileServer Service : FileServer service as per fileService.proto file. ***
#   *** This class implements all the required methods to serve the user requests. ***
#
class FileServer(fileService_pb2_grpc.FileserviceServicer):
    def __init__(
        self,
        hostname,
        server_port,
        activeNodesChecker,
        shardingHandler,
        superNodeAddress,
    ):
        self.serverPort = server_port
        self.serverAddress = hostname + ":" + server_port
        self.activeNodesChecker = activeNodesChecker
        self.shardingHandler = shardingHandler
        self.hostname = hostname
        self.lru = LRU(3)
        self.superNodeAddress = superNodeAddress

    #
    #   This service gets invoked when user uploads a new file.
    #
    def UploadFile(self, request, context):
        print("Inside Server method ---------- UploadFile")

        username, filename = "", ""

        print("Saving the data on my local db")

        dataToBeSaved = bytes("", "utf-8")

        username, filename = request.username, request.filename
        dataToBeSaved += request.data
        key = username + "_" + filename

        if(self.lru.has_key("cache_" + key) and self.lru["cache_" + key] == "valid"):
            self.lru["cache_" + key] = "invalid"

        # Save the data in redis
        # db.setData(key, dataToBeSaved)

        # save data in a file
        if not os.path.exists(username):
            os.makedirs(username)

        with open(username + "/" + filename, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(dataToBeSaved)

        return fileService_pb2.ack(success=True, message="Saved")

    def DownloadFile(self, request, context):

        print("Inside server method - download file")

        username, filename = request.username, request.filename
        key = username + "_" + filename
        cache_key = "cache_" + key
        # print(key)

        if(self.lru.has_key(cache_key) and self.lru[cache_key] == "valid"):
            print("Fetching data from Cache")

            data_cache = db.getFileData(cache_key)

            return fileService_pb2.FileData(username = request.username, filename = request.filename, data=data_cache, message="success from cache" )

        
        # data = db.getFileData(key)
        data_return = bytes("", "utf-8")
        with open(username + "/" + filename, "rb") as binary_file:
            # Write bytes to file
            data_return = binary_file.read()

        self.saveInCache(request.username, request.filename, data_return)

        return fileService_pb2.FileData(
            username=request.username,
            filename=request.filename,
            data=data_return,
            message="success",
        )

    # This service is responsible fetching all the files.
    def FileList(self, request, context):
        print("File List Called")
        userFiles = db.getUserFiles(request.username)
        return fileService_pb2.FileListResponse(Filenames=str(userFiles))

    # This helper method checks whether the file is present in db or not.
    def fileExists(self, username, filename):
        print("isFile Present", db.keyExists(username + "_" + filename))
        return db.keyExists(username + "_" + filename)

    # This helper method returns 2 least loaded nodes in cluster.

    # def getLeastLoadedNode(self):
    #     print("Ready to enter sharding handler")
    #     node, node_replica = self.shardingHandler.leastUtilizedNode()
    #     print("Least loaded node is :", node)
    #     print("Replica node - ", node_replica)
    #     return node, node_replica

    # This helper method checks whethere created channel is alive or not
    def isChannelAlive(self, channel):
        try:
            grpc.channel_ready_future(channel).result(timeout=1)
        except grpc.FutureTimeoutError:
            # print("Connection timeout. Unable to connect to port ")
            return False
        return True

    # This helper method is responsible for updating the cache for faster lookup.
    def saveInCache(self, username, filename, data):
        
        if(len(self.lru.items())>=self.lru.get_size()):
            file_key, path = self.lru.peek_last_item()
            if (path == "valid"):
                db.deleteEntry(file_key)

        cache_key = "cache_" + username + "_" + filename
        self.lru[cache_key]="valid"
        db.setCacheData(cache_key, data)


    # This service is responsible for sending the whole cluster stats to superNode
    # def getClusterStats(self, request, context):
    #     print("Inside getClusterStats")
    #     active_ip_channel_dict = self.activeNodesChecker.getActiveChannels()
    #     total_cpu_usage, total_disk_space, total_used_mem = 0.0, 0.0, 0.0
    #     total_nodes = 0
    #     for ip, channel in active_ip_channel_dict.items():
    #         if self.isChannelAlive(channel):
    #             stub = heartbeat_pb2_grpc.HearBeatStub(channel)
    #             stats = stub.isAlive(heartbeat_pb2.NodeInfo(ip="", port=""))
    #             total_cpu_usage = float(stats.cpu_usage)
    #             total_disk_space = float(stats.disk_space)
    #             total_used_mem = float(stats.used_mem)
    #             total_nodes += 1

    #     if total_nodes == 0:
    #         return fileService_pb2.ClusterStats(
    #             cpu_usage=str(100.00),
    #             disk_space=str(100.00),
    #             used_mem=str(100.00),
    #         )

    #     return fileService_pb2.ClusterStats(
    #         cpu_usage=str(total_cpu_usage / total_nodes),
    #         disk_space=str(total_disk_space / total_nodes),
    #         used_mem=str(total_used_mem / total_nodes),
    #     )

    # This service is responsible for sending the leader info to superNode as soon as leader changes.

    def getLeaderInfo(self, request, context):
        channel = grpc.insecure_channel("{}".format(self.superNodeAddress))
        stub = fileService_pb2_grpc.FileserviceStub(channel)
        response = stub.getLeaderInfo(
            fileService_pb2.ClusterInfo(
                ip=self.hostname, port=self.serverPort, clusterName="team1"
            )
        )
        print(response.message)

    #   This service gets invoked when user deletes a file.
    def FileDelete(self, request, data):
        username = request.username
        filename = request.filename
        print("Deleting file : " + filename)
        key = username + "_" + filename

        if(self.lru.has_key("cache_" + key)):
            self.lru["cache_" + key] = "invalid"
            db.deleteEntry("cache_" + key)

        #delete file from redis
        # db.deleteEntry(key)

        if os.path.exists(username + "/" + filename):
            os.remove(username + "/" + filename)
        print("Deleted File")

        return fileService_pb2.ack(
            success=True, message="Successfully deleted file from the cluster"
        )