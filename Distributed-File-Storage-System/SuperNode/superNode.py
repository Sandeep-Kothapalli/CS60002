import sys  
sys.path.append('./proto')
from concurrent import futures
from threading import Thread
import grpc
import yaml
    
import db
import fileService_pb2_grpc
import fileService_pb2
import time
import threading
import random
from ClusterStatus import ServerStatus


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

neighbors = {'172.16.45.132:3000' : '172.16.45.133:3000', '172.16.45.133:3000' : '172.16.45.134:3000', '172.16.45.134:3000' : '172.16.45.132:3000'}

#
#   *** FileServer Service : FileServer service as per fileService.proto file. ***
#   *** This class implements all the required methods to serve the user requests. *** 
#
class FileServer(fileService_pb2_grpc.FileserviceServicer):
    def __init__(self, hostIP, port):
        self.serverAddress = hostIP+":"+port
        self.clusterLeaders = {}
        self.serverStatus = ServerStatus()
        self.ip_channel_dict = {}

    #
    #   This service gets invoked when each cluster's leader informs the supernode
    #   about who the current cluster leader is
    #
    def getLeaderInfo(self, request, context):
        print("getLeaderInfo Called")
        address = request.ip + ":" + request.port
        self.clusterLeaders[request.clusterName] = address
        print("ClusterLeaders: ",self.clusterLeaders)
        channel = grpc.insecure_channel('{}'.format(address))
        self.ip_channel_dict[address] = channel
        return fileService_pb2.ack(success=True, message="Leader Updated.")

    #
    #   This service gets invoked when client uploads a new file.
    #
    def UploadFile(self, request, context):
        print("Inside Server method ---------- UploadFile")
        
        # Get the two clusters that have the most resources based on cluster stats
        # node, node_replica = self.clusterStatus.leastUtilizedNode(self.clusterLeaders)
        node = random.choice(list(neighbors.keys()))
        if self.serverStatus.isChannelAlive(node) == False:
            node = neighbors[node]
        
        node_replica = neighbors[node]
       
        # if(node==-1):
        #     return fileService_pb2.ack(success=False, message="No Active Clusters.")
        
        print("Node found is:{}, replica is:{}".format(node, node_replica))

        channel1 = self.serverStatus.isChannelAlive(node)
        stub1 = fileService_pb2_grpc.FileserviceStub(channel1)
        # if(node_replica!="" and node_replica in self.ip_channel_dict):
        channel2 = self.serverStatus.isChannelAlive(node_replica)
        stub2 = fileService_pb2_grpc.FileserviceStub(channel2)
        # else: stub2 = None
        
        # filename, username = "",""
        # data = bytes("",'utf-8')
        
        # for request in request_iterator:
        filename, username = request.filename, request.username
        data=request.data
            # break
        
        if(self.fileExists(username, filename)):
            return fileService_pb2.ack(success=False, message="File already exists for this user. Please rename or delete file first.")

        
        # def sendData(username, filename, data):
        #     yield fileService_pb2.FileData(username=username, filename=filename, data=data)
        #     for request in request_iterator:
        #         data+=request.data
        #         yield fileService_pb2.FileData(username=request.username, filename=request.filename, data=request.data)
        
        # resp1 = stub1.UploadFile(fileService_pb2.FileData(username=username, filename=filename, data=data))
        resp1 = stub1.UploadFile(request)
        
        # Replicate current file to alternate cluster
        if(stub2 is not None):
            t1 = Thread(target=self.replicateData, args=(stub2,username,filename,data,))
            t1.start()

        # save Meta Map of username+filename->clusterName that its stored on
        if(resp1.success):
            db.saveMetaData(username, filename, node, node_replica)
            db.saveUserFile(username, filename)
        
        return resp1


    #
    #   This service gets invoked when user requests an uploaded file.
    #
    def DownloadFile(self, request, context):

         # Check if file exists
        if(self.fileExists(request.username, request.filename)==False):
            return fileService_pb2.FileData(username=request.username, filename=request.filename, data=bytes("",'utf-8'), message="FNE")

        fileMeta = db.parseMetaData(request.username, request.filename)
        
        primaryIP, replicaIP = -1,-1
        channel1, channel2 = -1,-1
        # if(fileMeta[0] in self.clusterLeaders): 
        #     primaryIP = self.clusterLeaders[fileMeta[0]]
        #     channel1 = self.serverStatus.isChannelAlive(primaryIP)

        primaryIP = fileMeta[0]
        channel1 = self.serverStatus.isChannelAlive(primaryIP)
            
        # if(fileMeta[1] in self.clusterLeaders):
        #     replicaIP = self.clusterLeaders[fileMeta[1]]
        #     channel2 = self.serverStatus.isChannelAlive(replicaIP)

        replicaIP = fileMeta[1]
        channel2 = self.serverStatus.isChannelAlive(replicaIP)

        if(channel1):
            stub = fileService_pb2_grpc.FileserviceStub(channel1)
            # responses = stub.DownloadFile(fileService_pb2.FileInfo(username = request.username, filename = request.filename))
            
            response = stub.DownloadFile(fileService_pb2.FileInfo(username = request.username, filename = request.filename))
            # for response in responses:
            #     yield response

            return response
        elif(channel2):
            stub = fileService_pb2_grpc.FileserviceStub(channel2)
            # responses = stub.DownloadFile(fileService_pb2.FileInfo(username = request.username, filename = request.filename))

            response = stub.DownloadFile(fileService_pb2.FileInfo(username = request.username, filename = request.filename))
            # for response in responses:
            #     yield response

            return response
        else:
            return fileService_pb2.FileData(username=request.username, filename=request.filename, data=bytes("",'utf-8'), message="2F")

    #
    #   Function to check if file exists in db (redis)
    #  
    def fileExists(self,username, filename):
        return db.keyExists(username + "_" + filename)

    #
    #   Function that takes care of file replication on alternate cluster
    #  
    def replicateData(self,stub, username, filename, data):
        
        # def streamData(username, filename, data):
        #     chunk_size = 4000000
        #     start, end = 0, chunk_size
        #     while(True):
        #         chunk = data[start:end]
        #         if(len(chunk)==0): break
        #         start=end
        #         end += chunk_size
        #         yield fileService_pb2.FileData(username=username, filename=filename, data=chunk)

        req = fileService_pb2.FileData(username=username, filename=filename, data=data)
            
        resp = stub.UploadFile(req)


    #
    #   This services is invoked when user wants to delete a file
    #  
    def FileDelete(self, request, context):
        print("In FileDelete")

        if(self.fileExists(request.username, request.filename)==False):
            return fileService_pb2.ack(success=False, message="File {} does not exist for user {}.".format(request.filename, request.username))

        fileMeta = db.parseMetaData(request.username, request.filename)
        print("FileMeta = ", fileMeta)

        primaryIP, replicaIP = -1,-1
        channel1, channel2 = -1,-1
        # if(fileMeta[0] in self.clusterLeaders): 
        #     primaryIP = self.clusterLeaders[fileMeta[0]]
        #     channel1 = self.serverStatus.isChannelAlive(primaryIP)
        primaryIP = fileMeta[0]
        channel1 = self.serverStatus.isChannelAlive(primaryIP)
            
        # if(fileMeta[1] in self.clusterLeaders):
        #     replicaIP = self.clusterLeaders[fileMeta[1]]
        #     channel2 = self.serverStatus.isChannelAlive(replicaIP)
        replicaIP = fileMeta[1]
        channel2 = self.serverStatus.isChannelAlive(replicaIP)
        
        
        print("PrimaryIP={}, replicaIP={}".format(primaryIP,replicaIP))

        if(channel1):
            stub = fileService_pb2_grpc.FileserviceStub(channel1)
            response1 = stub.FileDelete(fileService_pb2.FileInfo(username = request.username, filename = request.filename))
        
        if(channel2):
            stub = fileService_pb2_grpc.FileserviceStub(channel2)
            response2 = stub.FileDelete(fileService_pb2.FileInfo(username = request.username, filename = request.filename))

        if(response1.success==True and response2.success == True):
            db.deleteEntry(request.username + "_" + request.filename)
            return fileService_pb2.ack(success=True, message="File successfully deleted from both primary and replica : ")
        else:
            if response1.success == False:
                return fileService_pb2.ack(success=False, message="Primary delete error")
            else:
                return fileService_pb2.ack(success=False, message="Replica delete error")
            
    #
    #   This services is invoked when user wants to check if a file exists
    #  
    def FileSearch(self, request, context):

        if(self.fileExists(request.username, request.filename)==False):
            return fileService_pb2.ack(success=False, message="File {} does not exist.".format(request.filename))

        fileMeta = db.parseMetaData(request.username, request.filename)

        primaryIP, replicaIP = -1,-1
        channel1, channel2 = -1,-1

        if(fileMeta[0] in self.clusterLeaders): 
            primaryIP = self.clusterLeaders[fileMeta[0]]
            channel1 = self.serverStatus.isChannelAlive(primaryIP)
            
        if(fileMeta[1] in self.clusterLeaders):
            replicaIP = self.clusterLeaders[fileMeta[1]]
            channel2 = self.serverStatus.isChannelAlive(replicaIP)

        if(channel1 != -1):
            stub = fileService_pb2_grpc.FileserviceStub(channel1)
            response = stub.FileSearch(fileService_pb2.FileInfo(username = request.username, filename = request.filename))

        if(channel2 != -1):
            stub = fileService_pb2_grpc.FileserviceStub(channel2)
            response = stub.FileSearch(fileService_pb2.FileInfo(username = request.username, filename = request.filename))
        
        if(response.success==True):
            return fileService_pb2.ack(success=True, message="File exists! ")
        else:
            return fileService_pb2.ack(success=False, message="File does not exist in any cluster.")

    #
    #   This services lists all files under a user
    #  
    def FileList(self, request, context):
        userFiles = db.getUserFiles(request.username)
        return fileService_pb2.FileListResponse(Filenames=str(userFiles))


def run_server(hostIP, port):
    print('Supernode started on {}:{}'.format(hostIP, port))

    #GRPC 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fileService_pb2_grpc.add_FileserviceServicer_to_server(FileServer(hostIP, port), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

# ----------------------Main-------------------- #
if __name__ == '__main__':
    config_dict_orig = yaml.load(open('config.yaml'))
    super_node_address = config_dict_orig['super_node_address']

    server_desc = super_node_address.split(":")
    hostIP =server_desc[0]
    port = server_desc[1]
    run_server(hostIP, port)
