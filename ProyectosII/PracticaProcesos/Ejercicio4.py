import multiprocessing
from multiprocessing import shared_memory
import time
import logging
from random import randint

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

def proceso(n, id, lock): # Añadimos lock a los argumentos
    name = multiprocessing.current_process().name
    print("------------------------- proceso:", name)
    shmp = shared_memory.SharedMemory(name="buffsh4", create=False)
    contador = 0
    while True:
        num = randint(n, n + 24)
        contador += 1
        with lock: # El bloqueo solo para escribir
            shmp.buf[0] = num
            shmp.buf[1] = id
        
        # EL SLEEP DEBE IR FUERA DEL LOCK
        # Si está dentro, los otros procesos no pueden trabajar
        time.sleep(0.01) 
    shmp.close()

if __name__ == "__main__":
    shm = shared_memory.SharedMemory(name="buffsh4", create=True, size=10)
    lock = multiprocessing.Lock() # Creamos el cerrojo
    
    num = randint(0, 100)
    shm.buf[0] = 255 # Valor inicial neutro
    print("ha de adivinar", num)
    
    # Pasamos el lock en los args
    p1 = multiprocessing.Process(name="PROCESO1", target=proceso, args=(0, 1, lock))
    p2 = multiprocessing.Process(name="PROCESO2", target=proceso, args=(25, 2, lock))
    p3 = multiprocessing.Process(name="PROCESO3", target=proceso, args=(50, 3, lock))
    p4 = multiprocessing.Process(name="PROCESO4", target=proceso, args=(75, 4, lock))
    
    time.sleep(5)
    start = time.time()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    # El padre espera a que el valor en memoria coincida
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