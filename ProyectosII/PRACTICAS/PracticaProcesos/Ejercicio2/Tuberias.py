import logging
from multiprocessing import Process, Pipe
import multiprocessing
import keyboard

def PROCTRL(tub):
    name = multiprocessing.current_process().name
    logging.info(f'{name} iniciado')
    tecla = keyboard.read_key()
    logging.info(f'Tecla presionada: {tecla}')
    tub.send(tecla)
    while(tub.poll(timeout=0.01)):
        ret=tub.recv()
        logging.info(f'El proceso recibió: {ret}')
    logging.info('Proceso finalizado')

def PROCPRIN(tub):
    name = multiprocessing.current_process().name
    logging.info(f'{name} iniciado')
    ret = tub.recv() 
    logging.info(f"Se recibio la tecla: {ret}")
        
    tub.send(f"Confirmado, recibí la tecla {ret}")


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

    