import ffmpeg

process = (
    ffmpeg
    .input('FaceTime', format='avfoundation', pix_fmt='uyvy422', framerate=30)
    .output('out.mp4', pix_fmt='yuv420p', frames=100)
)
process.run()

# ----- OUTLINE -----
# class that uses context manager. 
# with videoStream as vs:
#     vs.add_client(x)



# import ffmpeg_streaming`


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
