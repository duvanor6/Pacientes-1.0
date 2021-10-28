import sqlite3

def conectarse():
    try:
        con = sqlite3.connect('dbmedicos.db')
        print("conectados a dbmedicos")
        return con
    except:
        print("No se pudo conectar con dbmedicos")

def crearTabla(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('CREATE TABLE if not exists medicos (cedula integer PRIMARY KEY, nombre text, apellido text, tipo_documento text, clave text, correo text)')
        con.commit()
        con.close()
        print("Tabla creada")
    except:
        print("No se pudo crear la tabla citas")