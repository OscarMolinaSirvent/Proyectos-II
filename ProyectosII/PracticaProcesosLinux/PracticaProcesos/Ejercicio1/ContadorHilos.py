#ejemplo de como se ejecuta una función sobre 2 hilos
#simula repartir el trabajo de cálculo entre dos hilos. En un sistema
#multicore "normal", esto implicaría duplicar la productivdad
import time
import math
from threading import Thread

COUNT = 200000000
def countdown(n):
    while n>0:
        n -= 1
        a = math.sqrt(n)

t1 = Thread(target=countdown, args=(COUNT/2,))
t2 = Thread(target=countdown, args=(COUNT/2,))
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print('Time taken in seconds -', end - start)