import csi_cam
import cv2
import time
from PIL import Image
import celery_tasks  
import numpy as np

camera = csi_cam.csiCamera()
img = camera.getFrame()
start_time = time.time()
numFrames = 30

for i in range(numFrames):
    img = camera.getFrame()
    while img is None:
        img = camera.getFrame()

end_time = time.time()

print(type(img))
print(img.shape)
print(img[1][1][1])
print(type(img[1][1][1]))
celery_tasks.save.delay(img.tolist(img), 1)
cv2.imwrite("images/frame{}.jpg".format(3), img)

print("FPS = ", (numFrames/(end_time-start_time)))
print(camera)

camera.stopCamera()


