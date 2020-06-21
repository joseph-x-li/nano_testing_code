import insightface
import urllib
import urllib.request
import cv2
import numpy as np


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


url = "https://github.com/deepinsight/insightface/blob/master/sample-images/t1.jpg?raw=true"
img = url_to_image(url)


model = insightface.model_zoo.get_model("retinaface_r50_v1")

model.prepare(ctx_id=-1, nms=0.4)

bbox, landmark = model.detect(img, threshold=0.5, scale=1.0)


print(bbox, landmark)
