# Implementation of CSI camera as a Class.
# 


import cv2
import time
from threading import Thread

def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

class csiCamera:
    def __init__(self, width = 1920, height = 1080, framerate = 30, display = False, flip = 2):
        self.display = display
        self.width = width
        self.height = height
        self.framerate = framerate
        self.flip = flip

        self.pipeline = gstreamer_pipeline(
            capture_width = width,
            capture_height = height,
            display_width = width,
            display_height = height,
            framerate = framerate,
            flip_method = flip)
        self.cap = None
        self.capture_thread = None
        self.hasFrame = False
        self.nextFrame = None
        self.killThread = False
        self.startCamera()

    def __eq__(self, other):
        return (other != None and self.display == other.display and
                self.width == other.width and self.flip == other.flip and self.framerate==other.framerate)
    
    def __repr__(self):
        return "Height: {}\nWidth: {}\nDisplay? {}\nFramerate: {}\nFlip: {}".format(self.height, self.width, self.display, self.framerate, self.flip)

    def __del__(self):
        self.stopCamera()

    def frameDaemon(self):
        if self.cap.isOpened:
            if self.display:
                window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
            while True:
                if (not self.cap.isOpened) or self.killThread:
                    break
                ret_val, self.nextFrame = self.cap.read()
                self.hasFrame = True
                if self.display:
                    cv2.imshow("CSI Camera", self.nextFrame)
                    
                keyCode = cv2.waitKey(30) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
        else:
            print("Unable to open camera")
            return 0
        #thread kill behavior
        self.cap.release()
        cv2.destroyAllWindows()
        return 0
    
    def getFrame(self):
        if self.hasFrame:
            self.hasFrame = False
            return self.nextFrame
        else:
            return None
    
    def startCamera(self):
        self.cap = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)
        self.capture_thread = Thread(target=self.frameDaemon, args=(), daemon = True)
        self.capture_thread.start()
        print("Camera Warming Up...")
        time.sleep(2) #wait 3 seconds for camera to boot up I guess
        print("Camera On")

    def stopCamera(self):
        self.killThread = True
        time.sleep(3)

    #functions you probably dont need
    def frameReady(self):
        return self.hasFrame
    