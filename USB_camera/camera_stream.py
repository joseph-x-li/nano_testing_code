import cv2
import time

print(cv2.__file__)
def send():
    cap_idx = input("Capture Device: ")
    cap = cv2.VideoCapture(int(cap_idx), cv2.CAP_AVFOUNDATION)
    if not (cap.isOpened()):
        print("could not open device")
        exit()

    gst_str_rtp = (
        'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000'
    )

    sink = cv2.VideoWriter(
        gst_str_rtp, int(cv2.CAP_GSTREAMER), 
        int(cv2.VideoWriter_fourcc(*"MPEG")),
        int(cap.get(cv2.CAP_PROP_FPS)),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
    )

    # print(f"OPENED?: {cv2.CAP_AVFOUNDATION}")
    # print(f"OPENED?: {cap.isOpened()}")
    # print(f"BACKEND: {cap.getBackendName()}")

    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    start = time.time()

    for _ in range(1000):
        ret, frame = cap.read()
        sink.write(frame)   
        # cv2.imshow('preview', frame)
        print("FPS: ", 1 / (time.time() - start))
        print(frame.shape)
        start = time.time()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    print(f"Capture Mode: {cap.get(cv2.CAP_PROP_MODE)}")
    print(f"WxH: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    # print(f"BACKEND: {cap.getBackendName()}")
    print(f"FOURCC: {cap.get(cv2.CAP_PROP_FOURCC)}")
    print(f"MAT FORMAT: {cap.get(cv2.CAP_PROP_FORMAT)}")
    print(f"RGB CONVERT?: {cap.get(cv2.CAP_PROP_CONVERT_RGB)}")

    cap.release()
    cv2.destroyAllWindows()


def receive():
    cap_receive = cv2.VideoCapture('udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

    if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)

    while True:
        ret,frame = cap_receive.read()

        if not ret:
            print('empty frame')
            break

        cv2.imshow('receive', frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

gst_str_rtp = (
    'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=172.16.0.49 port=5000'
)
out_send = cv2.VideoWriter(
    gst_str_rtp, cv2.CAP_GSTREAMER, 
    0,
    30,
    (1920, 1080),
)

time.sleep(1)

if not out_send.isOpened():
    print('VideoWriter not opened')
