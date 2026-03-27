import socket
from pyniryo import *
import numpy as np

def emisor():
    # 1. Conexión y Configuración Inicial
    robot = NiryoRobot("127.0.0.1")
    
    robot.calibrate_auto()
    robot.update_tool()
    
    # Intentamos detectar la cinta, si falla, asignamos ID 1 por defecto
    conveyor_id = robot.set_conveyor()
    if conveyor_id is None:
        conveyor_id = ConveyorID.ID_1
        
    robot.stop_conveyor(conveyor_id)

    # 2. Definición de Pines
    sensor_pin_id = PinID.DI5
    robot.wait(1)



    # --- Secuencia de Movimiento ---
    while(True):
        # Posición inicial
        robot.move(JointsPosition(0.0002, 0.4994, -1.2506, 0, 0, 0))
        robot.release_with_tool()
        robot.wait(1.0) 

        # Posición ataque y cogida
        robot.move(JointsPosition(-2.3541, -1.0064, 0.4355, 0, -1.0002, -2.5294))
        robot.move(JointsPosition(-2.3602, -1.1518, 0.5461, 0, -0.9649, -2.2778))
        robot.grasp_with_tool()
        robot.wait(1.0)         
        # Volver a posición de seguridad tras coger el objeto
        robot.move(JointsPosition(-2.3541, -1.0064, 0.4355, 0, -1.0002, -2.5294))

        # Punto dejada en la cinta
        robot.move(JointsPosition(-0.9174, -0.4671, -0.2689, 0.0108, -0.8376, -0.911))
        robot.move(JointsPosition(-0.9174, -0.5504, -0.2931, 0.0123, -0.7302, -0.9126))
        robot.release_with_tool()
        robot.wait(0.5)
        
        # Retirar brazo para no chocar
        robot.move(JointsPosition(-0.9174, -0.4671, -0.2689, 0.0108, -0.8376, -0.911))

        # 3. Control de la Cinta con el Sensor
        robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)
        
        # Bucle de espera: se detiene cuando el objeto llega al sensor (cambia a LOW)
        print("Moviendo cinta... esperando sensor.")
        
        
        # Una vez detectado, esperamos un poco para que avance al centro y paramos
        robot.wait(1.5) 
        robot.stop_conveyor(conveyor_id)
        print("Ciclo finalizado.")

# Ejecución de la función
if __name__ == "__main__":
    emisor()