import sys

sys.path.append("./proto")
from concurrent import futures
from threading import Thread
import grpc
import yaml

import db
import fileService_pb2_grpc
import fileService_pb2
import time
import random
from ClusterStatus import ServerStatus

random.seed(time.time())


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

with open("../iptable.txt") as iptable:
    ip1 = iptable.readline()
    ip2 = iptable.readline()
    ip3 = iptable.readline()

neighbors = {ip1: ip2, ip2: ip3, ip3: ip1}

#   FileServer Service : FileServer service as per fileService.proto file.
class FileServer(fileService_pb2_grpc.FileserviceServicer):
    def __init__(self, hostIP, port):
        self.serverAddress = hostIP + ":" + port
        self.clusterLeaders = {}
        self.serverStatus = ServerStatus()
        self.ip_channel_dict = {}

        # consistency after recovery
        self.message_queue = {ip1: [], ip2: [], ip3: []}

        self.ip1_delete_consi_thread = Thread(
            target=self.deleteInconsistentFile, args=(ip1,)
        )

        self.ip1_delete_consi_thread.start()

        self.ip2_delete_consi_thread = Thread(
            target=self.deleteInconsistentFile, args=(ip2,)
        )

        self.ip2_delete_consi_thread.start()

        self.ip3_delete_consi_thread = Thread(
            target=self.deleteInconsistentFile, args=(ip3,)
        )

        self.ip3_delete_consi_thread.start()

    def deleteInconsistentFile(self, ipaddress):
        while True:
            time.sleep(0.5)
            channel = self.serverStatus.isChannelAlive(ipaddress)

            if channel:
                stub = fileService_pb2_grpc.FileserviceStub(channel)
                if len(self.message_queue[ipaddress]) > 0:
                    print(
                        "Deleting Stale Data : " + ipaddress + " after Recovery"
                    )
                    message = self.message_queue[ipaddress].pop(0)
                    stub.FileDelete(message)
                    

    # check if file metadata is in redis
    def fileExists(self, username, filename):
        return db.keyExists(username + "_" + filename)

    #   This service gets invoked when client uploads a new file.
    def UploadFile(self, request, context):
        print("In UploadFile method")

        # choose active 2 storage nodes from 3
        node = random.choice(list(neighbors.keys()))
        if self.serverStatus.isChannelAlive(node) == False:
            node = neighbors[node]

        node_replica = neighbors[node]
        if self.serverStatus.isChannelAlive(node_replica) == False:
            node_replica = neighbors[node_replica]

        print(
            "primary node is:{}, replica node is:{}".format(node, node_replica)
        )

        channel1 = self.serverStatus.isChannelAlive(node)
        stub1 = fileService_pb2_grpc.FileserviceStub(channel1)

        channel2 = self.serverStatus.isChannelAlive(node_replica)
        stub2 = fileService_pb2_grpc.FileserviceStub(channel2)

        filename, username, data = (
            request.filename,
            request.username,
            request.data,
        )

        # preventing the upload of duplicate files
        if self.fileExists(username, filename):
            return fileService_pb2.ack(
                success=False,
                message="File already exists for this user. Please rename or delete file first.",
            )

        # sending to storage servers
        resp1 = stub1.UploadFile(request)

        # new thread for replication
        t1 = Thread(
            target=self.replicateData,
            args=(
                stub2,
                username,
                filename,
                data,
            ),
        )
        t1.start()

        # save metadata in redis if success
        if resp1.success:
            db.saveMetaData(username, filename, node, node_replica)
            db.saveUserFile(username, filename)

        return resp1

    #   This service gets invoked when user wants to download
    def DownloadFile(self, request, context):
    	print("Downloading File : " + request.filename)
        # Check if file exists
        if self.fileExists(request.username, request.filename) == False:
        	return fileService_pb2.FileData(
                username=request.username,
                filename=request.filename,
                data=bytes("", "utf-8"),
                message="FNE",
            )


        metadata_file = db.parseMetaData(request.username, request.filename)

        channel1 = self.serverStatus.isChannelAlive(metadata_file[0])
        channel2 = self.serverStatus.isChannelAlive(metadata_file[1])

        if channel1:
            stub = fileService_pb2_grpc.FileserviceStub(channel1)
            response = stub.DownloadFile(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )
            return response
        elif channel2:
            stub = fileService_pb2_grpc.FileserviceStub(channel2)
            response = stub.DownloadFile(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )
            return response
        else:
            return fileService_pb2.FileData(
                username=request.username,
                filename=request.filename,
                data=bytes("", "utf-8"),
                message="2F",
            )

    #   Function that takes care of file replication on replica
    def replicateData(self, stub, username, filename, data):

        req = fileService_pb2.FileData(
            username=username, filename=filename, data=data
        )
        stub.UploadFile(req)

    #   This service is invoked when user wants to delete a file
    def FileDelete(self, request, context):
        print("in server method FileDelete")

        if self.fileExists(request.username, request.filename) == False:
            return fileService_pb2.ack(
                success=False,
                message="File {} does not exist for user {}.".format(
                    request.filename, request.username
                ),
            )

        fileMeta = db.parseMetaData(request.username, request.filename)
        print("FileMeta = ", fileMeta)

        primaryIP = fileMeta[0]
        channel1 = self.serverStatus.isChannelAlive(primaryIP)

        replicaIP = fileMeta[1]
        channel2 = self.serverStatus.isChannelAlive(replicaIP)

        print("PrimaryIP={}, replicaIP={}".format(primaryIP, replicaIP))

        if channel1:
            stub = fileService_pb2_grpc.FileserviceStub(channel1)
            response1 = stub.FileDelete(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )
        else:
            self.message_queue[primaryIP].append(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )

        if channel2:
            stub = fileService_pb2_grpc.FileserviceStub(channel2)
            response2 = stub.FileDelete(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )
        else:
            self.message_queue[replicaIP].append(
                fileService_pb2.FileInfo(
                    username=request.username, filename=request.filename
                )
            )
        #delete file metadata in super node
        #file is not accessible anymore
        db.deleteEntry(request.username + "_" + request.filename)

        if (
            channel1
            and response1.success == True
            and channel2
            and response2.success == True
        ):
            return fileService_pb2.ack(
                success=True,
                message="File successfully deleted from both primary and replica : ",
            )
        else:
            if not channel1:
                if not channel2:
                    return fileService_pb2.ack(
                    success=False, message="Primary and replica both Servers Down"
                )
                return fileService_pb2.ack(
                    success=False, message="Primary Server Down"
                )
            elif response1.success == False:
                return fileService_pb2.ack(
                    success=False, message="Primary Delete Failed"
                )
            elif not channel2:
                return fileService_pb2.ack(
                    success=False, message="Replica Server Down"
                )
            else:
                return fileService_pb2.ack(
                    success=False, message="Replica Delete Failed"
                )
    #   This service is invoked when user wants to list all files
    def FileList(self, request, context):
    	print("Fetching File list for User : " + request.username)
    	userFiles = db.getUserFiles(request.username)
    	return fileService_pb2.FileListResponse(Filenames=str(userFiles))


def run_server(hostIP, port):
    print("Supernode started on {}:{}".format(hostIP, port))

    # GRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fileService_pb2_grpc.add_FileserviceServicer_to_server(
        FileServer(hostIP, port), server
    )
    # listen from all ips
    server.add_insecure_port("[::]:{}".format(port))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


# ----------------------Main-------------------- #
if __name__ == "__main__":
    config_dict_orig = yaml.load(open("../config.yaml"))
    super_node_address = config_dict_orig["super_node_address"]

    server_desc = super_node_address.split(":")
    hostIP = server_desc[0]
    port = server_desc[1]
    run_server(hostIP, port)
