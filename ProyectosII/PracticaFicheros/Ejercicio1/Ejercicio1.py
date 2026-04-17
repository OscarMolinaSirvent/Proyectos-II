import keyboard
import threading
import time
import logging
tecla_x = False
tecla_y = False

def fun():
    global tecla_y,tecla_x
    while True:
        tecla = keyboard.read_key()
        if tecla == 'x':
            tecla_x = True
            break
        elif tecla == 'y':
            tecla_y = True
            break


def main():
    global tecla_x, tecla_y
    logging.basicConfig(level=logging.INFO)
    x1 = threading.Thread(target=fun, args=())
    x1.start()

    while True:
        time.sleep(0.1)
        if not x1.is_alive():
            break

    ruta = "Ejercicio1.txt"
    numero = 0
    if tecla_x == True:
        logging.info("Dentro")
        try:
            with open(ruta, "r") as f:
                contenido = f.readline().strip()
                if contenido:
                    numero = int(contenido)
                    numero += 1
        except FileNotFoundError:
            print("El archivo no existe.")

        try:
            with open(ruta, "w") as f:
                f.write(str(numero))

        except FileNotFoundError:
            print("El archivo no existe.")
            
    elif tecla_y == True:
        try:
            with open("Alarma.txt", "a") as f:
                f.write("1")
        except FileNotFoundError:
                print("El archivo no existe.")        

if __name__ == "__main__":
    main()