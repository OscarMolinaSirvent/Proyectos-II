import multiprocessing
from multiprocessing import shared_memory
import time
import logging
from random import randint
lock = multiprocessing.Lock()

# Configuración básica de logging para que se vean los mensajes
logging.basicConfig(level=logging.INFO)

def proceso(n,id):
    name = multiprocessing.current_process().name
    print("------------------------- proceso:", name)
    shmp = shared_memory.SharedMemory(name="buffsh4", create=False)
    contador = 0
    while True:
        num = randint(n, n + 24)
        contador += 1
        with lock:
            shmp.buf[0] = num
            shmp.buf[1] = id
        time.sleep(0.1)
    shmp.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(name="buffsh4", create=True, size=10)
    num = randint(0, 100)
    shm.buf[0] = num
    print("ha de adivinar", num)
    p1 = multiprocessing.Process(name="PROCESO1", target=proceso, args=(0,1))
    p2 = multiprocessing.Process(name="PROCESO2", target=proceso, args=(25,2))
    p3 = multiprocessing.Process(name="PROCESO3", target=proceso, args=(50,3))
    p4 = multiprocessing.Process(name="PROCESO4", target=proceso, args=(75,4))
    time.sleep(5)
    start = time.time()
    p1.start() # time.sleep(0.5)
    p2.start()
    p3.start()
    p4.start()
    
    while shm.buf[0] != num:
        pass
    
    print(f"Termino la busqueda, con el numero: {shm.buf[0]} por el proceso: {shm.buf[1]}")
    p1.terminate()
    p2.terminate()
    p3.terminate()
    p4.terminate()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    end = time.time()
    logging.info("Main:     esperando que termine todo")
    shm.close()
    shm.unlink()
    print('Tiempo de ejecución:', end - start)