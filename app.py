from typing import List
from flask.helpers import make_response
from werkzeug.wrappers import response
import yagmail as yagmail
from flask import Flask, render_template, flash, request, redirect, url_for
import utilidades, datosUsuarios, os, datosCitas, datosMedicos
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    datosMedicos.crearTabla(datosMedicos.conectarse())
    return render_template('Login.html')

@app.route('/login', methods=('GET','POST'))
def login():
    try:
        if request.method=='POST':
            user = request.form['username']
            password = request.form['password']            

            if datosUsuarios.validarUsuario(datosUsuarios.conectarse(),user):
                datos = datosUsuarios.devolverUsuario(datosUsuarios.conectarse(),user)
                print(datos)
                for row in datos:
                    print("User: ",row[0],"Clave: ",row[1])
                    if(str(row[0])==str(user) and row[1]==password):
                        response = make_response(render_template("pacientes/Citas.html"))
                        response.set_cookie("custome_cookie",str(row[0]))
                        return response
                    else:
                        error = "Datos incorrectos, intentalo de nuevo"
                        flash(error)
                        print("Error!")
                        error=""
                        return redirect('/')      
            elif(user=="Medico" or user=="medico"):
                #error = "Datos incorrectos"
                #flash(error)
                #print("Error!")
                #error=""
                return redirect('Inicio-Medicos') 
                       
    except ValueError:
        print('error',ValueError)
        return render_template('Login.html')

@app.route('/eliminar-cita+<int:id>')
def eliminarcita(id):
    if(datosCitas.validarCita(datosCitas.conectarse(),str(id))):
        if(datosCitas.eliminarCita(datosCitas.conectarse(),str(id))):
            succes = "Se eliminó correctamente"
            flash(succes)
            succes = ""
            return redirect("/vercitas")
        else:
            error = "Error al intentar eliminar"
            flash(error)
            print("Error!")
            error= ""
            return redirect("/vercitas")
    else:
        return print("Esta cita no existe")
    

@app.route('/registrarse', methods=['GET','POST'])
def registrarse():
    val = False
    error = ""
    if request.method=='POST':    
        try:         
            datosUsuarios.crearTabla(datosUsuarios.conectarse())
            nom = request.form['nomReg']
            ape = request.form['apellidoReg']
            tipo = request.form['docTipe']
            doc = request.form['docReg']
            corr =request.form['emailReg']
            clave = request.form['passReg']            
            datos ="("+doc+",'"+nom+"','"+ape+"','"+tipo+"','"+clave+"','"+corr+"')"
            #print(datos)
            val = datosUsuarios.registrarUsuario(datosUsuarios.conectarse(),datos)  
            datosUsuarios.conectarse().close()

        except:
            error = "Error al intentar registrar"
            flash(error)
            print("Error!")
            error=None
            return redirect('/registro')     
        finally:
            if val:
                error = "Usuario registrado"
                flash(error)
                print("usuario registrado!")   
                error=None                 
                return redirect("/")
            else:
                print("Error de datos")
                error = "No se pudo regitrar el usuario,verifique los datos"
                flash(error)
                error=None
                return redirect("/registro")

@app.route('/Detalles-cita/<int:idcita>', )
def detallescita(idcita):
    if(datosCitas.validarCita(datosCitas.conectarse(),str(idcita))):
        citas = datosCitas.devolverCita(datosCitas.conectarse(),str(idcita))
        print(citas[0])
        return render_template("Pacientes/SolicitarCitas/detallesdelacita.html",paciente=citas[0][1],tipoCita=citas[0][4],FechaCita=citas[0][5],Lugar="Sincelejo, Sucre",medico="Juan Lazarte",id=citas[0][0],EPS="Nueva EPS",cit=citas[0][0])
    else:
        return print("Esta cita no existe")
    
@app.route('/registro')
def registro():
    return render_template('pacientes/registro.html')

@app.route('/solicitarcita')
def solicitudcita():
    return render_template('Pacientes/SolicitarCitas/solicitarcita.html')

