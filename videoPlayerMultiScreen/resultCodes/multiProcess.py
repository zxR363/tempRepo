#!/usr/bin/python


import multiprocessing
from multiprocessing import Process, Queue
import os 
import threading
import time

import socket
import os
from _thread import *

recordStopFlag = False
playStopFlag = False

q = Queue()

mainPcHost = '127.0.0.2'
mainPcPort = 6900

#------------------------------------------ MANAGE RECORD AND PLAY SIDE SERVER ----------------------------------

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 6789
ThreadCount = 0
monitorSize = 2
path = "C:\\Users\\\yustuntepe\\Desktop\\abc.mp4"
path2 = "C:\\Users\\\yustuntepe\\Desktop\\123.mp4"
sendingMessage = ""

def manageMessage(q):
	reply = "P&-&0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"  # R -> RECORD , P -> PLAY
	return reply

def runAllSubMediaPlayer(value,path):
    cmd = "python 2_network_ile.py --host " + host + " --port " + str(port) + " --monitor " + str(value)+" --path "+path
    print("CommandAllSubMedia="+cmd)
    os.system(cmd)
    print("Process Killed")


def threaded_client(connection, playStopFlag,manageMessage):
	connection.send(str.encode('Welcome to the Servern'))
	while True:
		if playStopFlag == True:
			break
		time.sleep(15)
		# data = connection.recv(2048)
		# reply = 'Server Says: ' + data.decode('utf-8')
		reply = "0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"  # ProcessId,ProcessValue,Path
		connection.sendall(str.encode(reply))
		time.sleep(1000000)
	connection.close()

def playSideWorker(data,ThreadCount,playStopFlag):
	global sendingMessage
	global ServerSocket
	#customPathForSubMediPlayer = data[1]
	customPathForSubMediPlayer = data[3].replace("\\", "/")
	print("data3=",customPathForSubMediPlayer)
	print("PlaySideData=",data)
	for i in range(2,len(data),1):
		sendingMessage = sendingMessage + data[i]  #ProcessId,ProcessValue

	for i in range(1, monitorSize, 1):
		start_new_thread(runAllSubMediaPlayer, (i,customPathForSubMediPlayer))   #Sending host,port,monitor,path

	while True:
		client, address = ServerSocket.accept()
		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(threaded_client, (client,playStopFlag,sendingMessage))    #Sending command for player process
		ThreadCount += 1
		print('Thread Number: ' + str(ThreadCount))

	ServerSocket.close()

#---------------------PROCESSS------------------------------------

def manageRecordAndPlaySide(q):
	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waiting for a Connection..')
	ServerSocket.listen(5)

	while True:
		if not q.empty():
			val1  = q.get()
			rslt = val1.split("&-&")
			if rslt[0] == "P":
				playSideWorker(rslt,ThreadCount,playStopFlag)
				print("")
			elif rslt[1] == "P-S":
				playFlag = True

		else:
			a=5
			#print("Veri yok")

	
def mainPcNetworkSide(q):   #Mesaj yükleme tamamlandi ( MainPC den gelen komut üzerine yönetim yapıldı ve ilgili mesaj aktarildi )
	ClientSocket = socket.socket()

	print('Waiting for connection')
	try:
		ClientSocket.connect((mainPcHost, mainPcPort))
	except socket.error as e:
		print(str(e))

	Response = ClientSocket.recv(1024)
	while True:
		# Input = input('Say Something2: ')
		# ClientSocket.send(str.encode(Input))
		Response = ClientSocket.recv(1024)
		msg = Response.decode('utf-8')
		msg = manageMessage(msg)
		if q.empty():
			q.put(msg)
			print("Veriler EKLENDI...")
		else:
			print("Wrong Size")

		time.sleep(0.1)

	ClientSocket.close()

#-------------------------------------------------------------------  

if __name__ == "__main__": 
	# printing main program process id 
	print("ID of main process: {}".format(os.getpid())) 

	#num = Value('d', 5.0)


	# creating processes 
	p1 = multiprocessing.Process(target=manageRecordAndPlaySide,args=(q,))
	p2 = multiprocessing.Process(target=mainPcNetworkSide,args=(q,))
  
	# starting processes 
	p1.start() 
	p2.start() 
  
	# process IDs 
	print("ID of process p1: {}".format(p1.pid)) 
	print("ID of process p2: {}".format(p2.pid)) 
  
	# wait until processes are finished 
	p1.join() 
	p2.join() 
  
	# both processes finished 
	print("Both processes finished execution!") 