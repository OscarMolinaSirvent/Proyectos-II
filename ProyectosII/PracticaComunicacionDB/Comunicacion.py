import oracledb
def conectar(usuario, password):
    try:
        conexion = oracledb.connect(
            user=usuario,
            password=password,
            dsn="oralabos.dsic.upv.es/labora.dsic.upv.es"
        )
        print("Conectado con éxito")
        return conexion
    except Exception as e:
        print("Error al conectar:", e)
        return None

def insertar_log(conexion, instruccion):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO LOGS (INSTRUCCION) VALUES (:1)"
        cursor.execute(sql, [instruccion])
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al insertar:", e)

  