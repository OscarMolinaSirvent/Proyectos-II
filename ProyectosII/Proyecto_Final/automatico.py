from pyniryo import *

sensor_pin_id1 = PinID.DI5
sensor_pin_id2 = PinID.DI1
contador = 0

robot = NiryoRobot("127.0.0.1")

#robot.calibrate_auto()
robot.update_tool()
conveyor_id = robot.set_conveyor()

def PickPlace():
    global contador
    robot.release_with_tool()
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)#Pos Inicial
    
    robot.move_joints(-0.68, -0.38, -0.30,-0.21,-1.09, -0.60) #Posicion de ataque
    robot.move_joints(-0.69, -0.47, -0.32, -0.23 , -1.10, -0.58) #Pos cogida
    robot.grasp_with_tool()
    robot.move_joints(-0.68, -0.38, -0.30,-0.21,-1.09, -0.60) #Pos ataque
    
    robot.move_joints(-0.72, -0.70, 0.10, -0.02, -0.96, -0.89)#Pos ataque cinta
    robot.move_joints(-0.76, -0.73, 0.03, -0.03, -0.86, -0.88)#Pos dejar cinta
    robot.release_with_tool()
    robot.move_joints(-0.72, -0.65, 0.24, 0.01, -1.16, -0.84)#Pos ataque cinta
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    while robot.digital_read(sensor_pin_id1) == PinState.HIGH:
        robot.wait(0.1)
    robot.wait(0.5)
    robot.stop_conveyor(conveyor_id)
    if(robot.digital_read(sensor_pin_id2)) == PinState.LOW:
        Defectuosas()
        return 1
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    robot.wait(4)
    robot.stop_conveyor(conveyor_id)
    if contador == 0:
        MovimientoMesa1()
        contador += 1
    elif contador == 1:
        MovimientoMesa2()
        contador += 1
    return 0
def MovimientoMesa1():
    robot.release_with_tool()
    robot.move_joints(0.84,-0.99,0.60,-0.02,-1.26,0.02)
    robot.move_joints(0.84,-0.99,0.52,-0.03,-1.14,0.03)
    
    
    robot.grasp_with_tool()#Primera dejada
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)#Pos Inicial
    robot.move_joints(1.80,0.03,-0.99,0.10,-0.70,0.12)
    robot.move_joints(1.80,-0.08,-1.03,0.09,-0.50,0.11)
    robot.release_with_tool()
    robot.move_joints(1.80,0.03,-0.99,0.10,-0.70,0.12)
    
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)#Pos Inicial
    
def MovimientoMesa2():
    robot.release_with_tool()
    robot.move_joints(0.84,-0.99,0.60,-0.02,-1.26,0.02)
    robot.move_joints(0.84,-0.99,0.52,-0.03,-1.14,0.03)
    
    robot.grasp_with_tool()#Primera dejada
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)#Pos Inicial
    robot.move_joints(1.71,-0.57,-0.15,0.00,-0.88,0.17)
    robot.move_joints(1.70,-0.65,-0.15,0.00,-0.80,0.16)
    robot.release_with_tool()
    robot.move_joints(1.71,-0.57,-0.15,0.00,-0.88,0.17)
    robot.move_joints(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)#Pos Inicial
    
def Defectuosas():
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
    robot.wait(10)
    robot.stop_conveyor(conveyor_id)
    
PickPlace()
PickPlace()
PickPlace()
        
        

    
robot.unset_conveyor(conveyor_id)
robot.close_connection()
