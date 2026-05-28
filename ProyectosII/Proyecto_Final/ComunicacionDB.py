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

def insertar_log(conexion, instruccion): # Inserta en la BD LOG
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO LOGS (INSTRUCCION) VALUES (:1)"
        cursor.execute(sql, [instruccion])
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al insertar:", e)

def insertar_cinta(conexion, velocidad, direccion, estado):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO CINTAS (VELOCIDAD, DIRECCION, ESTADO) VALUES (:1, :2, :3)"
        cursor.execute(sql, [velocidad, direccion, estado])
        conexion.commit()
        cursor.close()
        print("¡Registro insertado con éxito!")
    except Exception as e:
        print("Error al insertar en la tabla CINTAS:", e)

def actualizar_estado_robot(conexion, id_robot, nuevo_estado):

    try:
        cursor = conexion.cursor()
        # Sentencia SQL usando marcadores de posición para evitar inyección SQL
        sql = "UPDATE ROBOTS SET ESTADO = :1 WHERE ID = :2"
        
        cursor.execute(sql, [nuevo_estado, id_robot])
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al intentar actualizar el estado del robot:", e)

def obtener_logs(conexion, elemento=None):
    try:
        cursor = conexion.cursor() 
        if elemento == "Movimiento": #Filtrado por Elemento
            sql = """
            SELECT fecha_hora, elemento, instruccion
            FROM logs
            WHERE ELEMENTO = 'Movimiento'
            ORDER BY fecha_hora DESC
            """

        if elemento == "Cinta":
            sql = """
            SELECT fecha_hora, elemento, instruccion
            FROM logs
            WHERE ELEMENTO = 'Cinta'
            ORDER BY fecha_hora DESC
            """
        
        if elemento == "Herramienta":
            sql = """
            SELECT fecha_hora, elemento, instruccion
            FROM logs
            WHERE ELEMENTO = 'Herramienta'
            ORDER BY fecha_hora DESC
            """
            
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    
    except Exception as e:
        print("Error al consultar logs:", e)
        return []
    
def verificar_credenciales(conexion, nombre, password):
    try:
        cursor = conexion.cursor()
        # Consulta basada en la estructura de tu tabla USUARIOS
        sql = "SELECT TIPO FROM USUARIOS WHERE NOMBRE = :1 AND PASSWORD = :2"
        cursor.execute(sql, [nombre, password])
        resultado = cursor.fetchone()
        cursor.close()
        
        if resultado:
            return resultado[0]  #ADMIN O OPERARIO
        return None
    except Exception as e:
        print(f"Error en la verificación: {e}")
        return None