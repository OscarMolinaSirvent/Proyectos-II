from pyniryo import *
import sys
import csv
from datetime import datetime
import threading
from ComunicacionDB import *

robot_ip = "172.16.190.25" 

# Único lock para asegurar que no se solapen comandos en el socket TCP del robot
lock = threading.Lock()

# Evento para frenar el hilo del ciclo automático de forma inmediata
stop_urgente = threading.Event()

try:
    # --- Conexión al Robot ---
    robot = NiryoRobot(robot_ip)
    robot.calibrate_auto()
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
except Exception as e:
    print("Error de conexión:", e)
    sys.exit()

try:
    conexion_db = conectar("omolsir", "omolsir")
    insertar_log(conexion_db, "Inicio de sistema OMOLSIR", "Servidor Central")
except Exception as e:
    print("Error de conexión a la Base de Datos:", e)

# --- Configuración de Pines y Variables ---
sensor_pin_id1 = PinID.DI5
sensor_pin_id2 = PinID.DI1
contador = 0
cinta_activa = False 

def run_conv(velocidad):
    with lock:
        robot.run_conveyor(conveyor_id, speed=velocidad, direction=ConveyorDirection.FORWARD)
        insertar_log(conexion_db, "Cinta Activa", "Cinta")
        modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=velocidad, nueva_direccion="FORWARD", nuevo_estado="En Funcionamiento")

def stop_conv():
    with lock:
        robot.stop_conveyor(conveyor_id)
        insertar_log(conexion_db, "Cinta Detenida", "Cinta")
        modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=0, nueva_direccion="NULL", nuevo_estado="Detenida")

def get_pose():
    with lock:
        pose = robot.get_pose()
        return {
            "x": pose.x, "y": pose.y, "z": pose.z,
            "roll": pose.roll, "pitch": pose.pitch, "yaw": pose.yaw
        }

def move_joints(j1, j2, j3, j4, j5, j6):
    with lock:
        robot.move(JointsPosition(j1, j2, j3, j4, j5, j6))

# --- Configuración del Archivo CSV ---
archivo_csv = "registro_robot.csv"
columnas = ["Timestamp", "j1", "j2", "j3", "j4", "j5", "j6", "Herramienta", "Cinta_Estado", "Sensor_1", "Sensor_2"]

