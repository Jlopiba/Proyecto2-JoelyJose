import mysql.connector
import uuid

def init():
    con = mysql.connector.connect(user="root", password="root", host="localhost")
    cur = con.cursor()
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS robot")
        cur.execute("USE robot")

        # Crear tablas
        cur.execute("CREATE TABLE IF NOT EXISTS robots(name CHAR(32))")
        cur.execute("CREATE TABLE IF NOT EXISTS medidas(name CHAR(32), ecinta BOOL, esensor BOOL, epinza BOOL)")
        cur.execute("CREATE TABLE IF NOT EXISTS comandos(instruccion CHAR(32), name CHAR(32))")
        cur.execute("CREATE TABLE IF NOT EXISTS parametros(instruccion CHAR(32), name CHAR(32), X FLOAT, Y FLOAT, Z FLOAT)")

        # Crear la tabla de historial
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historial(
                id INT AUTO_INCREMENT PRIMARY KEY,
                operacion VARCHAR(64),
                parametros TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("Base de datos y tablas creadas correctamente.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        con.close()

def agregar_a_historial(operacion, parametros):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"INSERT INTO historial (operacion, parametros) VALUES ('{operacion}', '{parametros}')")
        con.commit()
    except Exception as e:
        print("Error al agregar al historial:", e)
    finally:
        cur.close()
        con.close()

def addrobot(robot):
    if not robot: raise Exception("Missing user")
    if not "name" in robot: raise Exception("Missing name")
    
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"INSERT INTO robots VALUES('{robot['name']}')")
        cur.execute(f"INSERT INTO medidas (name, ecinta, esensor, epinza) VALUES ('{robot['name']}', 0, 0, 0)")
        con.commit()

        # Registrar la operación en el historial
        operacion = "Agregar robot"
        parametros = f"Nombre: {robot['name']}"
        agregar_a_historial(operacion, parametros)

    finally:
        con.close()

    return robot

def listrobots(query=""):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        robots = []
        cur = con.cursor()
        sql = "SELECT * FROM robots" + (" WHERE " + query if len(query) > 0 else "")
        cur.execute(sql)
        for row in cur.fetchall():
            user = {
                "name": row[0],
            }
            robots.append(user)
    finally:
        con.close()
    return robots   

def instruccion(instruccion, robot_name):
    if not instruccion or not robot_name:
        raise Exception("Missing instruction or robot name")
    
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"INSERT INTO comandos VALUES('{instruccion}', '{robot_name}')")
        con.commit()

        # Registrar la operación en el historial
        operacion = "Agregar instrucción"
        parametros = f"Instrucción: {instruccion}, Robot: {robot_name}"
        agregar_a_historial(operacion, parametros)

    finally:
        con.close()
    
    print(f"Instrucción '{instruccion}' añadida para el robot '{robot_name}'.")

def removerobot(robot_name):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()

        # Verificar si el robot existe antes de intentar eliminarlo
        cur.execute(f"SELECT name FROM robots WHERE name = '{robot_name}'")
        if cur.fetchone() is None:
            raise Exception(f"No se encontró el robot '{robot_name}'.")

        # Eliminar registros relacionados en la tabla 'comandos'
        cur.execute(f"DELETE FROM comandos WHERE name = '{robot_name}'")

        # Eliminar registros relacionados en la tabla 'medidas'
        cur.execute(f"DELETE FROM medidas WHERE name = '{robot_name}'")

        # Eliminar registros relacionados en la tabla 'parametros'
        cur.execute(f"DELETE FROM parametros WHERE name = '{robot_name}'")

        # Eliminar el robot de la tabla 'robots'
        cur.execute(f"DELETE FROM robots WHERE name = '{robot_name}'")

        con.commit()
        print(f"Robot '{robot_name}' y sus datos relacionados eliminados.")
    except Exception as e:
        print("Error al eliminar el robot:", e)
    finally:
        cur.close()
        con.close()

def instruccionrobot(instruccion, robot_name, x, y, z):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"INSERT INTO comandos VALUES('{instruccion}', '{robot_name}')")
        cur.execute(f"INSERT INTO parametros VALUES('{instruccion}', '{robot_name}', {x}, {y}, {z})")
        con.commit()

        # Registrar la operación en el historial
        operacion = "Instrucción con parámetros"
        parametros = f"Instrucción: {instruccion}, Robot: {robot_name}, Coordenadas: ({x}, {y}, {z})"
        agregar_a_historial(operacion, parametros)

        print(f"Instrucción '{instruccion}' para el robot '{robot_name}' y coordenadas ({x}, {y}, {z}) añadidas.")
    except Exception as e:
        print("Error al añadir la instrucción y coordenadas:", e)
    finally:
        cur.close()
        con.close()

def setmedidas(nombre, ecinta, esensor, epinza):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"UPDATE medidas SET ecinta = {ecinta}, esensor = {esensor}, epinza = {epinza} WHERE name = '{nombre}'")
        con.commit()

        # Registrar la operación en el historial
        operacion = "Actualizar medidas"
        parametros = f"Robot: {nombre}, Cinta: {ecinta}, Sensor: {esensor}, Pinza: {epinza}"
        agregar_a_historial(operacion, parametros)

        print(f"Medidas para el robot '{nombre}' actualizadas.")
    except Exception as e:
        print("Error al actualizar las medidas:", e)
    finally:
        cur.close()
        con.close()

def get_medidas(nombre):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT ecinta, esensor, epinza FROM medidas WHERE name = '{nombre}'")
        row = cur.fetchone()

        if row:
            return {
                "ecinta": row[0],
                "esensor": row[1],
                "epinza": row[2]
            }
        else:
            return None
    except Exception as e:
        print("Error al obtener las medidas:", e)
        return None
    finally:
        cur.close()
        con.close()

def get_instruccion(robot_name):
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        cur = con.cursor()
        cur.execute(f"SELECT instruccion FROM comandos WHERE name = '{robot_name}'")
        rows = cur.fetchall()

        if rows:
            return [row[0] for row in rows]  # Retorna una lista con todas las instrucciones del robot
        else:
            return []
    except Exception as e:
        print("Error al obtener las instrucciones:", e)
        return []
    finally:
        cur.close()
        con.close()

def get_historial():
    con = mysql.connector.connect(user="root", password="root", database="robot")
    try:
        historial = []
        cur = con.cursor()
        cur.execute("SELECT operacion, parametros, fecha FROM historial ORDER BY fecha DESC")
        for row in cur.fetchall():
            historial.append({
                "operacion": row[0],
                "parametros": row[1],
                "fecha": row[2]
            })
    finally:
        con.close()
    return historial

