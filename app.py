from typing import List
from flask.helpers import make_response
from werkzeug.wrappers import response
from werkzeug.security import generate_password_hash, check_password_hash
import yagmail as yagmail
from flask import Flask, render_template, flash, request, redirect, session
import utilidades, datosUsuarios, os, datosCitas, datosMedicos
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'username' in session:
        session.clear()
    response = make_response(render_template('LoginModo.html'))
    response.set_cookie("custome_cookie","")
    datosMedicos.crearTabla(datosMedicos.conectarse())
    return response

@app.route('/login-paciente')
def logpac():
    return render_template('/LoginPacientes.html')

@app.route('/login-medicos')
def logmed():
    return render_template('/LoginMedicos.html')

@app.route('/contactanos')
def acerca():
    return render_template('About.html')

@app.route('/log-medicos', methods=('GET','POST'))
def loginmedicos():
    try:
        if request.method=='POST':
            user = request.form['username']
            password = request.form['password']            
            
            if datosMedicos.validarUsuario(datosMedicos.conectarse(),user):
                datos = datosMedicos.devolverUsuario(datosMedicos.conectarse(),user)
                #print(datos)
                for row in datos:
                    print("User: ",row[0],"Clave: ",row[1])
                    if(str(row[0])==str(user) and check_password_hash(row[1],password)):
                        session.clear()
                        session['username']=user
                        session['password']=row[1]
                        session['opcion']="Login success"
                        response = make_response(redirect('/Pacientes-Medicos'))
                        response.set_cookie("custome_cookie",str(row[0]))
                        return response
                    else:
                        error = "Datos incorrectos, intentalo de nuevo"
                        flash(error)
                        print("Error!")
                        error=""
                        return redirect('/login-medicos')      
            else:
                error = "El usuario no existe"
                flash(error)
                print("Error!")
                error=""
                return redirect('/')
                       
    except ValueError:
        print('error',ValueError)
        return render_template('Login.html')
    

@app.route('/log-paciente', methods=('GET','POST'))
def loginpaciente():
    try:
        if request.method=='POST':
            user = request.form['username']
            password = request.form['password']            
            
            if datosUsuarios.validarUsuario(datosUsuarios.conectarse(),user):
                datos = datosUsuarios.devolverUsuario(datosUsuarios.conectarse(),user)
                #print(datos)
                for row in datos:
                    #print("User: ",row[0],"Clave: ",row[1])
                    if(str(row[0])==str(user) and check_password_hash(row[1],password)):
                        session.clear()
                        session['username']=user
                        session['password']=row[1]
                        session['opcion']="Login success"
                        response = make_response(redirect('/Pacientes'), )
                        response.set_cookie("custome_cookie",str(row[0]))
                        return response
                    else:
                        error = "Datos incorrectos, intentalo de nuevo"
                        flash(error)
                        print("Error!")
                        error=""
                        return redirect('/login-paciente')      
            
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
            clave = generate_password_hash(request.form['passReg'])             
            datos ="("+doc+",'"+nom+"','"+ape+"','"+tipo+"','"+clave+"','"+corr+"','"+request.form['userTipe']+"')"
            
            if(request.form['userTipe']=='Medico'):
                if(not datosMedicos.validarUsuario(datosMedicos.conectarse(),doc)):
                    val = datosMedicos.registrarUsuario(datosUsuarios.conectarse(),datos)  
                    datosUsuarios.conectarse().close()                    
                    error = "Usuario registrado"
                else: 
                    error = "El usuario "+doc+" ya se encuentra en la base de datos"
                    val = False
            elif(request.form['userTipe']=='Paciente'):
                
                if(not datosUsuarios.validarUsuario(datosUsuarios.conectarse(),doc)):
                    val = datosUsuarios.registrarUsuario(datosUsuarios.conectarse(),datos)  
                    datosUsuarios.conectarse().close()                    
                    error = "Usuario registrado"
                else:
                    print(datos)
                    error = "El usuario "+doc+" ya se encuentra en la base de datos"
                    val= False
        except:
            flash(error)
            print("Error!")
            return redirect('/registro')     
        finally:
            if val:
                flash(error)
                print("usuario registrado!")   
                error=None                 
                return redirect("/")
            else:
                print("Error de datos")                
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
    return render_template('Pacientes/registro.html')

@app.route('/solicitarcita')
def solicitudcita():
    devolverMed = datosMedicos.devolverMedicos(datosMedicos.conectarse())
    fechaActual = datetime.today().strftime('%Y-%m-%d')
    print(fechaActual)
    return render_template('Pacientes/SolicitarCitas/solicitarcita.html', datoMedic = devolverMed, fecha = fechaActual)

@app.route('/solicitarcita/apartarcita', methods=['GET','POST'])
def apartarcita():
    val = False
    if request.method=='POST':
        try:
            datosCitas.crearTabla(datosCitas.conectarse())
            nom =request.form['name']            
            doc = request.cookies['custome_cookie']
            tipoCita = request.form['tipoCita']
            fechaCita = request.form['fechaCita']
            fechaCre = datetime.today().strftime('%Y-%m-%d')
            print(fechaCre)
            med = request.form['medico']
            cel = request.form['celCita']
            agg = request.form['mensajeCita']            
            datos ="('"+nom+"',"+doc+",'"+tipoCita+"','"+fechaCita+"','"+fechaCre+"','"+cel+"','"+agg+"','"+med+"')"
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
                return render_template("Pacientes/SolicitarCitas/detallesdelacita.html",paciente=nom,tipoCita=tipoCita,FechaCita=fechaCita,Lugar="Sincelejo, Sucre",medico="Juan Lazarte",id=doc,EPS="Nueva EPS",cit="null")
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
    citas = list()
    medicos = list()
    vec = list()
    max = len(salidas)
    min = len(salidas) - 11
    cont = 0
    print(len(salidas)-10)
    if(max > 10):
        for a in range(len(salidas)):            
            if(cont > min and cont < max):
                citas.append(salidas[cont])
                #limite.add(salidas[cont])
            cont += 1
    else:
        for a in range(len(salidas)):            
            citas.append(salidas[cont])
            cont = cont + 1
    for a in citas:
        print(a[8])
        vec.append(datosMedicos.datosPerfil(datosMedicos.conectarse(),a[8]))
    print(vec)
    for e in vec:
        cont += 1
        
        print(e)
        for i in e:
            nom = str(i[1]) +" "+str(i[2]) 
            medicos.append(nom)
            nom= ""
    
    return render_template('Pacientes/SolicitarCitas/vercitas.html', citas=citas, medicos=medicos)

@app.route('/Inicio-Medicos')
def indexMedicos():
    return render_template('Doctores/index.html')

@app.route('/Pacientes-Medicos')
def PacientesMedicos():
    return render_template('Doctores/index.html')

@app.route('/Perfil-Medico')
def PerfilMedico():
    return render_template('Doctores/index.html')

@app.route('/Agenda-Medica')
def AgendaMedico():
    print(request.cookies.get("custome_cookie"))
    citas = list(datosCitas.obtenerCitasMed(datosCitas.conectarse(),request.cookies.get("custome_cookie")))
    return render_template('Doctores/Listadecitas.html',citas = citas)

@app.route('/Historia-Medica')
def HistoriaMedica():
    return render_template('Doctores/Historias-Medicas.html')


if __name__=='__main__':
    app.run(debug=True)

    