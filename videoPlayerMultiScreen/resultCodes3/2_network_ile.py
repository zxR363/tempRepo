import platform
import os
import sys
import socket
import threading
import time
import multiprocessing
from multiprocessing import Process, Queue
import argparse


import vlc
from PyQt5.QtWidgets import QFrame, QDesktopWidget
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal

host = "127.0.0.1"
port = 6789

rslt = []

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)

    ClientSocket = socket.socket()

    def run(self):
        try:
            self.ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
            self.finished.emit()

        Response = self.ClientSocket.recv(1024)
        while True:
            #Input = input('Say Something2: ')
            #self.ClientSocket.send(str.encode(Input))
            #self.ClientSocket.send(str.encode("Lets TRY"))
            rsp = self.ClientSocket.recv(1024)
            #print(Response.decode('utf-8'))
            response = rsp.decode('utf-8')
            rslt = response.split("&-&")
            print("response=",response)
            self.progress.emit(rslt)

        ClientSocket.close()
        self.finished.emit()


class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self,filename,duration,host,port):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Media Player")
        self.showFullScreen()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent;")
        self.setContentsMargins(0, 0, 0, 0)

        self.count =0
        self.duration = duration
        self.maxDuration = 0

        # Network
        self.host = host # '127.0.0.1'
        self.port = port # 6789
        self.filename = filename
        self.runLongTask()

        # Create a basic vlc instance
        self.instance = vlc.Instance()
        self.media = None
        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        #self.create_ui(filename)

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.chooseProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        """
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )
        """

    def chooseProgress(self,listData):

        progressId    = listData[0]
        progressValue = listData[1]

        if progressId == "0": # Start Play
            self.create_ui(self.filename)
        if progressId == "1": # Jump Specific Time
            self.jumpSpecificTime(progressValue)
        elif progressId == "2":
            self.closeAllProcess()

    def create_ui(self,filename):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.setContentsMargins(0,0,0,0)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.widget.setLayout(self.vboxlayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_ui)
        self.open_file(filename)


    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return
            self.mediaplayer.play()

            time.sleep(0.1)
            # getting the duration of the video
            self.maxDuration = self.mediaplayer.get_length()
            print("Max Duration=",self.maxDuration)

            self.mediaplayer.set_time(self.duration)
            self.timer.start()

    def jumpSpecificTime(self, duration):
        if int(duration) > 0 and int(duration) <= self.maxDuration:
            self.mediaplayer.set_time(int(duration))
        else:
            print("WRONG DURATION !!!!!!!!")

    def stop(self):
        """Stop player"""
        self.timer.stop()
        self.mediaplayer.stop()
        #self.closeEvent()

    def open_file(self,filename):
        """Open a media file in a MediaPlayer"""
        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename)

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        #self.setWindowTitle(self.media.get_meta(0))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def set_volume(self, volume):
        """Set the volume"""
        self.mediaplayer.audio_set_volume(volume)

    def update_ui(self):  #periyodic function
        """Updates the user interface"""

        self.count = self.count + 1

        if self.count == 10:          #Init player Time => After 100 ms ,all scenes start from 0
            self.jumpSpecificTime(self.duration)  #Sync for All scenes
        if self.count == 500:
            print("")
            #self.jumpSpecificTime(125000)
            #self.timer.stop() For stop timer
        if self.count == 1000:
            print("")
            #self.jumpSpecificTime(10000)
        if self.count == 1500:
            print("k")
            #self.closeAllProcess()   # All process are closed

    def closeEvent(self, event):
        event.accept()
    def closeAllProcess(self):
        print("All process DONE!!!!")
        sys.exit()

def createVideoPlayer(monitorNumber,filename,duration,host,port):
    app = QtWidgets.QApplication(sys.argv)
    player = Player(filename,duration,host,port)
    # player.show()

    widget = player  # define your widget
    display_monitor = monitorNumber - 1  # the number of the monitor you want to display your widget

    monitor = QDesktopWidget().screenGeometry(display_monitor)
    widget.move(monitor.left(), monitor.top())
    widget.showFullScreen()
    sys.exit(app.exec_())

def main(host,port,monitorNumber,path):
    createVideoPlayer(monitorNumber,path,0,host,port)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Information')
    parser.add_argument('--host', dest='host', type=str, help='IP')
    parser.add_argument('--port', dest='port', type=int, help='PORT')
    parser.add_argument('--monitor', dest='monitor', type=int, help='MONITOR NUMBER')
    parser.add_argument('--path', dest='path',type=str, help="Video Path")

    args = parser.parse_args()
    print(args.host)
    print(args.port)
    print(args.monitor)
    print(args.path)

    time.sleep(0.2)
    main(args.host,args.port,args.monitor,args.path)
