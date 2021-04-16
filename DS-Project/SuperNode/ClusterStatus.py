from concurrent import futures
import grpc
import sys
import db
sys.path.append('./proto')
import fileService_pb2_grpc
import fileService_pb2
import time
import threading

class ServerStatus():

    def isChannelAlive(self, ip_address):
        #print("In isChannelAlive")
        try:
            channel = grpc.insecure_channel('{}'.format(ip_address))
            grpc.channel_ready_future(channel).result(timeout=1)
        except grpc.FutureTimeoutError:
            return False
        return channel