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

def obtener_logs(conexion, elemento=None):
    try:
        cursor = conexion.cursor()
        if elemento == "Movimiento":
            sql = """
            SELECT fecha_hora, elemento, instruccion
            FROM logs
            WHERE elemento = 'Movimientos'
            ORDER BY fecha_hora DESC
            """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    except Exception as e:
        print("Error al consultar logs:", e)
        return []