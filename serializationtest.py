import numpy as np
import time
import pickle
import json
import base64
import msgpack
import msgpack_numpy as m

fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size

# pickle
print("Now testing: pickle")
start = time.time()
pickle_enc = pickle.dumps(fakeFrame, protocol=0)
end = time.time()
pickle_enc_time = end-start
print("Encoding type: {}".format(type(pickle_enc)))

start = time.time()
pickle_dec = pickle.loads(pickle_enc)
end = time.time()
pickle_dec_time = end-start
print("Decoding type: {}".format(type(pickle_dec)))
print("Encoding time: {}\nDecoding time: {}".format(pickle_enc_time, pickle_dec_time)) 



# msgpack_numpy
print("Now testing: msgpack-numpy")
start = time.time()
msgpack_enc = msgpack.packb(fakeFrame, default=m.encode)
end = time.time()
print("Encoding type: {}".format(type(msgpack_enc)))
msgpack_enc_time = end-start

start = time.time()
msgpack_dec = msgpack.unpackb(msgpack_enc, object_hook=m.decode)
end = time.time()
msgpack_dec_time = end-start
print("Decoding type: {}".format(type(msgpack_dec)))
print("Encoding time: {}\nDecoding time: {}".format(msgpack_enc_time, msgpack_dec_time))



# JSON
print("Now testing: JSON")
start = time.time()
json_enc = json.dumps([str(fakeFrame.dtype), base64.b64encode(fakeFrame), fakeFrame.shape])
end = time.time()
print("Encoding type: {}".format(type(json_enc)))
json_enc_time = end-start

start = time.time()
# get the encoded json dump
enc = json.loads(json_enc)
# build the numpy data type
dataType = numpy.dtype(enc[0])
# decode the base64 encoded numpy array data and create a new numpy array with this data & type
dataArray = numpy.frombuffer(base64.decodestring(enc[1]), dataType)
# if the array had more than one data set it has to be reshaped
if len(enc) > 2:
     dataArray.reshape(enc[2])   # return the reshaped numpy array containing several data sets

end = time.time()
json_dec_time = end-start
print("Decoding type: {}".format(type(json_dec)))
print("Encoding time: {}\nDecoding time: {}".format(json_enc_time, json_dec_time))

