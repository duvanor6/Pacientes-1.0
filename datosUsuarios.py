import sqlite3
from sqlite3.dbapi2 import Cursor

def conectarse():
    try:
        con = sqlite3.connect('usuarios.db')
        print("conectados")
        return con
    except:
        print("No se pudo conectar")



def crearTabla(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('CREATE TABLE if not exists pacientes (cedula integer PRIMARY KEY, nombre text, apellido text, tipo_documento text, clave text, correo text)')
        con.commit()
        con.close()
        print("Tabla creada")
    except:
        print("No se pudo crear la tabla")

def registrarUsuario(con, datos):
    valor = False
    try:
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO pacientes (cedula, nombre, apellido, tipo_documento, clave, correo) VALUES'+datos)
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
        cursorObj.execute("SELECT cedula FROM pacientes WHERE cedula = '"+cedula+"'")  
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
        cursorObj.execute("SELECT cedula, clave FROM pacientes WHERE cedula = '"+cedula+"'")
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
        cursorObj.execute("SELECT * FROM pacientes WHERE cedula = '"+cedula+"'")
        result = cursorObj.fetchall()
        con.close()
        return result
    except ValueError:
        print("No se encontró")
        return None
        