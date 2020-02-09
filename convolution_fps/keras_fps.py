import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D
import time
import numpy as np
from numpy import  array

model = Sequential()
bs=1   #batch size
xdim = 64
ydim = 64
kernel_len = 1 #1, 3, 5, 7
input_shape = (xdim, ydim, 3)
model.add(Conv2D(32, kernel_size=(kernel_len, kernel_len),
                 activation='relu',
                 input_shape=input_shape, bias_initializer='random_uniform'))
model.add(Conv2D(64, (kernel_len, kernel_len), activation='relu'))

n = 1000 #number of times we repeat the prediction
picture = np.random.randint(0, 255, size=(64, 64, 3))
picture = picture/255
frame = array([picture])
total_time = 0;
for i in range(n):
  start = time.time()
  hole = model.predict(x = frame, verbose=0)
  end = time.time()
  total_time += (end-start)
print("Number of frames: ", n)
print("Elapsed Time: ", total_time)
print("FPS: ", n/total_time)
