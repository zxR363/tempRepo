import os
import sys
import socket
import argparse
# import required libraries
from vidgear.gears import WriteGear

import cv2
import numpy as np
import pyautogui

from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
import atexit

def exit_handler():
    print("Application is ending!")

#Custom FFMPEG Binary => https://ffbinaries.com/downloads

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Information')
    parser.add_argument('--path', dest='path',type=str, help="Video Path")

    args = parser.parse_args()

    atexit.register(exit_handler)

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
    writer = WriteGear(output_filename=args.path, logging=False,  #output_filename="test.mp4"
                       custom_ffmpeg="C:\\Users\\democh\\Downloads\\ffmpeg-4.2.1-win-64", **output_params)

    # loop over
    while True:
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