from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'clave_segura_reuseit'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

usuarios = {
    "gisell": {"password": "admin123", "rol": "admin"},
    "gisell": {"password": "admin123", "rol": "admin"},
    "emmanuel": {"password": "emmanuel123", "rol": "lector"}
}

semanas = [
    {
        "titulo": "Semana 1 - Base del proyecto",
        "fecha": "15 al 20 de septiembre",
        "tareas": [
            "Configurar Django y PostgreSQL",
            "Crear modelo personalizado de usuario (core.User)",
            "Definir roles en el modelo Role",
            "Activar Swagger (DRF-YASG)",
            "Crear endpoint de estado /api/status/"
        ],
        "archivo": "",
        "logros": "", "obstaculos": "", "proximo": "", "mejoras": "", "novedades": ""
    },
    {
        "titulo": "Semana 2 - Inventario",
        "fecha": "22 al 27 de septiembre",
        "tareas": [
            "Crear modelo Producto",
            "Implementar CRUD con DRF",
            "Agregar filtros por categoría y ubicación",
            "Asignar permisos por rol (arrendador)",
            "Registrar en admin"
        ],
        "archivo": "",
        "logros": "", "obstaculos": "", "proximo": "", "mejoras": "", "novedades": ""
    },
    {
        "titulo": "Semana 3 - Reservas",
        "fecha": "29 de septiembre al 3 de octubre",
        "tareas": [
            "Crear modelo Reserva",
            "Validar fechas y disponibilidad",
            "Crear ViewSet con permisos",
            "Proteger con JWT",
            "Documentar en Swagger"
        ],
        "archivo": "",
        "logros": "", "obstaculos": "", "proximo": "", "mejoras": "", "novedades": ""
    },
    {
        "titulo": "Semana 4 - Facturación",
        "fecha": "6 al 11 de octubre",
        "tareas": [
            "Crear modelos Factura y DetalleFactura",
            "Generar factura desde reserva",
            "Agregar permisos por rol",
            "Registrar en Swagger"
        ],
        "archivo": "",
        "logros": "", "obstaculos": "", "proximo": "", "mejoras": "", "novedades": ""
    },
    {
        "titulo": "Semana 5 - Entrega final",
        "fecha": "13 al 18 de octubre",
        "tareas": [
            "Revisar y corregir bugs",
            "Completar documentación técnica",
            "Validar integración entre módulos",
            "Preparar evidencias para entrega",
            "Entregar backend funcional"
        ],
        "archivo": "",
        "logros": "", "obstaculos": "", "proximo": "", "mejoras": "", "novedades": ""
    }
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario in usuarios and usuarios[usuario]["password"] == clave:
            session["usuario"] = usuario
            session["rol"] = usuarios[usuario]["rol"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST" and session["rol"] == "admin":
        if "semana" in request.form:
            semana_index = int(request.form["semana"])
            file = request.files.get("archivo")
            if file:
                filename = f"semana{semana_index + 1}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                semanas[semana_index]["archivo"] = filename

            campos = ["logros", "obstaculos", "proximo", "mejoras", "novedades"]
            for campo in campos:
                valor = request.form.get(f"{campo}{semana_index + 1}")
                if valor:
                    semanas[semana_index][campo] = valor

    return render_template("usm.html", semanas=semanas, rol=session["rol"], usuario=session["usuario"])

@app.route("/eliminar_archivo", methods=["POST"])
def eliminar_archivo():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect(url_for("login"))

    semana_index = int(request.form["semana"])
    archivo = semanas[semana_index]["archivo"]

    if archivo:
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], archivo)
        if os.path.exists(ruta):
            os.remove(ruta)
        semanas[semana_index]["archivo"] = ""

    return redirect(url_for("dashboard"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)










