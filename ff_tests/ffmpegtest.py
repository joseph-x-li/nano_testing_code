import av
import time
import numpy as np
import platform
import cv2

input_dev = input("INPUT DEVICE: ")

framerate = "30.000030"
resolution = "1920x1080"
optn = {"resolution": resolution, "framerate": framerate}  #
optinal = {"input_format": "h264"}
optn.update(optinal)

conversion = {"Linux": "v4l2", "Darwin": "avfoundation", "Windows": "dshow"}
sys = platform.system()


first = True
with av.open(file="rtp://127.0.0.1:5003", mode="w", format="rtp", options={"sdp_file":"video.sdp"}) as stream:
    sink = stream.add_stream("rtp", rate=framerate)
    with av.open(file=input_dev, format=conversion[sys], options=optn) as camera:
        print(f"open type: {type(camera)}")
        end = 0
        for frame in camera.decode():
            dump = frame.to_image()
            dump2 = np.array(dump)
            stream.mux(sink.encode(av.VideoFrame.from_ndarray(dump2)))
            print(f"Size: {dump2.shape}")
            if first:
                dump.save("hi.png")
                first = False
                dump.show()
            # cv2.imshow("asdf", dump)
            print(f"HIT {dump.size}, fps = {1/(time.time() - end)}")
            end = time.time()
        time.sleep(1)


# LINUX
# ffmpeg -flags low_delay
# -f v4l2 -input_format h264 -video_size 1920x1080 -framerate 30 -i /dev/video1
# -c copy -f rtp -sdp_file video.sdp 'rtp://239.2.4.1:5004?ttl=3'

# MAC
# ffmpeg -f avfoundation -framerate 30 -video_size 1920x1080 -i 1 out.mpeg
# ffmpeg -f avfoundation -framerate 30 -video_size 1280x720 -i 1 out.mkv
