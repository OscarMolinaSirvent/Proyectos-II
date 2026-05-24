import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from Funciones import *
import Funciones
from ComunicacionDB import *
import time

app = Flask(__name__)
CORS(app) 

posicion_actual = {"status": "inicializando"}
# Evita colisiones de lectura/escritura de la variable en memoria de Flask
pos_lock = threading.Lock()

def bucle_actualizacion_posicion():
    """Bucle infinito en hilo daemon que actualiza la variable local."""
    global posicion_actual
    while True:
        try:
            # Llama de forma segura al get_pose() controlado por su lock interno
            nueva_pos = Funciones.get_pose()
            
            with pos_lock:
                posicion_actual = nueva_pos
                
        except Exception as e:
            print(f"Error al leer la posición del robot: {e}")
            
        time.sleep(0.15) # Espera de 150ms

threading.Thread(target=bucle_actualizacion_posicion, daemon=True).start()


@app.route("/startCinta", methods=["POST"])
def runcov():
    print("Boton Pulsado")
    threading.Thread(target=run_conv).start()
    return jsonify({"status": "cinta funcionando"})

@app.route("/stopCinta", methods=["POST"])
def stop_cinta():
    threading.Thread(target=stop_conv).start()
    return jsonify({"status": "cinta detenida"})


@app.route("/startAuto", methods=["POST"])
def ruta_automatico():
    print("Iniciando ciclo automático...")
    threading.Thread(target=Funciones.automatico).start()
    return jsonify({"status": "proceso automatico iniciado"})


@app.route("/get_position", methods=["GET"])
def get_position():
    with pos_lock:
        posicion = posicion_actual
    return jsonify(posicion)


@app.route("/move", methods=["POST"])
def move_robot():
    data = request.json

    j1 = data.get("j1")
    j2 = data.get("j2")
    j3 = data.get("j3")
    j4 = data.get("j4")
    j5 = data.get("j5")
    j6 = data.get("j6")

    threading.Thread(target=Funciones.move_joints, args=(j1, j2, j3, j4, j5, j6)).start()
    return jsonify({"status": "movimiento iniciado"})

@app.route("/log")
def ver_logs():
    conexion = conectar("omolsir", "omolsir")
    elemento = request.args.get("elemento")
    logs = obtener_logs(conexion, elemento)
    print(elemento)
    
    html = "<h2>Logs de Niryo</h2>"
    for fecha, elem, instruccion in logs:
        html += f"<li><strong>{fecha}</strong> [{elem}] - {instruccion}</li>"
    return html

@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    conexion = conectar("omolsir", "omolsir")
    if not conexion:
        return jsonify({"success": False, "message": "Error de conexión con BD"}), 500

    tipo_usuario = verificar_credenciales(conexion, usuario, password)
    conexion.close()
    print(f"Usuario: {usuario}, Tipo: {tipo_usuario}, Contraseña: {password}")
    if tipo_usuario:
        return jsonify({
            "success": True, 
            "tipo": tipo_usuario, 
            "mensaje": f"Bienvenido, {usuario}"
        })
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)