import socket
import os
from _thread import *
import os
import time


ServerSocket = socket.socket()
host = '127.0.0.2'
port = 6900
ThreadCount = 0
monitorSize = 2
path = "C:\\Users\\\yustuntepe\\Desktop\\abc.mp4"
path2 = "C:\\Users\\\yustuntepe\\Desktop\\123.mp4"

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        p = input("message=")
        if p == "s":
            reply = "P&-&0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"   #ProcessId,ProcessValue,Path
            connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()