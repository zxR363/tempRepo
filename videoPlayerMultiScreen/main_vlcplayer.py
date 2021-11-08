# importing vlc module
import vlc

# importing time module
import time

# creating vlc media player object
#vlc.Instance("--directx-device={,display,\\.\DISPLAY2} ")



media_player = vlc.MediaPlayer()

# media object
media = vlc.Media("C:\\Users\\democh\\PycharmProjects\\video\\Output.mp4")

#media_player.set_xwindow(1)
#print(media_player.get_xwindow())

# setting media to the media player
media_player.set_media(media)
media_player.set_fullscreen(True)
media_player.audio_set_volume(0)
media_player.set_video_title_display(2,10000)


# start playing video
media_player.play()

#jump specific time
media_player.set_time(30000)

time.sleep(0.1)
# getting the duration of the video
duration = media_player.get_length()
print("FPS=",media_player.get_fps())

# printing the duration of the video
print("Duration : " + str(duration))

# wait so the video can be played for 5 seconds
# irrespective for length of video
time.sleep((duration/1000))

media_player.stop()





