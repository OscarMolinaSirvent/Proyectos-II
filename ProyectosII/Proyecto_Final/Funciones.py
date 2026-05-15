from pyniryo import *
import sys

robot_ip = "172.16.190.25" 

try:
    robot = NiryoRobot(robot_ip) # Conexión real
    conveyor_id = robot.set_conveyor() # Configurar ID de la cinta
except Exception as e:
    print("Error de conexión:", e)
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

def move_joints(j1, j2, j3, j4, j5, j6):
    robot.move(JointsPosition(j1, j2, j3, j4, j5, j6))