import logging
import threading
import time 
import sys
import select


def esperar_tecla_con_timeout():
    print("Presiona una tecla (tienes 5 segundos):")
    i, _, _ = select.select([sys.stdin], [], [], 10)
    if i:
        tecla_presionada = sys.stdin.readline().strip()
        print(f"Tecla presionada: {tecla_presionada}")
        return tecla_presionada
    else:
        print("Se ha agotado el tiempo. No se presion´o ninguna tecla.")

#Programa principal. Llama al hilo y termina (sin esperar al hilo creado)
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

    logging.info("Main:     antes de crear el thread")
    x = threading.Thread(target=esperar_tecla_con_timeout,args=())
    logging.info("Main:     antes de ejecutar el thread")
    x.start()
    logging.info("Main:     esperando que termine el hilo")
    #si ponemos el join, el programa principal espera a que termien los threads, y el orden de la salida cambia
    x.join(timeout=5)
    if(x.is_alive()):
        logging.info("Main:  el hilo esta vivo")
    else:
        logging.info("Main: el hilo esta muerto")
    logging.info("Main:     todo realizado")