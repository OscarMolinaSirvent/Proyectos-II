from niryo_robot_python_ros_wrapper import * # Importar librería oficial
import sys

robot_ip = "127.0.0.1" 

try:
    robot = NiryoRobot(robot_ip) # Conexión real
    conveyor_id = robot.set_conveyor() # Configurar ID de la cinta
except:
    print("No se pudo conectar al robot")
    sys.exit()

def run_conv():
    robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

def stop_conv():
    robot.stop_conveyor(conveyor_id)


def get_pose():
    pose = robot.get_pose()
    return {
        "x": pose.x, "y": pose.y, "z": pose.z,
        "roll": pose.roll, "pitch": pose.pitch, "yaw": pose.yaw
    }

def move_to(x, y, z, roll, pitch, yaw):
    robot.move_pose(x, y, z, roll, pitch, yaw)