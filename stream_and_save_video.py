# # For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# import cv2 as cv2
# import cv2 as cv
# import numpy as np
# import os
#
# FILE_OUTPUT = 'output.mp4'
#
# # Checks and deletes the output file
# # You cant have a existing file or it will through an error
# if os.path.isfile(FILE_OUTPUT):
#     os.remove(FILE_OUTPUT)
#
# # Playing video from file:
# # cap = cv2.VideoCapture('vtest.avi')
# # Capturing video from webcam:
# cap = cv2.VideoCapture(0)
#
# currentFrame = 0
#
#
# width = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 40);
# height  = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
#
#
# # Get current width of frame
# # width = cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH)   # float
# # Get current height of frame
# # height = cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT) # float
#
#
# # Define the codec and create VideoWriter object
# # fourcc = cv2.CV_FOURCC(*'X264')
#
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter(FILE_OUTPUT,fourcc, 20.0, (int(width),int(height)))
#
# # while(True):
# while(cap.isOpened()):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     if ret == True:
#         # Handles the mirroring of the current frame
#         frame = cv2.flip(frame,1)
#
#         # Saves for video
#         out.write(frame)
#
#         # Display the resulting frame
#         cv2.imshow('frame',frame)
#     else:
#         break
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#     # To stop duplicate images
#     currentFrame += 1
#
# # When everything done, release the capture
# cap.release()
# out.release()
# cv2.destroyAllWindows()


# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)
#
# # Define the codec and create VideoWriter object
# #fourcc = cv2.cv.CV_FOURCC(*'DIVX')
# #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
# out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
#
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     if ret==True:
#         frame = cv2.flip(frame,0)
#
#         # write the flipped frame
#         out.write(frame)
#
#         cv2.imshow('frame',frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# # Release everything if job is finished
# cap.release()
# out.release()
# cv2.destroyAllWindows()


import numpy as np
import os
import cv2


filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']



cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

while True:
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()