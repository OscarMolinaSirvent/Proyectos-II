import time
import math
from multiprocessing import Process

COUNT = 200000000
def countdown(n):
    while n>0:
        n -= 1
        a = math.sqrt(n)
        
if __name__ == "__main__":
    p1 = Process(target=countdown, args=(COUNT/2,))
    p2 = Process(target=countdown, args=(COUNT/2,))
    start = time.time()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print('Time taken in seconds -', end - start)