import socket
import os
from _thread import *
import os
import time


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 6789
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
        time.sleep(15)
        #data = connection.recv(2048)
        #reply = 'Server Says: ' + data.decode('utf-8')
        reply = "0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"
        connection.sendall(str.encode(reply))
        time.sleep(1000000)
    connection.close()

def runAllSubMediaPlayer(value):
    cmd = "python 2_network_ile.py --host " + host + " --port " + str(port) + " --monitor " + str(value)+" --path "+path
    os.system(cmd)
    print("process Killed")

def tempRun():
    cmd = "python 2_network_ile.py --host " + host + " --port " + str(port) + " --monitor " + str(1) + " --path " + path
    os.system(cmd)

for i in range(1,monitorSize,1):
    start_new_thread(runAllSubMediaPlayer,(i,))

start_new_thread(tempRun,())



while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()