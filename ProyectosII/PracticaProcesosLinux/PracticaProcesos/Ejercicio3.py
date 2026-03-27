import logging
import time
from multiprocessing import Process, Pipe
import multiprocessing

def PROCTRL(tub):
    name = multiprocessing.current_process().name
    logging.info(f'{name} iniciado')
    while True:
        ret=tub.recv()
        logging.info(f'El proceso recibió: {ret}')
        if ret == 0:
            break
    logging.info('Proceso finalizado')

def PROCPRIN(tub):
    name = multiprocessing.current_process().name
    logging.info(f'{name} iniciado')
    while True:
        for I in range(1,4):
            logging.info(f"Enviando: {I}")
            tub.send(I)
            time.sleep(1)

        logging.info("Enviando: 0")
        tub.send(0)
        break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    tub1, tub2 = Pipe(duplex=True) #Duplex = True para habilitar comunicacion en ambos sentidos
    p1=multiprocessing.Process(name="PROCESO1",target=PROCTRL, args=(tub1,))
    p2=multiprocessing.Process(name="PROCESO2",target=PROCPRIN, args=(tub2,))
    logging.info("Empezamos proceso1:")
    p1.start()
    logging.info("Empezamos proceso2:")
    p2.start()
    p1.join()
    p2.join()
    logging.info("Termino procesos")

    