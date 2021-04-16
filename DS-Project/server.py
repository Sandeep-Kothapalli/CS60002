from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

from threading import Thread
import grpc
import sys
sys.path.append('./utils')
sys.path.append('./service')
sys.path.append('./proto')
import db
import fileService_pb2_grpc
import fileService_pb2
import time
import yaml
import threading
import hashlib
from FileServer import FileServer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# Start the server.
def run_server(hostname, server_port, raft_port, super_node_address):


    # Declare the gRPC server with 10 max_workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add FileService to the server.
    # fileService_pb2_grpc.add_FileserviceServicer_to_server(FileServer(hostname, server_port, activeNodesChecker, shardingHandler, super_node_address), server)
    fileService_pb2_grpc.add_FileserviceServicer_to_server(FileServer(hostname, server_port, super_node_address), server)

    # Start the server on server_port.
    server.add_insecure_port('[::]:{}'.format(server_port))
    server.start()
    print(f"server started at {hostname}. super node can communicate.")

    # Keep the server running for '_ONE_DAY_IN_SECONDS' seconds.
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

# ----------------------Main Method-------------------- #
if __name__ == '__main__':
    # Read the configuration from 'config.yaml'
    config_dict_orig = yaml.load(open('config.yaml'))
    if(len(sys.argv)<2):
        print("Usage python3 server.py <<server No>>")
        print("Enter one, two or three for server No.")
        exit()
    config_dict = config_dict_orig[str(sys.argv[1]).lower()]
    server_host = config_dict['hostname']
    server_port = str(config_dict['server_port'])
    raft_port = str(config_dict['raft_port'])
    super_node_address = config_dict_orig['super_node_address']

    db.setData("primaryStatus", 0)

    # Start the server
    run_server(server_host, server_port, raft_port, super_node_address)
