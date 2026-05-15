from pyniryo import *
import time

robot_ip = "127.0.0.1" 
try:
    robot = NiryoRobot(robot_ip)
    conveyor_id = robot.set_conveyor()
except Exception as e:
    print("Error de conexión:", e)

def get_pose():
    try:
        p = robot.get_pose()
        return {"x": p.x, "y": p.y, "z": p.z, "roll": p.roll, "pitch": p.pitch, "yaw": p.yaw}
    except:
        return {"x":0,"y":0,"z":0,"roll":0,"pitch":0,"yaw":0}

def move_joints(j1, j2, j3, j4, j5, j6):
    try:
        robot.move_joints(j1, j2, j3, j4, j5, j6)
    except:
        pass

def run_conv():
    try:
        robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)
    except:
        pass

def stop_conv():
    try:
        robot.stop_conveyor(conveyor_id)
    except:
        pass

def control_gripper(open_it):
    try:
        if open_it: robot.open_gripper()
        else: robot.close_gripper()
    except:
        pass

def stop_all():
    try:
        robot.stop_conveyor(conveyor_id)
        # robot.abort_current_move() # Descomentar si la versión de pyniryo lo soporta
    except:
        pass

def secuencia_automatica():
    """Modifica este ciclo con los movimientos reales de tu proyecto"""
    print("Iniciando Proceso...")
    try:
        robot.move_to_home()
        run_conv()
        time.sleep(3)
        stop_conv()
        robot.open_gripper()
        robot.close_gripper()
        robot.move_to_home()
    except Exception as e:
        print("Ciclo abortado o error:", e)