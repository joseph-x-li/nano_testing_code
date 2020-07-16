import ffmpeg

process = (
    ffmpeg
    .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30)
    .output('out.mp4', pix_fmt='yuv420p', frames=100)
)
process.run()
    

# ----- OUTLINE -----
# class Video S that uses context manager. 
# with videoStream as vs:
#     vs.add_client(x)
# 