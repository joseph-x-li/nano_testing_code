import csi_cam
import cv2
import time
from PIL import Image
import celery_tasks  

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
celery_tasks.save.delay(img.tostring(), 1)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
GGAM = Image.fromarray(img)
GGAM.save("images/frame{}.jpeg".format(3))

print("FPS = ", (numFrames/(end_time-start_time)))
print(camera)

camera.stopCamera()


