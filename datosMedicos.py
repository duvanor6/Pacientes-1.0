import sqlite3

def conectarse():
    try:
        con = sqlite3.connect('db.db')
        print("conectados a dbmedicos")
        return con
    except:
        print("No se pudo conectar con dbmedicos")

def crearTabla(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('CREATE TABLE if not exists medicos (cedula integer PRIMARY KEY, nombre text, apellido text, tipo_documento text, clave text, correo text, userTip text)')
        con.commit()
        con.close()
        print("Tabla creada")
    except:
        print("No se pudo crear la tabla citas")

def registrarUsuario(con, datos):
    valor = False
    try:
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO medicos (cedula, nombre, apellido, tipo_documento, clave, correo, userTip) VALUES'+datos)
        con.commit()
        cursorObj.close()
        con.close()
        valor = True
        return valor
    except:
        print('Error al registrar datos: ')
        valor = False
        return valor

def validarUsuario(con, cedula):    
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT cedula FROM medicos WHERE cedula = '"+cedula+"'")  
        registro = cursorObj.fetchall()
        print(registro)

        if registro != []:
            con.close()  
            print("True user")      
            return True
        else:
            con.close()
            print("False user")    
            return False
    except ValueError:
        print("No se encontró")
        return False

def devolverUsuario(con, cedula):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT cedula, clave FROM medicos WHERE cedula = '"+cedula+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        print("No se encontró")
        return None

def devolverMedicos(con):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM medicos ")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        print("No se encontró")
        return None

def datosPerfil(con, cedula):
    result = None
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM medicos WHERE cedula = '"+cedula+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        print("No se encontró")
        return None
        