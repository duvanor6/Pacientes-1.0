import sqlite3

def conectarse():
    try:
        con = sqlite3.connect('db.db')
        #print("conectados a citas")
        return con
    except:
        print("No se pudo conectar con citas")

def crearTabla(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('CREATE TABLE if not exists citas (id integer PRIMARY KEY AUTOINCREMENT, nombre text, documento integer, tipo_cita text, fecha_cita date, fecha_creacion date, celular text, agregado real, medico text)')
        con.commit()
        con.close()
        #print("Tabla creada para citas")
    except:
        print("No se pudo crear la tabla citas")


def registrarCita(con, datos):
    valor = False
    try:
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO citas (nombre, documento, tipo_cita, fecha_cita, fecha_creacion,celular, agregado, medico) VALUES'+datos)
        con.commit()
        cursorObj.close()
        con.close()
        valor = True
        return valor
    except ValueError:
        print(ValueError)
        valor = False
        return valor

def obtenerCitas(con, cedula):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM citas WHERE documento = '"+cedula+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        #print("No se encontró cita(s)")
        return None

def obtenerCitasMed(con, cedula):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM citas WHERE medico = '"+cedula+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        #print("No se encontró cita(s)")
        return None

def devolverCita(con, id):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM citas WHERE id = '"+id+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        #print("No se encontró")
        return None

def eliminarCita(con, id):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("DELETE FROM citas WHERE id = '"+id+"'")
        con.commit()
        cursorObj.close()
        return True
    except:
        return False

def validarCita(con, id):    
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT id FROM citas WHERE id = '"+id+"'")  
        registro = cursorObj.fetchall()
        print(registro)
        if registro != []:
            con.close()  
            #print("True cita")      
            return True
        else:
            con.close()
            #print("False cita")    
            return False
    except ValueError:
        #print("No se encontró")
        return False