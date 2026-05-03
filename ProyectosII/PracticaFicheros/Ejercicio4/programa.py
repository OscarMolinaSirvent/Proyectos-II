from pyniryo import *

with open("PracticaFicheros/Ejercicio4/Palet.txt", "r") as file:
    paletizado = file.readline().split()

with open("PracticaFicheros/Ejercicio4/Objeto.txt", "r") as file:
    objeto = file.readline().split()

with open("PracticaFicheros/Ejercicio4/Frecuencia.txt", "r") as file:
    frec = file.readline().split()

robot = NiryoRobot("127.0.0.1")
robot.calibrate_auto()
robot.update_tool()
conveyor_id = robot.set_conveyor()
robot.stop_conveyor(conveyor_id)
print(objeto)

robot.move(objeto)

