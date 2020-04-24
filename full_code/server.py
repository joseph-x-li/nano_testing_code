import socket
import numpy as np

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(
    (socket.gethostname(), 11234)
)

s.listen(5)

while True:
    cluentsocket, address = s.accept()
    print(f"Connection from {address} is established")
    fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size
    msg = fakeFrame.tobytes()
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
    clientsocket.send(msg)