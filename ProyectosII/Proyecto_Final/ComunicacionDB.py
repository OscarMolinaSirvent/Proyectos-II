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

def insertar_log(conexion, instruccion, elemento):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO LOGS (INSTRUCCION, ELEMENTO) VALUES (:1, :2)"
        cursor.execute(sql, [instruccion, elemento])
        conexion.commit()
        cursor.close()
        print("¡Log guardado en el historial!")
    except Exception as e:
        print("Error en LOGS:", e)

def modificar_cinta(conexion, id_componente, nueva_velocidad, nueva_direccion, nuevo_estado):
    try:
        cursor = conexion.cursor()
        
        sql = """
            UPDATE CINTAS 
            SET VELOCIDAD = :1, 
                DIRECCION = :2, 
                ESTADO = :3, 
                FECHA_CINTAS = SYSDATE 
            WHERE ID_COMPONENTE = :4
        """
        cursor.execute(sql, [nueva_velocidad, nueva_direccion, nuevo_estado, id_componente])
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"¡Éxito! Cinta {id_componente} actualizada (Datos y Fecha modificados).")
        else:
            print(f"Advertencia: No se encontró ninguna cinta con el ID {id_componente}.")
            
        cursor.close()
    except Exception as e:
        print("Error al intentar modificar la cinta:", e)

def insertar_comando(conexion, nombre_accion, valor, tipo, eje1_6, id_robot):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO COMANDOS (NOMBRE_ACCION, VALOR, TIPO, EJE1_6, ID_ROBOT) VALUES (:1, :2, :3, :4, :5)"
        cursor.execute(sql, [nombre_accion, valor, tipo, eje1_6, id_robot])
        conexion.commit()
        cursor.close()
        print("¡Comando registrado con éxito!")
    except Exception as e:
        print("Error en COMANDOS:", e)

def modificar_ocupado(conexion, id_tablero, identificador_casilla, nuevo_estado):
    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE OCUPADOS 
            SET ESTADO = :1, 
                FECHA_OCUPADOS = SYSDATE 
            WHERE ID_TABLERO = :2 
              AND IDENTIFICADOR = :3
        """

        cursor.execute(sql, [nuevo_estado, id_tablero, identificador_casilla])
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"¡Éxito! Casilla {identificador_casilla} del Tablero {id_tablero} actualizada a '{nuevo_estado}'.")
        else:
            print(f"Advertencia: No se encontró la casilla {identificador_casilla} en el tablero {id_tablero}.")
            
        cursor.close()
    except Exception as e:
        print("Error al intentar modificar el registro en OCUPADOS:", e)


def modificar_sensor(conexion, id_componente, nuevo_tipo, nuevo_estado):
    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE SENSORES 
            SET TIPO = :1, 
                ESTADO = :2, 
                FECHA_SENSORES = SYSDATE 
            WHERE ID_COMPONENTE = :3
        """
        
        cursor.execute(sql, [nuevo_tipo, nuevo_estado, id_componente])
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"¡Éxito! Sensor {id_componente} actualizado (Tipo: {nuevo_tipo}, Estado: {nuevo_estado}).")
        else:
            print(f"Advertencia: No se encontró ningún sensor con el ID {id_componente}.")
            
        cursor.close()
    except Exception as e:
        print("Error al intentar modificar el sensor:", e)

def modificar_pinza(conexion, id_componente, nuevo_estado):
    try:
        cursor = conexion.cursor()
        sql = """
            UPDATE PINZAS 
            SET ESTADO = :1, 
                FECHA_PINZA = SYSDATE 
            WHERE ID_COMPONENTE = :2
        """
        
        cursor.execute(sql, [nuevo_estado, id_componente])
        conexion.commit()
        
        if cursor.rowcount > 0:
            print(f"¡Éxito! Pinza {id_componente} actualizada a '{nuevo_estado}' (Fecha renovada).")
        else:
            print(f"Advertencia: No se encontró ninguna pinza con el ID {id_componente}.")
            
        cursor.close()
    except Exception as e:
        print("Error al intentar modificar la pinza:", e)

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
        if elemento == "Sensor":
            sql = """
            SELECT fecha_hora, elemento, instruccion
            FROM logs
            WHERE ELEMENTO = 'Sensor'
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