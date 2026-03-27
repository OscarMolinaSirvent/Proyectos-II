# !/usr/bin/env python3
import logging
import threading
import time

from pyniryo import *
robot = NiryoRobot("127.0.0.1")
candado = threading.Lock() # Este lock se usará para sincronizar el acceso a los movimientos del robot
bloquear = threading.Lock() # Usamos este lock para evitar condiciones de carrera

def hilo(nomb):
    logging.info(f"Hilo {nomb}: Iniciado")
    dentro = True
    
    while dentro:
        with candado: # <---Lectura del movimiento actual del robot
            angulos = robot.get_joints()
        
        if nomb == 1:
            with bloquear: # <---Modificación del movimiento del robot
                angulos[0] += 0.1
                if angulos[0] > 0.8:
                    dentro = False  
        elif nomb == 2:
            with bloquear: # <---Modificación del movimiento del robot
                angulos[1] -= 0.1
                if angulos[1] < -0.1:
                    dentro = False              
        elif nomb == 3:
            with bloquear: # <---Modificación del movimiento del robot
                angulos[2] += 0.1
                if angulos[2] > -0.8:
                    dentro = False
        
        logging.info(f"Hilo {nomb}: Moviendo articulación...")
        with candado:  # <---Lectura del movimiento actual del robot         
            robot.move(JointsPosition(*angulos))
            actuales = robot.get_joints()
        time.sleep(0.1)
        
        print(f"Hilo {nomb} en posición: {actuales}")       

if __name__ == "__main__":
    format = "%(asctime)s: %(message) s"
    logging.basicConfig(format=format,level=logging.INFO, datefmt="%H;%M;%S")

    robot.calibrate_auto()

    robot.move(JointsPosition(0.105, 0.600, -1.2, 0.000, 0.000, 0.000))
    time.sleep(2)
    angulo = robot.get_joints()
    print(angulo)
    time.sleep(1)
    logging.info("programa principal")
    time.sleep(1)
    x1 = threading.Thread(target=hilo, args=(1,))
    x2 = threading.Thread(target=hilo, args=(2,))
    x3 = threading.Thread(target=hilo, args=(3,))
    x1.start()
    x2.start()
    x3.start()

    print("terminado")
    x1.join()#timeout=10.1)
    x2.join()#timeout=10.1)
    x3.join()#timeout=10.1)    
    print("fin hilos")
    robot.close_connection()