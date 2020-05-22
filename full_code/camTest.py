# Takes one photo and uses celery to save it

import csi_cam
import cv2
import time
from PIL import Image
import celery_tasks  
import numpy as np
import msgpack
import msgpack_numpy as m

camera = csi_cam.csiCamera()

# START
start_time = time.time()
numFrames = 5

for i in range(numFrames):
    img = camera.getFrame()
    while img is None:
        img = camera.getFrame()
    celery_tasks.save.delay(msgpack.packb(img, default=m.encode), i)
    print("frame: {}".format(i))

end_time = time.time()
# END

# RETROSPECTIVE
print(type(img))
print(img.shape)
print(img[1][1][1])
print(type(img[1][1][1]))
cv2.imwrite("images/frame{}.jpg".format(3), img)

print("FPS = ", (numFrames/(end_time-start_time)))
print(camera)

camera.stopCamera()


