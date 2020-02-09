from celery import Celery
import pickle as pkl
# import csi_cam
import time

# cam = csi_cam.csiCamera(display = False)
app = Celery('tasks', broker='amqp://jet1:1990@localhost:5672/master')

@app.task
def add(x, y):
    return x + y

# image = asdf.getFrame()
# index = 0

# while image is None:
#     image = asdf.getFrame()
#     time.sleep(0.1)
#     index += 1
#     # print(index)

# print(index)
# print(image)
# asdf.stopCamera()

# print("starting camera again lol")

# asdf.startCamera()
# image = None
# index = 0

# while image is None:
#     image = asdf.getFrame()
#     time.sleep(0.1)
#     index += 1
#     # print(index)

# print(index)
# print(image)
# asdf.stopCamera()

# for i in range(10):
#     print("shit")