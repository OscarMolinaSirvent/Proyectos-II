from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import niryo_logic as niryo

app = Flask(__name__)
CORS(app)

@app.route("/get_position", methods=["GET"])
def get_position():
    return jsonify(niryo.get_pose())

@app.route("/move", methods=["POST"])
def move_robot():
    data = request.json
    threading.Thread(target=niryo.move_joints, args=(
        data['j1'], data['j2'], data['j3'], 
        data['j4'], data['j5'], data['j6']
    )).start()
    return jsonify({"status": "ok"})

@app.route("/run_auto", methods=["POST"])
def run_auto():
    threading.Thread(target=niryo.secuencia_automatica).start()
    return jsonify({"status": "running"})

@app.route("/stop", methods=["POST"])
def stop():
    niryo.stop_all()
    return jsonify({"status": "stopped"})

@app.route("/startCinta", methods=["POST"])
def start_cinta():
    niryo.run_conv()
    return jsonify({"status": "ok"})

@app.route("/stopCinta", methods=["POST"])
def stop_cinta():
    niryo.stop_conv()
    return jsonify({"status": "ok"})

@app.route("/gripper/open", methods=["POST"])
def open_g():
    niryo.control_gripper(True)
    return jsonify({"status": "ok"})

@app.route("/gripper/close", methods=["POST"])
def close_g():
    niryo.control_gripper(False)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)