with open(archivo_csv, mode='w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f)
    escritor.writerow(columnas)

def registrar_estado(estado_herramienta="Desconocido"):
    """Captura el estado actual del robot y lo añade al CSV"""
    global cinta_activa
    
    # IMPORTANTE: No lleva 'with lock:' porque ya se ejecuta dentro de PickPlace 
    # que mantiene el lock activo durante toda su ejecución.
    pos_articulacion = robot.get_joints()
    s1 = "HIGH" if robot.digital_read(sensor_pin_id1) == PinState.HIGH else "LOW"
    s2 = "HIGH" if robot.digital_read(sensor_pin_id2) == PinState.HIGH else "LOW"
    
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

def verificar_parada():
    """Lanza una excepción si se ha solicitado detener la ejecución."""
    if stop_urgente.is_set():
        raise InterruptedError("HILO_DETENIDO: Parada de emergencia solicitada.")

def abrir_pinza():
    with lock:
        robot.release_with_tool()
        modificar_pinza(conexion_db, id_componente=2, nuevo_estado="Abierta")
        insertar_log(conexion_db, "Pinza Abierta", "Herramienta")
        registrar_estado("Abierta")
def cerrar_pinza():
    with lock:
        robot.grasp_with_tool()
        modificar_pinza(conexion_db, id_componente=2, nuevo_estado="Cerrada")
        insertar_log(conexion_db, "Pinza Cerrada", "Herramienta")
        registrar_estado("Cerrada (Objeto)")
        
def PickPlace():
    global contador, cinta_activa
    
    verificar_parada()
    robot.stop_conveyor(conveyor_id)
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=0, nueva_direccion="NULL", nuevo_estado="Detenida")
    insertar_log(conexion_db, "Cinta Detenida", "Cinta")
    insertar_comando(conexion_db, "MoveJoints", "N/A", "Automatico", "N/A", id_robot=1)
    robot.release_with_tool()
    modificar_pinza(conexion_db, id_componente=2, nuevo_estado="Abierta")
    insertar_log(conexion_db, "Pinza Abierta", "Herramienta")
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.move(JointsPosition(-0.6658,-0.4262,-0.2053,-0.2223,-1.2625,-0.6334)) 
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.move(JointsPosition(-0.696, -0.474, -0.315, -0.242 , -1.121, -0.604)) 
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.grasp_with_tool()
    modificar_pinza(conexion_db, id_componente=2, nuevo_estado="Cerrada")
    insertar_log(conexion_db, "Pinza Cerrada", "Herramienta")
    registrar_estado("Cerrada (Objeto)")
    
    verificar_parada()
    robot.move(JointsPosition(-0.68, -0.38, -0.30,-0.21,-1.09, -0.60)) 
    registrar_estado("Cerrada (Objeto)")
    
    verificar_parada()
    robot.move(JointsPosition(-0.72, -0.70, 0.10, -0.02, -0.96, -0.89)) 
    registrar_estado("Cerrada (Objeto)")
    
    verificar_parada()
    robot.move(JointsPosition(-0.76, -0.73, 0.03, -0.03, -0.86, -0.88)) 
    registrar_estado("Cerrada (Objeto)")
    
    verificar_parada()
    robot.release_with_tool()
    modificar_pinza(conexion_db, id_componente=2, nuevo_estado="Abierta")
    insertar_log(conexion_db, "Pinza Abierta", "Herramienta")
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.72, -0.65, 0.24, 0.01, -1.16, -0.84)) 
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0))
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    cinta_activa = True
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=80, nueva_direccion="FORWARD", nuevo_estado="En Funcionamiento")
    insertar_log(conexion_db, "Cinta Activa", "Cinta")
    registrar_estado("Abierta")
    
    while robot.digital_read(sensor_pin_id1) == PinState.HIGH:
        verificar_parada()
        modificar_sensor(conexion_db, id_componente=3, nuevo_tipo="1", nuevo_estado= "HIGH" if robot.digital_read(sensor_pin_id1) == PinState.HIGH else "LOW")
        modificar_sensor(conexion_db, id_componente=4, nuevo_tipo="2", nuevo_estado= "HIGH" if robot.digital_read(sensor_pin_id2) == PinState.HIGH else "LOW")
        robot.wait(0.1)

    verificar_parada()
    robot.wait(0.5)
    robot.stop_conveyor(conveyor_id)
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=0, nueva_direccion="NULL", nuevo_estado="Detenida")

    cinta_activa = False
    registrar_estado("Abierta")
    
    verificar_parada()
    if robot.digital_read(sensor_pin_id2) == PinState.LOW:
        modificar_sensor(conexion_db, id_componente=3, nuevo_tipo="1", nuevo_estado= "HIGH" if robot.digital_read(sensor_pin_id1) == PinState.HIGH else "LOW")
        modificar_sensor(conexion_db, id_componente=4, nuevo_tipo="2", nuevo_estado= "HIGH" if robot.digital_read(sensor_pin_id2) == PinState.HIGH else "LOW")
        Defectuosas()
        return 1 #Descomentar para activar función de defectuosas"""
        
    verificar_parada()
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.FORWARD)
    cinta_activa = True
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=80, nueva_direccion="FORWARD", nuevo_estado="En Funcionamiento")
    insertar_log(conexion_db, "Cinta Activa", "Cinta")
    registrar_estado("Abierta")
    
    verificar_parada()
    robot.wait(4)

    verificar_parada()
    robot.stop_conveyor(conveyor_id)
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=0, nueva_direccion="NULL", nuevo_estado="Detenida")
    insertar_log(conexion_db, "Cinta Detenida", "Cinta")
    cinta_activa = False
    registrar_estado("Abierta")
    verificar_parada()

    return 0

def MovimientoMesa1():
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    verificar_parada()
    robot.grasp_with_tool() 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.8028,-0.911,0.5688,0.0752,-1.2794,-0.1011))
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.80,0.03,-0.99,0.10,-0.70,0.12))
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.80,-0.08,-1.03,0.09,-0.50,0.11))
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(1.80,0.03,-0.99,0.10,-0.70,0.12))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Abierta")

