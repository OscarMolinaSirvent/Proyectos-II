import socket
from pyniryo import *
import csv

HOST = '127.0.0.2'
PORT = 65432

def emisor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        print(f"Conectado al servidor en {HOST}:{PORT}")

        texto = "¡Hola, servidor! Este es un mensaje desde el emisor."
        cliente.sendall(texto.encode('utf-8'))

        robot = NiryoRobot("127.0.0.1")

        robot.calibrate_auto()
        robot.update_tool()
        conveyor_id = robot.set_conveyor()
        robot.stop_conveyor(conveyor_id)

        for i in range(3):
            #Pos iniciaL
            robot.move(JointsPosition(0.0002,0.4994,-1.2506,0,0,0))
            robot.release_with_tool()
            robot.wait(0.5)
            texto = f"Iteración {i+1}: Posición inicial alcanzada."
            cliente.sendall(texto.encode('utf-8'))

            #Pos ataque y cogida
            robot.move(JointsPosition(-2.3541,-1.0064,0.4355,0,-1.0002,-2.5294))
            robot.move(JointsPosition(-2.3602,-1.1518,0.5461,0,-0.9649,-2.2778))
            robot.grasp_with_tool()
            robot.wait(0.5)
            robot.move(JointsPosition(-2.3541,-1.0064,0.4355,0,-1.0002,-2.5294))
            texto = f"Iteración {i+1}: Objeto cogido."
            cliente.sendall(texto.encode('utf-8'))

            #Punto dejada cinta
            robot.move(JointsPosition(-0.9174,-0.4671,-0.2689,0.0108,-0.8376,-0.911))
            robot.move(JointsPosition(-0.9174,-0.5504,-0.2931,0.0123,-0.7302,-0.9126))
            robot.release_with_tool()
            robot.wait(0.5)
            robot.move(JointsPosition(-0.9174,-0.4671,-0.2689,0.0108,-0.8376,-0.911))
            texto = f"Iteración {i+1}: Objeto dejado en la cinta."
            cliente.sendall(texto.encode('utf-8'))

            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)
            texto = f"Iteración {i+1}: Cinta transportadora activada."
            cliente.sendall(texto.encode('utf-8'))

            robot.wait(1)

            robot.stop_conveyor(conveyor_id)
            texto = f"Iteración {i+1}: Cinta transportadora detenida."
            cliente.sendall(texto.encode('utf-8'))
            

        robot.move(JointsPosition(0.0002,0.4994,-1.2506,0,0,0))
        texto = "Proceso completado. Posición inicial alcanzada."
        cliente.sendall(texto.encode('utf-8'))