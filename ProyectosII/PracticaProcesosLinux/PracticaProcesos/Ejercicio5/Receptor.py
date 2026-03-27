import csv
import socket

HOST = '127.0.0.2'
PORT = 65432
def receptor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST,PORT))
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        conn,adrr = servidor.accept()

        with conn:
            print(f"Conectado por: {adrr}")
            while True:
                datos = conn.recv(1024)
                if not datos:
                    break
                
                mensaje = datos.decode('utf-8')
                print(f"Mensaje recibido: {mensaje}")
                with open('Ejercicio5/table.csv', 'a', newline='') as file:
                    spamwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([mensaje])
                print("Mensaje guardado en table.csv")