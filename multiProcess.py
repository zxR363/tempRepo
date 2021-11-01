#!/usr/bin/python


import multiprocessing
from multiprocessing import Process, Queue
import os 
import threading
import time

x = -1
y = -1

q = Queue()


#---------------------THREADS------------------------------------

class autoPilotThread (threading.Thread):
	def __init__(self, threadID, name,values):
		 threading.Thread.__init__(self)
		 self.threadID = threadID
		 self.name = name
		 self.values = values
	def run(self):
		print("Starting => " + self.name)
		
		while True:
			 print("mmmmm.........")
			 time.sleep(1)
		
		print("Exiting => " + self.name)


class UpdateValuesThread (threading.Thread):
	def __init__(self, threadID, name,tempX,tempY):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.tempX = tempX  
		self.tempY = tempY
	def run(self):
		global x
		global y 

		if self.tempX != x or self.tempY != y:
			x = self.tempX
			y = self.tempY
			#hover moduna alinip yeni komut verilecek
			#Update autopilot goto function
			print("X=",x,"   Y=",y)
			x = -1
			y = -1
	
		time.sleep(1)

#-----------------------------------------------------------------


#---------------------PROCESSS------------------------------------

def autoPilotProcess(q):
	print("AutoPilot Process Started...")

	# Create new threads
	thread1 = autoPilotThread(1, "Thread1",q)


	# Start new Threads
	thread1.start()

	while True:
		if not q.empty():
			val1  = q.get()
			val2 = q.get()
			thread2 = UpdateValuesThread(2, "UpdateValues",val1,val2)
			thread2.start()

		else:
			print("Veri yok")
		time.sleep(1)

	
def imageProcess(q):
	print("Image Process Started...")
	while True:
		if q.empty() or q.qsize() < 3:
			q.put(1)
			q.put(2)
			print("Veriler EKLENDI...")
		else:
			print("Wrong Size")

		time.sleep(1)

 
#-------------------------------------------------------------------  

if __name__ == "__main__": 
	# printing main program process id 
	print("ID of main process: {}".format(os.getpid())) 
  
	#num = Value('d', 5.0)


	# creating processes 
	p1 = multiprocessing.Process(target=autoPilotProcess,args=(q,)) 
	p2 = multiprocessing.Process(target=imageProcess,args=(q,)) 
  
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