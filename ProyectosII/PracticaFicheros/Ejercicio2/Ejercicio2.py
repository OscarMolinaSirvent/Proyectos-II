
import logging

logging.basicConfig(level=logging.INFO)
maquina = True

def leer_estado():
    global maquina
    try:
        with open("Ejercicio2/estado.txt", "r") as f:
            estado = f.readline().strip()
            if estado == "1" and maquina == False:
                maquina = True
                print("Ejercicio2/estado.txt")
            elif estado == "0" and maquina == True:
                maquina = False
                print("Apagando maquina")

            
    except FileNotFoundError:
                print("El archivo no existe.")
                
if __name__ == "__main__":
    leer_estado()
