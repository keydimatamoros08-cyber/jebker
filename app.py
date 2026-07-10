from flask import Flask, render_template, request, redirect
def responder(mensaje):
    return "Hola, Soy jebker. Aun estoy configurandome. Enqe te ayudo?"
import sqlite3


app = Flask(__name__)


# CREAR BASE DE DATOS
def crear_bd():

    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    conexion.commit()
    conexion.close()



# LOGIN
@app.route("/")
def login():

    return render_template("login.html")



# REGISTRO
@app.route("/registro")
def registro():

    return render_template("registro.html")



@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form["nombre"]
    usuario = request.form["usuario"]
    password = request.form["password"]


    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()


    try:

        cursor.execute(
            "INSERT INTO usuarios(nombre,usuario,password) VALUES(?,?,?)",
            (nombre, usuario, password)
        )


        conexion.commit()


    except:

        conexion.close()

        return "Ese usuario ya existe."


    conexion.close()


    return redirect("/")





# INICIAR SESIÓN
@app.route("/entrar", methods=["POST"])
def entrar():


    usuario = request.form["usuario"]

    password = request.form["password"]


    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()



    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (usuario, password)
    )


    dato = cursor.fetchone()


    conexion.close()



    if dato:

        return redirect("/inicio")



    return "Usuario o contraseña incorrectos."






# PÁGINA PRINCIPAL
@app.route("/inicio")
def inicio():

    return render_template("index.html")





# CHAT
@app.route("/chat")
def chat():

    return render_template("chat.html")





# RESPUESTAS IA
@app.route("/mensaje", methods=["POST"])
def mensaje():


    texto = request.form["mensaje"]


    respuesta = responder(texto)


    return respuesta






if __name__ == "__main__":


    crear_bd()


    app.run(
        host="0.0.0.0",
        port=5000
    )
