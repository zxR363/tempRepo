# import required libraries
from vidgear.gears import ScreenGear
from vidgear.gears import WriteGear
from vidgear.gears import helper
import cv2

#Custom FFMPEG Binary => https://ffbinaries.com/downloads

# define dimensions of screen w.r.t to given monitor to be captured
options = {"top": 0, "left": 0, "width": 1920, "height": 1080}

# define suitable (Codec,CRF,preset) FFmpeg parameters for writer
output_params = {"-vcodec": "libx264", "-crf": 0, "-preset": "fast"}

# open video stream with defined parameters
stream = ScreenGear(monitor=1, logging=True, **options).start()
stream2 = ScreenGear(monitor=2, logging=True, **options).start()

# Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
writer = WriteGear(output_filename="Output.mp4", logging=False,custom_ffmpeg="D:\\ffmpeg-4.2.1-win-64", **output_params)
writer2 = WriteGear(output_filename="Output2.mp4", logging=False,custom_ffmpeg="D:\\ffmpeg-4.2.1-win-64", **output_params)

# loop over
while True:

    # read frames from stream
    frame = stream.read()
    frame2 = stream2.read()

    # check for frame if Nonetype
    if frame is None:
        break
    if frame2 is None:
        break

    # {do something with the frame here}
    # lets convert frame to gray for this example
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # write gray frame to writer
    writer.write(gray)
    writer2.write(gray2)

    cv2.imshow("aa",gray)
    # Show output window
    #cv2.imshow("Output Gray Frame", gray)
    #cv2.imshow("Output Gray Frame2", gray2)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()
stream2.stop()

# safely close writer
writer.close()
writer2.close()
print("DONE")