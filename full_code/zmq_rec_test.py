import cv2
import imagezmq
image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    frame_num, image = image_hub.recv_image()
    if image is not None:
        print("{}".format(frame_num ))
        cv2.imwrite("images/frame{}.jpg".format(frame_num), image)
        image_hub.send_reply(b'OK')