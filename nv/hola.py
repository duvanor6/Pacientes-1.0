from flask import Flask
app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return "Hola mundo!"

@app.route('/ruta2')
def ruta2():
    a = 10
    b = 20
    suma = a + b 
    re = "Estamos en la ruta 2 " + str(suma)
    return re

@app.route('/ruta2/ruta3')
def ruta3():
    return "Estamos en la ruta 3"

if __name__=="__main__":
    app.run()