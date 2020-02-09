import cv2
import time

print(cv2.__file__)

cap = cv2.VideoCapture()
if not (cap.isOpened()):
    print("could not open device")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

index = 0
start = time.time()

while(True):
    ret, frame = cap.read()
    print(index)
    index= index + 1
    cv2.imshow('preview', frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        end = time.time()
        print("Elapsed Time: ", end-start)
        print("FPS: ", index/(end-start))
        break

cap.release()
cv2.destroyAllWindows()
