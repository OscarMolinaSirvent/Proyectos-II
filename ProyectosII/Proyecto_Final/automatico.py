from pyniryo import *
import csv
from datetime import datetime  # Para saber cuándo se registró cada movimiento

# --- Configuración de Pines y Variables ---
sensor_pin_id1 = PinID.DI5
sensor_pin_id2 = PinID.DI1
contador = 0
cinta_activa = False # Variable para trackear si la cinta está encendida o no

# --- Configuración del Archivo CSV ---
archivo_csv = "registro_robot.csv"
columnas = ["Timestamp", "j1", "j2", "j3", "j4", "j5", "j6", "Herramienta", "Cinta_Estado", "Sensor_1", "Sensor_2"]

# Inicializar el archivo CSV con sus cabeceras (si el archivo no existe, lo crea)
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f)
    escritor.writerow(columnas)

# --- Conexión al Robot ---
robot = NiryoRobot("127.0.0.1")
robot.calibrate_auto()
robot.update_tool()
conveyor_id = robot.set_conveyor()

# --- Función para registrar datos ---
def registrar_estado(estado_herramienta="Desconocido"):
    """Captura el estado actual del robot y lo añade al CSV"""
    global cinta_activa
    
    # 1. Obtener posición de los ejes [j1, j2, j3, j4, j5, j6]
    pos_articulacion = robot.get_joints()
    
    # 2. Leer los sensores
    s1 = "HIGH" if robot.digital_read(sensor_pin_id1) == PinState.HIGH else "LOW"
    s2 = "HIGH" if robot.digital_read(sensor_pin_id2) == PinState.HIGH else "LOW"
    
    # 3. Preparar la fila de datos
    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], 
        pos_articulacion[0], pos_articulacion[1], pos_articulacion[2], 
        pos_articulacion[3], pos_articulacion[4], pos_articulacion[5],
        estado_herramienta,
        "ENCENDIDA" if cinta_activa else "PARADA",
        s1, s2
    ]
    

    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(fila)




def PickPlace():
    global contador, cinta_activa
    
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) # Pos Inicial
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.68, -0.38, -0.30,-0.21,-1.09, -0.60)) # Posicion de ataque
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.69, -0.47, -0.32, -0.23 , -1.10, -0.58)) # Pos cogida
    registrar_estado("Abierta")
    
    robot.grasp_with_tool()
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(-0.68, -0.38, -0.30,-0.21,-1.09, -0.60)) # Pos ataque
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(-0.72, -0.70, 0.10, -0.02, -0.96, -0.89)) # Pos ataque cinta
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(-0.76, -0.73, 0.03, -0.03, -0.86, -0.88)) # Pos dejar cinta
    registrar_estado("Cerrada (Objeto)")
    
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.72, -0.65, 0.24, 0.01, -1.16, -0.84)) # Pos ataque cinta
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0))
    registrar_estado("Abierta")
    
    # Control de cinta
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    cinta_activa = True
    registrar_estado("Abierta")

    #Quitar el comentario para simulacion fisica
    #while robot.digital_read(sensor_pin_id1) == PinState.HIGH:
    #   robot.wait(0.1)
        
    robot.wait(0.5)
    robot.stop_conveyor(conveyor_id)
    cinta_activa = False
    registrar_estado("Abierta")
    
    if robot.digital_read(sensor_pin_id2) == PinState.LOW:
        Defectuosas()
        return 1
        
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    cinta_activa = True
    registrar_estado("Abierta")
    
    robot.wait(4)
    robot.stop_conveyor(conveyor_id)
    cinta_activa = False
    registrar_estado("Abierta")
    
    if contador == 0:
        MovimientoMesa1()
        contador += 1
    elif contador == 1:
        MovimientoMesa2()
        contador += 1
    return 0

def MovimientoMesa1():
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    
    robot.grasp_with_tool() # Primera dejada
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) # Pos Inicial
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(1.80,0.03,-0.99,0.10,-0.70,0.12))
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(1.80,-0.08,-1.03,0.09,-0.50,0.11))
    registrar_estado("Cerrada (Objeto)")
    
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(1.80,0.03,-0.99,0.10,-0.70,0.12))
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) # Pos Inicial
    registrar_estado("Abierta")
    
def MovimientoMesa2():
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    
    robot.grasp_with_tool() # Primera dejada
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) # Pos Inicial
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(1.71,-0.57,-0.15,0.00,-0.88,0.17))
    registrar_estado("Cerrada (Objeto)")
    
    robot.move(JointsPosition(1.70,-0.65,-0.15,0.00,-0.80,0.16))
    registrar_estado("Cerrada (Objeto)")
    
    robot.release_with_tool()
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(1.71,-0.57,-0.15,0.00,-0.88,0.17))
    registrar_estado("Abierta")
    
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) # Pos Inicial
    registrar_estado("Abierta")
    
def Defectuosas():
    global cinta_activa
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
    cinta_activa = True
    registrar_estado("Desconocido")
    
    robot.wait(10)
    
    robot.stop_conveyor(conveyor_id)
    cinta_activa = False
    registrar_estado("Desconocido")
    
# --- Ejecución del Ciclo ---
PickPlace()
PickPlace()
PickPlace()
    
# --- Cierre de Conexiones ---
robot.unset_conveyor(conveyor_id)
robot.close_connection()