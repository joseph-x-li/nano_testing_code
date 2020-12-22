import cv2, zmq, time
import numpy as np
import multiprocessing as mp
from sys import getsizeof
from turbojpeg import TurboJPEG, TJSAMP_420, TJFLAG_FASTDCT, TJFLAG_FASTUPSAMPLE
from functools import partial

def send_ndarray(arr, socket):
    md = dict(
        dtype=str(arr.dtype),
        shape=arr.shape,
    )
    socket.send_json(md, zmq.SNDMORE|zmq.DONTWAIT)
    return socket.send(arr, copy=False)

def recv_ndarray(socket):
    md = socket.recv_json()
    msg = socket.recv(copy=False)
    buf = memoryview(msg)
    A = np.frombuffer(buf, dtype=md["dtype"])
    return A.reshape(md["shape"])

def named_ps(shutdown, name):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("ipc:///tmp/pipespeedtest")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    num = 0
    start = time.time()
    while not shutdown.is_set():
        if poller.poll(0):
            tmp = time.time()
            _ = recv_ndarray(socket)
            print(f"{name}, recv_time: {time.time() - tmp}")
            num += 1
            print(f"FPS: {num/(time.time() - start)}")

def test_pipe(rounds=100, n=2):
    for size in ["1920x1080", "1280x720", "640x480"]:
        img = cv2.imread(f"test_imgs/{size}.jpg")
        print(f"Testing image of shape {img.shape}, size {getsizeof(img)}")
        print(f"Testing uncompressed frame pipe speed...")
        input("Press enter to start")
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.bind("ipc:///tmp/pipespeedtest")
        shutdown = mp.Event()
        allps = [None] * n
        for i in range(n):
            ps = mp.Process(target=named_ps, args=(shutdown, str(i)))
            ps.daemon = True
            allps[i] = ps
        for ps in allps:
            ps.start()

        for i in range(rounds):
            tmp = time.time()
            send_ndarray(img, socket)
            print(f"SEND TIME: {time.time() - tmp}")
            time.sleep(0.01) # around 100 per second

        shutdown.set()
        for ps in allps:
            ps.join()

def test_enc(rounds=100):
    enc = partial(
        TurboJPEG().encode, quality=80, jpeg_subsample=TJSAMP_420, flags=TJFLAG_FASTDCT
    )
    for size in ["1920x1080", "1280x720", "640x480"]:
        img = cv2.imread(f"test_imgs/{size}.jpg")
        print(f"Testing image of shape {img.shape}, size {getsizeof(img)}")
        print(f"Testing compression speed...")
        input("Press enter to start")
        start = time.time()
        for i in range(rounds):
            buf = enc(img)
            if i % 5 == 0:
                print(f"FPS: {i/(time.time() - start)}")

def test_dec(rounds=100):
    enc = partial(
        TurboJPEG().encode, quality=80, jpeg_subsample=TJSAMP_420, flags=TJFLAG_FASTDCT
    )
    dec = partial(TurboJPEG().decode, flags=(TJFLAG_FASTDCT + TJFLAG_FASTUPSAMPLE))
    for size in ["1920x1080", "1280x720", "640x480"]:
        img = cv2.imread(f"test_imgs/{size}.jpg")
        buf = enc(img)
        print(f"Testing buffer of shape {len(buf)}, size {getsizeof(buf)}")
        print(f"Testing decompression speed...")
        input("Press enter to start")
        start = time.time()
        for i in range(rounds):
            img = dec(buf)
            if i % 5 == 0:
                print(f"FPS: {i/(time.time() - start)}")

def justpull(fromhere, shutdown):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(fromhere)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    start, idx = time.time(), 0
    while not shutdown.is_set():
        if poller.poll(0):
            buf = socket.recv()
            idx += 1
            print(f"FPS: {idx/(time.time() - start)}")

def test_pipe_buf(rounds=100):
    for size in ["1920x1080", "1280x720", "640x480"]:
        img = cv2.imread(f"test_imgs/{size}.jpg")
        print(f"Testing image of shape {img.shape}, size {getsizeof(img)}")
        print(f"Testing compressed buffer pipe speed...")
        input("Press enter to start")
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.bind("ipc:///tmp/pipespeedtest")
        shutdown = mp.Event()
        ps = mp.Process(target=justpull, args=("ipc:///tmp/pipespeedtest",shutdown))
        ps.daemon = True
        ps.start()
        enc = partial(
                TurboJPEG().encode, quality=80, jpeg_subsample=TJSAMP_420, flags=TJFLAG_FASTDCT
            )
        buf = enc(img)

        for i in range(rounds):
            socket.send(buf)

        time.sleep(1) # wait for processing
        shutdown.set()
        ps.join()
        
def pullonce(fromhere, shutdown):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.setsockopt(zmq.RCVHWM, 10)
    socket.connect(fromhere)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    while not shutdown.is_set():
        time.sleep(1)
        if poller.poll(0):
            buf = recv_ndarray(socket)
            print("RECEIVED")
            # break
        
    # print("Spinning...")
    # while not shutdown.is_set():
    #     time.sleep(0.1)

from itertools import count

def fillPUSH():
    img = cv2.imread(f"test_imgs/1920x1080.jpg")
    print(f"Testing HWM of PUSH socket...")
    input("Press enter to start")
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.setsockopt(zmq.SNDHWM, 10)
    socket.bind("ipc:///tmp/pushin")
    shutdown = mp.Event()
    ps = mp.Process(target=pullonce, args=("ipc:///tmp/pushin", shutdown))
    ps.daemon = True
    # ps.start()
    time.sleep(1) # wait for processing
    try:
        # for i in count():
        for i in range(18):
            send_ndarray(img, socket)
            time.sleep(0.1)
            print(f"\rSent {i} frames...", end="")
    except zmq.error.Again:
        print("AGAINED XDD")
        pass
    
    time.sleep(50)

    shutdown.set()
    ps.join()

if __name__ == "__main__":
    fillPUSH()