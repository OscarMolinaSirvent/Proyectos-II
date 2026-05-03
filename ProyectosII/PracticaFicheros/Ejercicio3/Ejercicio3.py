dato = input("Pulsa una tecla: ")
with open("Ejercicio3/Datos.txt", "a") as file:
    file.write(f"{dato}\n")
