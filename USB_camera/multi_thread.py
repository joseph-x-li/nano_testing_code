import cv2
import time
from threading import Thread

class VideoStream:
    def __init__(self, src=0, width=1920, height=1080, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.stream = cv2.VideoCapture(src)
        self.stream.set(CV_CAP_PROP_FRAME_WIDTH = self.width)
        self.stream.set(CV_CAP_PROP_FRAME_HEIGHT = self.height)
        self.stream.set(CV_CAP_PROP_FRAME_FPS = self.fps)
        self.ret, self.img = self.stream.read()
        
        self.left_thread = True
        capture_thread = Thread(target=self.update_img, args=())
        capture_thread.daemon = True

        capture_thread.start()
    def grab_image(self):    
    def update_img_1(self):
        while True:
            if self.stream.isOpened():
                self.ret, self.img = self.stream.read()
                print("hi")
            time.sleep(0.01)

    def get_frames(self, frameno):
        img = self.img
        cv2.imwrite("frame%d.jpg" % frameno, img)

if __name__ == "__main__":
    camera = VideoStream()
    frames = 100
    start_time = time.time()
    for i in range(frames):
        camera.get_frames(i)

    end_time = time.time()
    print("FPS: ")
    print(frames/(end_time-start_time))



