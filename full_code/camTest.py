import csi_cam
import cv2

camera = csi_cam.csiCamera()
img = camera.getFrame()

while img is None:
    img = camera.getFrame()

print(type(img))
print(img.shape)
cv2.imwrite("frame.jpg", img)
camera.stopCamera()

