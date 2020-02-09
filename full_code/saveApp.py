from celery import Celery
import pickle as pkl
from tasks import add

app = Celery('tasks', broker='amqp://jet2:1990@localhost:5672/master')