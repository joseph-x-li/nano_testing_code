import cv2
from multiprocessing import Process
import os
import time

def send():
    cap_send = cv2.VideoCapture(int(0), cv2.CAP_AVFOUNDATION)
    # gst_str_rtp = "appsrc ! videoconvert ! video/x-raw,format=YUY2 ! jpegenc ! rtpjpegpay ! udpsink host=172.0.0.1 port=9000"
    # out_send = cv2.VideoWriter(gst_str_rtp, cv2.CAP_GSTREAMER, 0 , 10, (640, 480), True)
    gst_str_rtp = (
        'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=172.16.0.49 port=5000'
    )
    out_send = cv2.VideoWriter(
        gst_str_rtp, cv2.CAP_GSTREAMER, 
        cv2.VideoWriter_fourcc(*"H264"),
        cap_send.get(cv2.CAP_PROP_FPS),
        (int(cap_send.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap_send.get(cv2.CAP_PROP_FRAME_HEIGHT))),
    )

    if not cap_send.isOpened():
        print('VideoCapture not opened')
        exit(0)
    
    if not out_send.isOpened():
        print('VideoWriter not opened')
        exit(0)
        

    while True:
        ret,frame = cap_send.read()

        if not ret:
            print('empty frame')
            break

        out_send.write(frame)

        cv2.imshow('send', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

    cap_send.release()
    out_send.release()

def receive():
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"
    cap_receive = cv2.VideoCapture("video.sdp")
    if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)
    
    end = time.time()
    for _ in range(1000):
        ret,frame = cap_receive.read()
        print(frame.shape)
        if not ret:
            print('empty frame')
            break
        
        print(f"FPS: {1/(time.time()-end)}")
        end = time.time()
        # cv2.imshow('receive', frame)
        # if cv2.waitKey(1)&0xFF == ord('q'):
        #     break

    #cap_receive.release()

if __name__ == '__main__':
    # s = Process(target=send)
    r = Process(target=receive)
    # s.start()
    r.start()
    # s.join()
    r.join()

    cv2.destroyAllWindows()