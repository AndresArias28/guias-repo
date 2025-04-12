from flask import request, jsonify, render_template, session, flash, redirect
from app import app
from models.instructores import Instructores
import yagmail
import threading
from app import recaptcha
import requests
import random
import string

email = yagmail.SMTP('santo2828@gmail.com','yoqdygtmnxvptnjn',encoding='utf-8')

@app.route("/instructores")
def get_instructores():
    try:
        instructores = Instructores.objects()
        return jsonify(instructores), 200
    except Exception as e:
        print("Error al obtener los instructores:", e)
        return jsonify({"error": "Error al obtener los instructores"}), 500

def enviarCorreo(destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=mensaje)
    

@app.route("/instructorRegister", methods=["POST"])
def create_instructor():
    try:
        nombre = request.form.get("nombre")
        password = request.form.get("password")
        email = request.form.get("email")
        regional = request.form.get("regional")
        
        if not all([nombre, password, email, regional]):
            return jsonify({"message": "Faltan datos"}), 400
        
        instruc = Instructores(
            nombre=nombre,
            password=password,
            email=email,
            regional=regional
        )
        
        instruc.save()

        print("correo", email)
        print("password", password)

        mensaje = f'Hola, has hecho el registro en la aplicación. Este es el reporte de tus datos: correo: {email}, password: {password}'
        destinatarios = [email, "andresan0328@gmail.com"]

        hilo = threading.Thread(target=enviarCorreo, args=(destinatarios, 'Registro exitoso', mensaje))
        hilo.start()

        flash('Instructor registrado exitosamente.', 'success')
        return render_template('login.html'), 200
    except Exception as e:
        print("Error al crear el instructor:", e)
        return jsonify({"error": "Error al crear el instructor"}), 500

@app.route("/instructorLogin", methods=["POST"])
def login_instructor():
    try:
        data = request.get_json(force=True)
        correo=data.get("email")
        passw=data.get("password")
        instructor = Instructores.objects(email=correo).first()
        
        if not instructor:
            return jsonify({"message": "Correo no registrado"}), 404
        
        if instructor.password != passw:
            return jsonify({"message": "Contraseña incorrecta"}), 401
        #sesion y correo
        session["id"] = str(instructor.id)
        session["email"] = instructor.email
        session["nombre"] = instructor.nombre
        session["password"] = instructor.password
        session["autenticado"] = True
        print("Instructor encontrado:", instructor)
        print("Correo:", instructor.email)
        return jsonify({"message": "Login exitoso"}), 200
    except Exception as e:
        print("Error al iniciar sesion:", e)
        return jsonify({"error": "Error al inicio de sesion"}), 500
    

@app.route('/usuarios/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Sesión cerrada"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@app.route('/loginVista', methods=['GET'])
def loginVista():
    try:
        return render_template('login.html'), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

  
@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/dash')
def dash():
    return render_template('content.html')