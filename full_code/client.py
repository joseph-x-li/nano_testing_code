import socket
import time

HEADERSIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(
    ("172.16.0.38", 11234)
)

for counter in range(40):
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(100)
        if new_msg:
            print(f"New Message Length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False 
        
        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("Done Receiving")
            finalAnswer = np.frombuffer(full_msg[HEADERSIZE:], dtype=np.int64).reshape((1920, 1080, 3))
            new_msg = True
            full_msg = b''