from celery import Celery
import cv2
import numpy as np
import msgpack
import msgpack_numpy as m

global window_handle 

app = Celery('tasks', broker='amqp://jet2:1990@10.0.0.20:5672/master')
# app = Celery('tasks', broker='amqp://jet1:1990@localhost:5672/master')

@app.task
def save(frame, frameNumber):
    frame = msgpack.unpackb(frame, object_hook=m.decode)
    cv2.imwrite("images/frame{}.jpg".format(frameNumber), frame)

@app.task
def initDisplay():
    global window_handle     
    window_handle = cv2.namedWindow("Camera Stream", cv2.WINDOW_AUTOSIZE)

@app.task
def killDisplay():
    cv2.destroyAllWindows()


@app.task
def displayFrame(frame, seconds):
    frame = np.asarray(frame)
    cv2.imshow("preview", frame)
    cv2.waitKey(1000*seconds)
    

#  (broker)
#  main.py ---| -- celeryTasks.py has all method calls to Celery. Depends on Celery, and some nparray image saving library that has DOES NOT require openCV
#             | -- csi_cam.py is camera class. Deps on OPENCV4.1.1

#  (worker)
#  celerTasks.py (copy)
