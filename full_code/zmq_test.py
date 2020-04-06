import socket
import time
from imutils.video import VideoStream
import imagezmq
import csi_cam
import cv2

sender = imagezmq.ImageSender(connect_to='tcp://172.16.0.37:5555')

# JET1 = socket.gethostname() # send RPi hostname with each image
camera = csi_cam.csiCamera()
time.sleep(2.0)  # allow camera sensor to warm up

print("start")

numFrames = 5

for i in range(numFrames):
    print('mark:{}'.format(i))
    img = camera.getFrame()
    while img is None:
        img = camera.getFrame()
    sender.send_image(i, img)