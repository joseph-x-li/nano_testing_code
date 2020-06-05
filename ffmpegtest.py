import ffmpeg

(
    ffmpeg.input(
        "FaceTime",
        format="avfoundation",
        pix_fmt="uyvy422",
        options={"framerate": "30", "video_size": "640x480"},
    )
    .output("out.mp4", pix_fmt="yuv420p", vframes=100)
    .run()
)

# import ffmpeg_streaming


# capture = ffmpeg_streaming.input('FaceTime', capture=True)


# def func4(a, b, c):
#     retval = c
#     retval -= b
#     hold = retval
#     retval = -1 if retval < 0 else 0
#     retval += hold
#     retval //= 2
#     hold = retval + b
#     if(hold <= a):
#         if(hold >= a):
#             return hold
#         else:
#             b = hold+1
#             retval = func4(a, b, c)
#             retval += hold
#             return retval
#     c = hold-1
#     retval = func4(a, b, c)
#     retval += hold
#     return retval

# def main():
#     for i in range(36):
#         print(f"{i}: {func4(i, 0, 14)}")

# if __name__ == "__main__":
#     main()
