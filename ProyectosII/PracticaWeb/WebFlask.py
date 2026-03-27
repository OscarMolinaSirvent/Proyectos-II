from flask import Flask, jsonify
from PickAndPlace import main #Método main del script prova

app = Flask(__name__) # Crear instancia de la aplicación Flask

@app.route("/") #El endpoint “/” muestra este mensaje
def home():
    return "API funcionando"

@app.route("/run_main", methods=["POST"]) #Endpoint “/run_main” que ejecuta main()
def run_main():
    main() #Llama al método “main”
    return jsonify({"status": "finished"}) #Lo devuelve al finalizar

@app.route("/stop_main", methods=["POST"]) #Endpoint “/stop_main” que detiene main()
def stop_main():
    return jsonify({"status": "stopped"}) #Lo devuelve al finalizar

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)