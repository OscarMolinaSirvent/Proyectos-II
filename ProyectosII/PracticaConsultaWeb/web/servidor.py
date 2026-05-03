import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from niryo import run_conv
import niryo 

app = Flask(__name__)
CORS(app) 


@app.route("/startCinta", methods=["POST"])
def runcov():
    # Usamos threading para no bloquear el servidor mientras el robot se mueve
    print("Boton Pulsado")
    threading.Thread(target=run_conv, args=("")).start()
    return jsonify({"status": "cinta funcionando"})

@app.route("/cinta/stop", methods=["POST"])
def stop_cinta():
    niryo.stop_conveyor()
    return jsonify({"status": "cinta detenida"})


@app.route("/get_position", methods=["GET"])
def get_position():
    posicion = niryo.get_pose()
    return jsonify(posicion)

@app.route("/paletizadas", methods=["POST"])
def paletizadas():
    # Aquí podrías llevar un contador real
    niryo.piezas_contadas += 1
    return jsonify({"piezas": niryo.piezas_contadas})


@app.route("/move", methods=["POST"])
def move_robot():
    data = request.json # Recibimos el objeto enviado desde JS
    
    x = data.get("x")
    y = data.get("y")
    z = data.get("z")
    roll = data.get("roll")
    pitch = data.get("pitch")
    yaw = data.get("yaw")
    
    
    threading.Thread(target=niryo.move_pose, args=(x, y, z, roll, pitch, yaw)).start()
    
    return jsonify({"status": "movimiento iniciado"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)