#!/usr/bin/python


import multiprocessing
from multiprocessing import Process, Queue
import os 
import threading
import time

import socket
import os
from _thread import *
from enum import Enum


class PlayENUM(Enum):
	IDLE = 0
	STOP = 1
	JUMP = 2
	PLAY = 3



recordStopFlag = False
playStopFlag = PlayENUM.IDLE

q = Queue()
qPlayer = Queue()
qRecord = Queue()

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
windowSize = 1
durationForJump = 0

def manageMessage(q):
	reply = "P&-&0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"  # R -> RECORD , P -> PLAY
	return reply

def runAllSubMediaPlayer(value,path):
    cmd = "python 2_network_ile.py --host " + host + " --port " + str(port) + " --monitor " + str(value)+" --path "+path
    print("CommandAllSubMedia="+cmd)
    os.system(cmd)
    print("Process Killed")


def threaded_client(connection, playStopFlag1,sendingMessage,durationForJump):
	global playStopFlag
	connection.send(str.encode('Welcome to the Servern'))

	time.sleep(15)
	# data = connection.recv(2048)
	# reply = 'Server Says: ' + data.decode('utf-8')
	reply = "0&-&30000&-&C:\\Users\\yustuntepe\\Desktop\\123.mp4"  # ProcessId,ProcessValue,Path
	connection.sendall(str.encode(reply))

	while True:
		if playStopFlag == PlayENUM.STOP:
			print("STOP MESSAGE YAZILACAK ve TUM THREADLER DURDURULACAK")
			playStopFlag = PlayENUM.IDLE
			break
		elif playStopFlag == PlayENUM.JUMP:
			print("JUMP MESSAGE YAZILACAK")
			reply = sendingMessage
			connection.sendall(str.encode(reply))
			playStopFlag = PlayENUM.IDLE
			continue
		elif playStopFlag == PlayENUM.PLAY:
			print("PLAY MESSAGE YAZILACAK")
			reply = sendingMessage
			connection.sendall(str.encode(reply))
			playStopFlag = PlayENUM.IDLE
			continue

	connection.close()


#---------------------PROCESSS------------------------------------

def managePlaySide(q):
	global playStopFlag
	global ThreadCount
	global sendingMessage

	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waiting for a Connection..')
	ServerSocket.listen(5)
	playStopFlag = PlayENUM.IDLE

	while True:
		if not q.empty():
			tmpData  = q.get()
			data = tmpData.split("&-&")
			print("tmpData=",tmpData)
			if data[0] == "P" and playStopFlag.IDLE:
				customPathForSubMediPlayer = data[3].replace("\\", "/")

				for i in range(2, len(data), 1):
					sendingMessage = sendingMessage + data[i]  # ProcessId,ProcessValue

				for i in range(1, monitorSize, 1):
					start_new_thread(runAllSubMediaPlayer,(i, customPathForSubMediPlayer))  # Sending host,port,monitor,path

				while (ThreadCount != windowSize):
					client, address = ServerSocket.accept()
					print('Connected to: ' + address[0] + ':' + str(address[1]))
					start_new_thread(threaded_client,(client, playStopFlag, sendingMessage,durationForJump))  # Sending command for player process
					ThreadCount += 1
					print('Thread Number: ' + str(ThreadCount))

				print("PLAYED DONE")
				playStopFlag.PLAY

			elif data[0] == "P-S":
				print("CLOSE ")
				playStopFlag = PlayENUM.STOP

			elif data[0] == "J":
				playStopFlag = PlayENUM.JUMP

				for i in range(2, len(data), 1):
					sendingMessage = sendingMessage + data[i]  # ProcessId,ProcessValue

				print("JUMP")

			print("Closed Socket")

		else:
			a=5
			#print("Veri yok")

	print("Closed 1 side")
	ServerSocket.close()

def manageRecordSide(q):
	global playStopFlag

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
			print("val1=",val1)
			if rslt[0] == "P":
				#start_new_thread(playSideWorker,(rslt,ThreadCount,playStopFlag,q))
				print("TTTTTT")
			elif rslt[0] == "P-S":
				print("CCC111")
				#playStopFlag = True
		else:
			a=5
			#print("Veri yok")

	
def mainPcNetworkSide(qPlayer,qRecord):   #Mesaj yükleme tamamlandi ( MainPC den gelen komut üzerine yönetim yapıldı ve ilgili mesaj aktarildi )
	ClientSocket = socket.socket()

	print('Waiting for connection')
	try:
		ClientSocket.connect((mainPcHost, mainPcPort))
	except socket.error as e:
		print(str(e))

	#Response = ClientSocket.recv(1024)
	while True:
		Response = ClientSocket.recv(1024)
		msg = Response.decode('utf-8')
		if qPlayer.empty():
			qPlayer.put(msg)
			print("Veriler EKLENDI...=",msg)
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
	p1 = multiprocessing.Process(target=managePlaySide,args=(qPlayer,))
	p2 = multiprocessing.Process(target=mainPcNetworkSide,args=(qPlayer,qRecord))
  
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