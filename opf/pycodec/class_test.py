from mpjpeg import UltraJPGEnc, UltraJPGDec
from pystreaming.listlib.circularlist import CircularList
import cv2
import zmq, asyncio
import threading as th

def frame_server(shutdown, bufqueue):
    

def run_server(port=5555, frames=1000):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
    bank = UltraJPGEnc()
    bank.start_workers()
    for i in range(frames):
        ret, frame = cap.read()
        bank.tell(frame)
        if i < 4: # allow workers to get full
            continue
        buf, idx = bank.hear()


async def aio_rr(context, source="172.16.0.25:5555"):
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{source}")
    print("Started a frame request async thread")
    while True:
        await socket.send(b"plz")
        buf = await socket.recv()
        idx = await socket.recv_pyobj()

async def aio_rr_main():
    context = zmq.asyncio.Context()
    await asyncio.gather(aio_rr(context),aio_rr(context),aio_rr(context),aio_rr(context))