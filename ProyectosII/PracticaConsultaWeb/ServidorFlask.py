import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from Funciones import *
import Funciones
from ComunicacionDB import *

app = Flask(__name__)
CORS(app) 


@app.route("/startCinta", methods=["POST"])
def runcov():
    # Usamos threading para no bloquear el servidor mientras el robot se mueve
    print("Boton Pulsado")
    threading.Thread(target=run_conv).start()
    return jsonify({"status": "cinta funcionando"})

@app.route("/stopCinta", methods=["POST"])
def stop_cinta():
    threading.Thread(target=stop_conv).start()
    return jsonify({"status": "cinta detenida"})


@app.route("/get_position", methods=["GET"])
def get_position():
    posicion = Funciones.get_pose()
    return jsonify(posicion)

"""@app.route("/paletizadas", methods=["POST"])
def paletizadas():
    # Aquí podrías llevar un contador real
    niryo.piezas_contadas += 1
    return jsonify({"piezas": niryo.piezas_contadas})"""



@app.route("/move", methods=["POST"])
def move_robot():
    data = request.json # Recibimos el objeto enviado desde JS
    
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
    #obtenemos el elemento por el que filtrar
    elemento = request.args.get("elemento")
    #obtener_logs se encuentra en el fichero de conexión a la BD
    logs = obtener_logs(conexion, elemento)
    #Creación del HTML
    html = "<h2>Logs de Niryo</h2>"
    for fecha, elem, instruccion in logs:
            html += f"<li><strong>{fecha}</strong> [{elem}] - {instruccion}</li>"
    return html #Devolvemos el HTML generado

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)