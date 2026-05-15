import multiprocessing
from multiprocessing import shared_memory
import time
import logging
from random import randint

# Configuración básica de logging para que se vean los mensajes
logging.basicConfig(level=logging.INFO)

def proceso(n):
    name = multiprocessing.current_process().name
    print("------------------------- proceso:", name)
    shmp = shared_memory.SharedMemory(name="buffsh4", create=False)
    contador = 0
    while True:
        num = randint(0, 100)
        contador += 1
        shmp.buf[0] = num
        print("intento ", contador, num)
        time.sleep(0.1)
    shmp.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(name="buffsh4", create=True, size=10)

    num = randint(0, 100)
    shm.buf[0] = num
    print("ha de adivinar", num)
    time.sleep(5)
    start = time.time()
    
    p1 = multiprocessing.Process(name="PROCESO", target=proceso, args=(1,))
    p1.start() # time.sleep(0.5)
    while shm.buf[0] != num:
        pass
    
    print("Terminando", shm.buf[0])
    p1.terminate()
    p1.join()
    
    end = time.time()
    logging.info("Main:     esperando que termine todo")
    shm.close()
    shm.unlink()
    print('Tiempo de ejecución:', end - start)