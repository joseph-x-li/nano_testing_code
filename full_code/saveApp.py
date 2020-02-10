from celery import Celery
import pickle as pkl
from tasks import add

app = Celery('tasks', broker='amqp://jet2:1990@localhost:5672/master')


#  (broker)
#  main.py ---| -- celeryTasks.py has all method calls to Celery. Depends on Celery, and some nparray image saving library that has DOES NOT require openCV
#             | -- csi_cam.py is camera class. Deps on OPENCV4.1.1

#  (worker)
#  celerTasks.py (copy)