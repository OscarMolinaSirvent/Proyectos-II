from pyniryo import *
import csv
import threading
import time
import os

bloquear = threading.Lock()

try:
    robot = NiryoRobot("127.0.0.1")
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
    robot.stop_conveyor(conveyor_id)
except Exception as e:
    print(f"Error: {e}")
    exit()

terminar = False
ruta_fichero = 'Ejercicio4/Datos.csv'

def Guardado():
    global terminar
    try:
        with open(ruta_fichero, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['J1', 'J2', 'J3', 'J4', 'J5', 'J6'])
            
            while not terminar:
                with bloquear:
                    angulos = robot.get_joints()
                
                if angulos:
                    escritor.writerow(angulos)
                    archivo.flush()
                
                time.sleep(1)
    except Exception as e:
        print(f"Error hilo: {e}")

if __name__ == "__main__":
    t1 = threading.Thread(target=Guardado)
    t1.daemon = True
    t1.start()

    try:
        with bloquear:
            robot.wait(0.5)

        with bloquear:
            robot.move(JointsPosition(-2.3541, -1.0064, 0.4355, 0, -1.0002, -2.5294))
        
        with bloquear:
            robot.move(JointsPosition(-2.3602, -1.1518, 0.5461, 0, -0.9649, -2.2778))
        
        with bloquear:
            robot.wait(0.5)
            robot.move(JointsPosition(-2.3541, -1.0064, 0.4355, 0, -1.0002, -2.5294))

        with bloquear:
            robot.move(JointsPosition(-0.9174, -0.4671, -0.2689, 0.0108, -0.8376, -0.911))
        
        with bloquear:
            robot.move(JointsPosition(-0.9174, -0.5504, -0.2931, 0.0123, -0.7302, -0.9126))
        
        with bloquear:
            robot.wait(0.5)
            robot.move(JointsPosition(-0.9174, -0.4671, -0.2689, 0.0108, -0.8376, -0.911))

    except Exception as e:
        print(f"Error main: {e}")
    
    finally:
        terminar = True
        t1.join(timeout=2)
        print("Proceso finalizado.")