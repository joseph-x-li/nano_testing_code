import socket
import numpy as np
import cv2

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
JET1 = ("172.16.0.38", 11238)
s.bind(
    JET1
)

s.listen(5)
# fakeFrame = np.random.randint(255, size=(1920, 1080, 3)) # make a fake image of proper size
# fakeFrame = np.zeros(shape = (1920, 1080, 3))
# is_success, im_buf_arr = cv2.imencode(".jpeg", fakeFrame)

with open("./images/frame0.jpg", "rb") as image:
  f = image.read()
  b = bytearray(f)

# msg = im_buf_arr.tobytes()
msg = b
msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} is established!")
    # with open('./images/frame0.jpg', 'rb') as f:
    #     clientsocket.sendfile(f, 0)
    # clientsocket.close()
    clientsocket.sendall(msg)