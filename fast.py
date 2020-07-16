import multiprocessing
import time
import random

a = 1
def outer():
    a = 5
    def inner():
        def three():
            nonlocal a
            a += 1
            print(a)

        three()
        print(a)
        
    inner()
    print(a)

print(a)
            


# def spawn(num):
#   x = random.random()
#   time.sleep(x)
#   print(num, x)

# if __name__ == '__main__':
#   start = time.time()
#   x = [multiprocessing.Process(target=spawn, args=(i,)) for i in range (25)]
#   end = time.time()
#   for p in x:
#     p.start()
#   print("INITS: ", end - start)