@app.route('/solicitarcita/apartarcita', methods=['GET','POST'])
def apartarcita():
    val = False
    if request.method=='POST':
        try:
            datosCitas.crearTabla(datosCitas.conectarse())
            nom =request.form['name']
            
            mail = request.form['emailCita']
            tipdoc = request.form['tipodocCita']
            doc = request.form['docCita']
            tipoCita = request.form['tipoCita']
            fechaCita = request.form['fechaCita']
            fechaCre = datetime.today().strftime('%Y-%m-%d')
            print(fechaCre)
            cel = request.form['celCita']
            agg = request.form['mensajeCita']            
            datos ="('"+nom+"',"+doc+",'"+tipdoc+"','"+tipoCita+"','"+fechaCita+"','"+fechaCre+"','"+cel+"','"+agg+"')"
            print(datos)
            val = datosCitas.registrarCita(datosCitas.conectarse(),datos)

        except ValueError:
            error = "Error al intentar apartar la cita"
            flash(error)
            print("Error!",ValueError)
            error=None
            return redirect('/solicitarcita')     
        finally:
            if val:
                error = "Cita apartada con exito!"
                flash(error)
                print("Cita apartada con exito!")   
                error=None               
                return render_template("Pacientes/SolicitarCitas/detallesdelacita.html",paciente=nom,tipoCita=tipoCita,FechaCita=fechaCita,Lugar="Sincelejo, Sucre",medico="Juan Lazarte",id=doc,EPS="Nueva EPS",cit=citas[0][0])
            else:
                print("Error de datos")
                error = "No se pudo apartar la cita, verifique los datos"
                flash(error)
                error=None
                return redirect("/solicitarcita")


@app.route('/Historias')
def historias():
    return render_template('Historias.html')

@app.route('/Contactenos')
def contacto():
    return render_template('Pacientes/Contactenos.html')


@app.route('/Pacientes')
def paciente():
    return render_template('Pacientes/Citas.html')

@app.route('/Medicos')
def medicos():
    return render_template('Pacientes/Medicos.html')

@app.route('/Perfil')
def perfil():
    doc = request.cookies.get("custome_cookie")
    perfil = datosUsuarios.datosPerfil(datosUsuarios.conectarse(),doc)
    for row in perfil:
        nombreC = row[1] +" " +row[2]
        cc = row[0]
        mail = row[5]
    return render_template('Pacientes/Perfil.html', nombre=nombreC, cedula = cc, email=mail,eps="Nueva Eps",fecha="17 de Junio de 1997")

@app.route('/historiasMedicas')
def historiasMedicas():
    return render_template('Pacientes/SolicitarCitas/historiasMedicas.html')

@app.route('/vercitas')
def vercitas():
    doc =request.cookies.get("custome_cookie")
    salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    limite = list()
    max = len(salidas)
    min = len(salidas) - 11
    cont = 0
    print(len(salidas)-10)
    for a in range(len(salidas)):
        cont += 1
        if(cont > min and cont < max):
            limite.append(salidas[cont])
            #limite.add(salidas[cont])
    return render_template('Pacientes/SolicitarCitas/vercitas.html', citas=limite)

@app.route('/Inicio-Medicos')
def indexMedicos():
    #doc =request.cookies.get("custome_cookie")
    #salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    return render_template('Doctores/index.html')

@app.route('/Pacientes-Medicos')
def PacientesMedicos():
    #doc =request.cookies.get("custome_cookie")
    #salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    return render_template('Doctores/index.html')

@app.route('/Perfil-Medico')
def PerfilMedico():
    #doc =request.cookies.get("custome_cookie")
    #salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    return render_template('Doctores/index.html')

@app.route('/Agenda-Medica')
def AgendaMedico():
    #doc =request.cookies.get("custome_cookie")
    #salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    return render_template('Doctores/Listadecitas.html')

@app.route('/Historia-Medica')
def HistoriaMedica():
    #doc =request.cookies.get("custome_cookie")
    #salidas = list(datosCitas.obtenerCitas(datosCitas.conectarse(),doc))
    return render_template('Doctores/Historias-Medicas.html')

# Modulo Principal
if __name__=='__main__':
    app.run(debug=True)

    