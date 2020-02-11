from celery import Celery
from tasks import add

app = Celery('tasks', broker='amqp://jet2:1990@localhost:5672/master')

@app.task
def save(frame, frameNumber):
    

#  (broker)
#  main.py ---| -- celeryTasks.py has all method calls to Celery. Depends on Celery, and some nparray image saving library that has DOES NOT require openCV
#             | -- csi_cam.py is camera class. Deps on OPENCV4.1.1

#  (worker)
#  celerTasks.py (copy)