import socket
import time
import numpy as np

HEADERSIZE = 20


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(
    ("172.16.0.38", 11238)
)


full_msg = b''
new_msg = True
print("MARKK")
start = time.time()
while True:
    msg = s.recv(10_000_000)
    if new_msg:
        print(f"New Message Length: {msg[:HEADERSIZE]}")
        msglen = int(msg[:HEADERSIZE])
        new_msg = False 
    print("mark")
    full_msg += msg
    # print(len(full_msg))
    if len(full_msg) - HEADERSIZE == msglen:
        end = time.time()
        print(f"FPS = {1/(end - start)}")
        print("Done Receiving")
        # finalAnswer = np.frombuffer(full_msg[HEADERSIZE:], dtype=np.int64).reshape((1920, 1080, 3))
        print(f"DONE w/ len: {len(full_msg)}")
        new_msg = True
        full_msg = b''
        break
