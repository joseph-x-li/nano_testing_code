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

fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size

# tobytes
print("Now testing: tobytes")
start = time.time()
bytes_enc = fakeFrame.tobytes()
end = time.time()
bytes_enc_time = end-start
print("Encoding type: {}".format(type(bytes_enc)))

start = time.time()
bytes_dec = np.frombuffer(bytes_enc, dtype=np.int64).reshape((1920, 1080, 3))
end = time.time()
bytes_dec_time = end-start
print("Decoding type: {}".format(type(bytes_dec)))
print("Encoding time: {}\nDecoding time: {}".format(bytes_enc_time, bytes_dec_time)) 
assert (fakeFrame == bytes_dec).all()

fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size

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
assert (fakeFrame == msgpack_dec).all()

fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size

# tolist
print("Now testing: tolist")
start = time.time()
tolist_enc = fakeFrame.tolist()
end = time.time()
print("Encoding type: {}".format(type(tolist_enc)))
tolist_enc_time = end-start

start = time.time()
tolist_dec = np.asarray(tolist_enc)
end = time.time()
tolist_dec_time = end-start
print("Decoding type: {}".format(type(tolist_dec)))
print("Encoding time: {}\nDecoding time: {}".format(tolist_enc_time, tolist_dec_time))

# Now testing: pickle
# Encoding type: <class 'bytes'>
# Decoding type: <class 'numpy.ndarray'>
# Encoding time: 0.2712821960449219
# Decoding time: 0.6469271183013916
# Now testing: tobytes
# Encoding type: <class 'bytes'>
# Decoding type: <class 'numpy.ndarray'>
# Encoding time: 0.023937702178955078
# Decoding time: 3.695487976074219e-05
# Now testing: msgpack-numpy
# Encoding type: <class 'bytes'>
# Decoding type: <class 'numpy.ndarray'>
# Encoding time: 0.055579423904418945
# Decoding time: 0.02417755126953125
# Now testing: tolist
# Encoding type: <class 'list'>
# Decoding type: <class 'numpy.ndarray'>
# Encoding time: 2.7683544158935547
# Decoding time: 4.521432399749756