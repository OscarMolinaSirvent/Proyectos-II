from pyniryo import *
sensor_pin_id = PinID.DI5


robot = NiryoRobot("127.0.0.1")

robot.calibrate_auto()
robot.update_tool()
conveyor_id = robot.set_conveyor()


def PickandPlace():
    robot.stop_conveyor(conveyor_id)
    #Pos iniciaL
    robot.move(JointsPosition(0.0002,0.4994,-1.2506,0,0,0))
    robot.release_with_tool()
    robot.wait(0.5)

    #Pos ataque y cogida
    robot.move(JointsPosition(-2.3541,-1.0064,0.4355,0,-1.0002,-2.5294))
    robot.move(JointsPosition(-2.3602,-1.1518,0.5461,0,-0.9649,-2.2778))
    robot.grasp_with_tool()
    robot.wait(0.5)
    robot.move(JointsPosition(-2.3541,-1.0064,0.4355,0,-1.0002,-2.5294))

    #Punto dejada cinta
    robot.move(JointsPosition(-0.9174,-0.4671,-0.2689,0.0108,-0.8376,-0.911))
    robot.move(JointsPosition(-0.9174,-0.5504,-0.2931,0.0123,-0.7302,-0.9126))
    robot.release_with_tool()
    robot.wait(0.5)
    robot.move(JointsPosition(-0.9174,-0.4671,-0.2689,0.0108,-0.8376,-0.911))

    robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)
    while robot.digital_read(sensor_pin_id) == PinState.HIGH:
        robot.wait(0.1)

    robot.wait(3)
    robot.stop_conveyor(conveyor_id)

def DejadaMesa(x,y):
    robot.move(JointsPosition(0.9544,-0.608,-0.1053,0,-0.8575,1.9973))
    robot.move(JointsPosition(0.9544,-0.6595,-0.1189,0,-0.7916,1.9973))
    robot.grasp_with_tool()
    robot.wait(0.5)
    robot.move(JointsPosition(0.9544,-0.608,-0.1053,0,-0.8575,1.9973))
    contador = 0
    robot.move(PoseObject(x,y,0.0983,2.7175,1.5706,2.6714))
    robot.move(PoseObject(x,y,0.085,2.7175,1.5706,2.6714))
    robot.release_with_tool()
    robot.wait(0.5)
    robot.move(PoseObject(x,y,0.0983,2.7175,1.5706,2.6714))
    robot.move(JointsPosition(0.0002,0.4994,-1.2506,0,0,0))
    

def main():
    x = -0.2269
    y = 0.2296
    for i in range(4):
        PickandPlace()
        DejadaMesa(x,y)

        if i == 0:
            y += 0.05
        elif i == 1:
            y = 0.2296
            x += 0.05
        elif i == 2:
            y += 0.05
