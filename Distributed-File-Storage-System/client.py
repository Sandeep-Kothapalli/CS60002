import sys

sys.path.append("./generated")
sys.path.append("./proto")
sys.path.append("./utils")

import grpc
import fileService_pb2_grpc
import fileService_pb2
import sys
import time
import yaml
import os
import random

INPUT_DIR = "files"
DOWNLOAD_DIR = "downloads"


def getFileData():
    username = input("Enter Username: ")
    fileName = input("Enter filename: ")
    sTime = time.time()

    outfile = os.path.join(INPUT_DIR, fileName)
    file_data = open(outfile, "rb").read()
    fileData = fileService_pb2.FileData(
        username=username, filename=fileName, data=file_data
    )

    print("Time for upload= ", time.time() - sTime)
    return fileData


def downloadTheFile(stub):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    data = bytes("", "utf-8")
    sTime = time.time()
    response = stub.DownloadFile(
        fileService_pb2.FileInfo(username=userName, filename=fileName)
    )

    if response.message == "FNE":
        print(
            "Error : File {} not found for user {}".format(fileName, userName)
        )
        return

    elif response.message == "2F":
        print("Two nodes down : data could not be retrieved")
        return

    fileName = response.filename
    data += response.data

    print("Time for Download = ", time.time() - sTime)
    filePath = os.path.join(DOWNLOAD_DIR, fileName)
    saveFile = open(filePath, "wb")
    saveFile.write(data)
    saveFile.close()

    print("File Downloaded - ", fileName)


def uploadTheFile(stub):
    response = stub.UploadFile(getFileData())
    if response.success:
        print("File successfully Uploaded")
    else:
        print("Failed to upload. Message - ", response.message)


def deleteTheFile(stub):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    response = stub.FileDelete(
        fileService_pb2.FileInfo(username=userName, filename=fileName)
    )
    print(response.message)


def listFiles(stub):
    userName = input("Enter Username: ")
    FileListResponse = stub.FileList(
        fileService_pb2.UserInfo(username=userName)
    )
    print(FileListResponse.Filenames)


def handleUserInputs(stub):
    while True:
        print("\n-----------------------------------")
        print("1. Upload a file")
        print("2. Download a file.")
        print("3. Delete a file")
        print("4. Get a list of all the files for an user")
        print("5. Exit")
        print("-----------------------------------")
        option = input("Please choose an option.")

        if option == "1":
            uploadTheFile(stub)
        elif option == "2":
            downloadTheFile(stub)
        elif option == "3":
            deleteTheFile(stub)
        elif option == "4":
            listFiles(stub)
        elif option == "5":
            break


def run_client(serverAddress):
    with grpc.insecure_channel(serverAddress) as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=1)
        except grpc.FutureTimeoutError:
            print("Connection timeout. Unable to connect to port ")
        else:
            print("Connected")
        stub = fileService_pb2_grpc.FileserviceStub(channel)
        handleUserInputs(stub)


if __name__ == "__main__":
    # server_addresses = ['18.224.22.150', '3.21.159.167']
    server_addresses = ["172.16.45.131:50051"]
    run_client(random.choice(server_addresses))
