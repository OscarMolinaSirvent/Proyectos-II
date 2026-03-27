import logging
import threading
import keyboard
import time

from pyniryo import *

robot = NiryoRobot("127.0.0.1")
bloquear = threading.Lock()
continuar_hilo = True

def hilo(num):
    while continuar_hilo:    
        with bloquear:
            angulos = robot.get_joints()
            print("Posición brazos \n", angulos)
            time.sleep(1.0)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    cambio_rapido = 0.1
    cambio_lento = 0.01

    robot.calibrate_auto()

    x = 0.1
    y = -0.2
    z = 0.5

    robot.move(JointsPosition(x, y, z, 0.0, 0.0, 0.0))
    logging.info("Programa principal")

    h = threading.Thread(target=hilo, args=(1,))
    h.start()

    while True:
            # wait espera a que se presione una tecla
            tecla = keyboard.read_key() 
            logging.info(f"Tecla presionada: {tecla}")    
            if tecla == "j":
                logging.info("Saliendo...")
                continuar_hilo = False
                break
            if tecla == "v":
                 longitud = cambio_rapido
            elif tecla == "b":
                longitud = cambio_lento
            #Teclas para movimiento del robot y su velocidad
            with bloquear:
                if tecla == "q": x += longitud
                elif tecla == "a": x -= longitud
                elif tecla == "w": y += longitud
                elif tecla == "s": y -= longitud
                elif tecla == "e": z += longitud
                elif tecla == "d": z -= longitud
                    
                    
                if tecla in "qawsed":
                    robot.move(JointsPosition(x, y, z, 0.0, 0.0, 0.0))

    time.sleep(0.5)

    h.join(timeout=10.1)
    robot.close_connection()
