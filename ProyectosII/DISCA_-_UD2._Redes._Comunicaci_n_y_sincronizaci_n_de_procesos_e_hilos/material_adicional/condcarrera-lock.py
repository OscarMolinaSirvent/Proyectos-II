import logging
import threading
import time 
import random
import concurrent.futures

class FakeDatabase:
    def __init__(self):
        self.value=0 #inicializa el valor a 0
        self._lock = threading.Lock()

    def update(self, name): #"simula" leer el valor de una BBDD
        #hacer unos cálculos, y reescribir el resultado en la BBDD
        with self._lock:
            logging.info("thread %s: inicia actualización. %s ",name, self.value) 
            logging.info("thread %s: ejecuta el lock ",name)   
            logging.info("thread %s: tiene el lock ",name)   
            local_copy = self.value
            local_copy +=1
            time.sleep(random.randint(1, 5))
            self.value= local_copy
            logging.info("thread %s: va a liberar el lock con self.value = %d ", name, self.value)    
        logging.info("thread %s: tras el release ", name)    
        logging.info("thread %s: actualización terminada ", name)    

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

    database = FakeDatabase()
    
    logging.info("Probando actualización. Valor inicial %s", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Probando actualización. Valor final %s", database.value)