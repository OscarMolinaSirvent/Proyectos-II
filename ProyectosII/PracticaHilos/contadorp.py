#ejemplo de como se ejecuta una función sobre un único hilo
import time
import math
#from threading import Thread

COUNT = 200000000
def countdown(n):
    while n>0:
        n -= 1
        a = math.sqrt(n)

start = time.time()
countdown(COUNT)    
end = time.time()
print('Tiempo en segundos -', end - start)
