import os
from flask import request, jsonify, render_template, session, flash, redirect
from app import app
from models.guias import Guias
from models.instructores import Instructores
from app import login_requerido
from werkzeug.utils import secure_filename
from datetime import datetime

@app.route("/guias")
def get_guias():
    try:
        guias = Guias.objects()
        return jsonify(guias), 200
    except Exception as e:
        print("Error al obtener las guías:", e)
        return jsonify({"error": "Error al obtener las guías"}), 500


@app.route("/guiasRegister", methods=["POST"])
# @login_requerido
def create_guia():
    try:
        data = request.get_json(force=True)
        instructor = Instructores.objects(email=data.get("email")).first()
        print("Instructor encontrado:", instructor)
        if instructor is None:
            return jsonify({"error": "Instructor no encontrado"}), 404
        data["instructor"] = instructor.id  # Guardar el ID del instructor en lugar del email
        data["instructor"] = str(data["instructor"])  # Convertir a string para MongoDB
        guia = Guias(**data)
        guia.save()
        return jsonify({"message": "guia guardada"}), 201
    except Exception as e:
        print("Error al crear el guia:", e)
        return jsonify({"error": "Error al crear la guia"}), 500

@app.route("/guiasvista", methods=["GET"])
def guiasvista():
    try:
        guias = Guias.objects()
        return render_template('guias.html', guias=guias), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    
@app.route("/agregarGuiaVista", methods=["GET"])
def agregarGuiaVista():
    try:
        return render_template('agregarGuia.html'), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route("/agregarGuia", methods=["POST"])
def agregarGuia():
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)

        docPDF = request.files.get("txtGuiaPDF")

        if not docPDF:
            return jsonify({"error": "Debe adjuntar un archivo PDF"}), 400

        instructor = Instructores.objects(nombre=data.get("instructor")).first()

        if not instructor:
            return jsonify({"error": "Instructor no encontrado"}), 404

        data["instructor"] = instructor.id
        data["fecha"] = date.today()

        nombre_pdf = secure_filename(docPDF.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_pdf)
        docPDF.save(ruta)
        data["documento_pdf"] = nombre_pdf

        guia = Guias(**data)
        guia.save()

        return jsonify({"message": "Guía guardada correctamente"}), 201

    except Exception as e:
        print("Error al crear la guía:", e)
        return jsonify({"error": str(e)}), 500
