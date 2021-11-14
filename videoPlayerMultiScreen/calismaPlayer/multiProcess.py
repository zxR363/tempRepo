#!/usr/bin/python


import multiprocessing
from multiprocessing import Process, Queue
import os 
import threading
import time
import numpy as np

import socket
import os
from _thread import *
from enum import IntEnum
from vidgear.gears import WriteGear

import cv2
import numpy as np
import pyautogui

from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
import atexit

from threading import Thread, Lock


class PlayENUM(IntEnum):
	IDLE = 0
	STOP = 1
	JUMP = 2
	PLAY = 3



recordStopFlag = False

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
monitorSize = 1
sendingMessage = ""
durationForJump = 0

playStopFlag = PlayENUM.IDLE
recordStopFlag = False


def runAllSubMediaPlayer(value,path):
    cmd = "python 2_network_ile.py --host " + host + " --port " + str(port) + " --path "+path
    print("CommandAllSubMedia="+cmd)
    os.system(cmd)
    print("Process Killed")


def threaded_client(connection, ThreadCount,durationForJump):
	global playStopFlag
	global sendingMessage
	connection.send(str.encode('Welcome to the Servern'))
	while True:
		if playStopFlag == PlayENUM.STOP:
			playStopFlag = PlayENUM.IDLE
			break
		elif playStopFlag == PlayENUM.JUMP:
			reply = sendingMessage
			connection.sendall(str.encode(reply))
			playStopFlag = PlayENUM.IDLE
			continue
		elif playStopFlag == PlayENUM.PLAY:
			reply = sendingMessage
			connection.sendall(str.encode(reply))

			playStopFlag = PlayENUM.IDLE
			continue
	connection.close()


#---------------------PROCESSS------------------------------------
def prepareSendingMessage(sendingMessage,data):
	sendingMessage = ""
	for i in range(1, len(data) - 1, 1):
		sendingMessage = sendingMessage + data[i] + "&-&"  # ProcessId,ProcessValue
	return sendingMessage


def managePlaySide(q):
	global ThreadCount
	global sendingMessage
	global playStopFlag

	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waiting for a Connection..')
	ServerSocket.listen(8)

	while True:
		if not q.empty():
			tmpData  = q.get()
			data = tmpData.split("&-&")
			print("tmpData=",tmpData)
			if data[0] == "P" and (playStopFlag == PlayENUM.IDLE):
				customPathForSubMediPlayer = data[3].replace("\\", "/")

				sendingMessage = prepareSendingMessage(sendingMessage,data)

				for i in range(0, monitorSize, 1):
					start_new_thread(runAllSubMediaPlayer,(1, customPathForSubMediPlayer))  # Sending host,port,monitor,path

				while (ThreadCount<monitorSize):
					client, address = ServerSocket.accept()
					print('Connected to: ' + address[0] + ':' + str(address[1]))
					start_new_thread(threaded_client,(client,ThreadCount, durationForJump))  # Sending command for player process
					ThreadCount += 1
					print('Thread Number: ' + str(ThreadCount))
					break

				playStopFlag = PlayENUM.PLAY

			elif data[0] == "P-S":  #CLOSE
				playStopFlag = PlayENUM.STOP

			elif data[0] == "J":   #JUMP
				sendingMessage = prepareSendingMessage(sendingMessage, data)
				playStopFlag = PlayENUM.JUMP

	print("PlaySide Socket Closed")
	ServerSocket.close()


#--------------------------------RECORD SIDE-----------------------------------------

def recordScreenFunction(path):
	global recordStopFlag

	img = pyautogui.screenshot()
	img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	# get info from img
	height, width, channels = img.shape

	# screenWidth = 3840
	# screenHeight = 1080

	pyautogui.onScreen(width, height)

	# define suitable (Codec,CRF,preset) FFmpeg parameters for writer
	output_params = {"-vcodec": "libx264", "-crf": 0, "-preset": "fast"}

	# Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
	writer = WriteGear(output_filename=path, logging=False,  # output_filename="test.mp4"
					   custom_ffmpeg="C:\\Users\\democh\\Downloads\\ffmpeg-4.2.1-win-64", **output_params)

	print("ACCC")
	# loop over
	while True:
		if recordStopFlag:
			print("END")
			break
		else:
			try:
				img = pyautogui.screenshot()
				image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
				# write gray frame to writer
				writer.write(image)
			except:
				break

	# close output window
	cv2.destroyAllWindows()

	# safely close writer
	writer.close()

def manageRecordSide(q2):
	global recordStopFlag
	path=""
	while True:
		if not q2.empty():
			tmpData = q2.get()
			data = tmpData.split("&-&")
			val = data[0].replace(" ", "")
			#process = multiprocessing.Process(target=recordScreenFunction, args=("test.mp4",recordStopFlag))
			#x = threading.Thread(target=recordScreenFunction, args=("test.mp4",))
			path = "test.mp4"
			if data[0] == "R":
				print("VAL=" + val)
				recordStopFlag=False
				start_new_thread(recordScreenFunction,(path,))
			elif data[0] == "R-S":
				recordStopFlag = True
	
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

		data = msg.split("&-&")
		val = data[0].replace(" ", "")
		print("DATA="+val)
		print("DATA=" , type(val))
		if val == "R" or val == "R-S":
			if qRecord.empty():
				qRecord.put(msg)
			else:
				print("Record Wrong Size")
		else:
			if qPlayer.empty():
				qPlayer.put(msg)
				print("Veriler EKLENDI...=",msg)
			else:
				print("Player Wrong Size")

		time.sleep(0.1)

	ClientSocket.close()

#-------------------------------------------------------------------  

if __name__ == "__main__": 
	# printing main program process id 
	print("ID of main process: {}".format(os.getpid()))

	# creating processes 
	p1 = multiprocessing.Process(target=managePlaySide,args=(qPlayer,))
	p2 = multiprocessing.Process(target=mainPcNetworkSide,args=(qPlayer,qRecord))
	p3 = multiprocessing.Process(target=manageRecordSide,args=(qRecord,))
  
	# starting processes 
	p1.start()
	p2.start()
	p3.start()

	# process IDs 
	print("ID of process p1: {}".format(p1.pid)) 
	print("ID of process p2: {}".format(p2.pid))
	print("ID of process p2: {}".format(p3.pid))

	# wait until processes are finished 
	p1.join()
	p2.join()
	p3.join()

	# both processes finished 
	print("Both processes finished execution!") 