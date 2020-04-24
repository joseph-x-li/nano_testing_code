import socket
import numpy as np

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(("172.16.0.38", 11234))


while True:
    fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size
    msg = fakeFrame.tobytes()
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    s.sendto(msg, ("172.16.0.37", 11234))