def MovimientoMesa2():
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    verificar_parada()
    robot.grasp_with_tool() 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.8028,-0.911,0.5688,0.0752,-1.2794,-0.1011))
    robot.move(JointsPosition(1.6,0.2,-0.4,-0.14,-1.3,-0.11)) 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.6,-0.47,-0.37,0.009,-0.86,-0.08))
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.6,-0.47,-0.43,0.02,-0.74,-0.04))
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(1.6,-0.47,-0.37,0.009,-0.86,-0.08))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Abierta")

def MovimientoMesa3():
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    verificar_parada()
    robot.grasp_with_tool() 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.8028,-0.911,0.5688,0.0752,-1.2794,-0.1011))
    robot.move(JointsPosition(1.6,0.2,-0.4,-0.14,-1.3,-0.11)) 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.98,-0.08,-0.86,-0.04,-0.75,-0.5))#Ataque 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.98,-0.17,-0.88,-0.07,-0.65,-0.59))#Dejada
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.98,-0.08,-0.86,-0.04,-0.75,-0.5))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Abierta")

def MovimientoMesa4():
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.60,-0.02,-1.26,0.02))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(0.84,-0.99,0.52,-0.03,-1.14,0.03))
    registrar_estado("Abierta")
    verificar_parada()
    robot.grasp_with_tool() 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(0.8028,-0.911,0.5688,0.0752,-1.2794,-0.1011))
    robot.move(JointsPosition(1.6,0.2,-0.4,-0.14,-1.3,-0.11)) 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.2,-0.5,-0.2,0.013,-0.96,-0.44))#Ataque 
    registrar_estado("Cerrada (Objeto)")
    verificar_parada()
    robot.move(JointsPosition(1.2,-0.62,-0.2,-0.038,-0.9,-0.38))#Dejada
    verificar_parada()
    robot.release_with_tool()
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(1.2,-0.5,-0.2,0.013,-0.96,-0.44))
    registrar_estado("Abierta")
    verificar_parada()
    robot.move(JointsPosition(-0.05, 0.24, -0.61, -0.01, -0.32, 0.0)) 
    registrar_estado("Abierta")

    
def Defectuosas():
    global cinta_activa
    verificar_parada()
    robot.run_conveyor(conveyor_id, speed=80, direction=ConveyorDirection.BACKWARD)
    cinta_activa = True
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=80, nueva_direccion="BACKWARD", nuevo_estado="En Funcionamiento")
    insertar_log(conexion_db, "Cinta Activa", "Cinta")
    registrar_estado("Desconocido")
    
    for i in range(100):
        verificar_parada()
        robot.wait(0.1)
        
    verificar_parada()
    robot.stop_conveyor(conveyor_id)
    cinta_activa = False
    modificar_cinta(conexion_db, id_componente=1, nueva_velocidad=0, nueva_direccion="NULL", nuevo_estado="Detenida")
    insertar_log(conexion_db, "Cinta Detenida", "Cinta")
    registrar_estado("Desconocido")

def detener_ciclo_automatico():
    """Activa el flag de parada urgente para romper la ejecución del bucle."""
    stop_urgente.set()

x =-36
y = 155
def automatico():
    stop_urgente.clear()
    global x, y
    contador = 0
    actualizar_estado_robot(conexion_db, id_robot=1, nuevo_estado="En Ejecución")
    with lock:
        try:
            while True:
                if contador == 4:
                        contador = 0
                        break
                defect = PickPlace()
                modificar_ocupado(conexion_db, id_tablero=1, identificador_casilla=contador, nuevo_estado="Ocupado")
                if defect != 1:
                    
                    if contador == 0:
                        MovimientoMesa1()
                    elif contador == 1:
                        MovimientoMesa2()
                    elif contador == 2:
                        MovimientoMesa3()
                    elif contador == 3:
                        MovimientoMesa4()
                    contador += 1
                print(contador)

            actualizar_estado_robot(conexion_db, id_robot=1, nuevo_estado="En Espera")
            for i in range(1,5):
                modificar_ocupado(conexion_db, id_tablero=1, identificador_casilla=i, nuevo_estado="Libre")

        except InterruptedError as e:
            print(f"Aviso: {e}")
        except Exception as e:
            print(f"Error inesperado en ciclo: {e}")