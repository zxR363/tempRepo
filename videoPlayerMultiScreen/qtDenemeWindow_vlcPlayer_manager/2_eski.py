import platform
import os
import sys

import multiprocessing
from multiprocessing import Process, Queue


import vlc
from PyQt5.QtWidgets import QFrame, QDesktopWidget
from PyQt5 import QtWidgets, QtGui, QtCore

class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self,filename,duration):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Media Player")
        self.showFullScreen()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent;")
        self.setContentsMargins(0, 0, 0, 0)

        self.count =0
        self.duration = duration

        # Create a basic vlc instance
        self.instance = vlc.Instance()
        self.media = None
        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.create_ui(filename)



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
            print("LENGTH = ",self.mediaplayer.get_length())
            self.mediaplayer.set_time(self.duration)
            self.timer.start()

    def jumpSpecificTime(self, duration):
        self.mediaplayer.set_time(duration)

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
            self.jumpSpecificTime(125000)
            #self.timer.stop() For stop timer
        if self.count == 1000:
            self.jumpSpecificTime(10000)
        if self.count == 1500:
            self.closeAllProcess()   # All process are closed

    def closeEvent(self, event):
        event.accept()
    def closeAllProcess(self):
        sys.exit()

def createVideoPlayer(monitorNumber,filename,duration):
    app = QtWidgets.QApplication(sys.argv)
    player = Player(filename,duration)
    # player.show()

    widget = player  # define your widget
    display_monitor = monitorNumber - 1  # the number of the monitor you want to display your widget

    monitor = QDesktopWidget().screenGeometry(display_monitor)
    widget.move(monitor.left(), monitor.top())
    widget.showFullScreen()
    sys.exit(app.exec_())

def main():
    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))

    # num = Value('d', 5.0)

    # creating processes
    #C:\\Users\\democh\\Desktop\\2.mp4"
    p1 = multiprocessing.Process(target=createVideoPlayer, args=(1, "C:\\Users\\democh\\PycharmProjects\\video\\Output.mp4",0,))
    p2 = multiprocessing.Process(target=createVideoPlayer, args=(2, "C:\\Users\\democh\\PycharmProjects\\video\\Output2.mp4",0,))

    # starting processes
    p1.start()
    p2.start()


    # process IDs
    print("ID of process p1: {}".format(p1.pid))
    print("ID of process p2: {}".format(p2.pid))

    # wait until processes are finished
    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
