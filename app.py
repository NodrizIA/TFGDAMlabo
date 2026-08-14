import os
import sqlite3
from pathlib import Path

from datos_troubleshooting import obtener_paso, validar_arbol_decision
from flask import Flask, flash, redirect, render_template, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "laboratorio.db"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
EXTENSIONES_IMAGEN = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("LABASSISTANT_SECRET_KEY", "clave_desarrollo_tfg")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


def extension_permitida(nombre_archivo):
    return "." in nombre_archivo and nombre_archivo.rsplit(".", 1)[1].lower() in EXTENSIONES_IMAGEN


def listar_imagenes(id_paso):
    carpeta = UPLOAD_DIR / id_paso
    if not carpeta.exists():
        return []

    imagenes = []
    for archivo in sorted(carpeta.iterdir()):
        if archivo.is_file() and extension_permitida(archivo.name):
            imagenes.append(f"uploads/{id_paso}/{archivo.name}")
    return imagenes


def conectar_bd():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def listar_parametros():
    with conectar_bd() as conn:
        # ACTUALIZADO: Solo pedimos el nombre, ya que los mínimos y máximos ahora dependen del sexo
        return conn.execute(
            "SELECT nombre FROM parametros ORDER BY nombre"
        ).fetchall()


def obtener_parametro_bd(nombre_parametro):
    with conectar_bd() as conn:
        return conn.execute(
            "SELECT * FROM parametros WHERE lower(nombre) = lower(?)",
            (nombre_parametro.strip(),),
        ).fetchone()


@app.route("/")
def index():
    return render_template("index.html", parametros=listar_parametros())


@app.route("/analizar", methods=["POST"])
def analizar():
    parametro_usuario = request.form.get("parametro", "").strip()
    valor_usuario = request.form.get("valor", "").strip()
    
    # NUEVO: Capturamos el sexo del formulario HTML
    sexo_usuario = request.form.get("sexo", "").strip() 

    try:
        valor = float(valor_usuario)
    except ValueError:
        flash("Introduce un valor numérico válido.", "danger")
        return redirect(url_for("index"))
        
    # NUEVO: Validamos que haya seleccionado un sexo
    if sexo_usuario not in ["M", "F"]:
        flash("Por favor, selecciona el sexo del paciente.", "danger")
        return redirect(url_for("index"))

    datos_db = obtener_parametro_bd(parametro_usuario)
    if datos_db is None:
        flash("Todavía no hay información para ese parámetro.", "warning")
        return redirect(url_for("index"))

    # NUEVO: Lógica de separación por sexos
    if sexo_usuario == 'M':
        minimo = datos_db["min_ref_m"]
        maximo = datos_db["max_ref_m"]
    else:
        minimo = datos_db["min_ref_f"]
        maximo = datos_db["max_ref_f"]

    # La evaluación ahora es independiente del sexo, usa el minimo y maximo calculados arriba
    if valor < minimo:
        estado = "bajo"
        mensaje = datos_db["mensaje_bajo"]
        color_alerta = "danger"
    elif valor > maximo:
        estado = "alto"
        mensaje = datos_db["mensaje_alto"]
        color_alerta = "danger"
    else:
        estado = "normal"
        mensaje = "Valores dentro del intervalo de referencia."
        color_alerta = "success"

    return render_template(
        "resultado.html",
        parametro=datos_db,
        valor=valor,
        estado=estado,
        mensaje=mensaje,
        color_alerta=color_alerta,
        rango_min=minimo, # Le pasamos los rangos a la vista por si quieres mostrarlos
        rango_max=maximo
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        usuario_valido = os.environ.get("LABASSISTANT_USER", "admin")
        password_valida = os.environ.get("LABASSISTANT_PASSWORD", "1234")

        if usuario == usuario_valido and password == password_valida:
            session["usuario_logueado"] = True
            session["usuario"] = usuario
            return redirect(url_for("panel_tecnico"))

        mensaje = "Usuario o contraseña incorrectos."

    return render_template("login.html", mensaje=mensaje)


@app.route("/tecnicos")
def panel_tecnico():
    if not session.get("usuario_logueado"):
        return redirect(url_for("login"))

    return render_template("panel_tecnico.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/troubleshooting/<id_paso>")
@app.route("/troubleshooting")
def troubleshooting(id_paso="inicio"):
    if not session.get("usuario_logueado"):
        return redirect(url_for("login"))

    paso = obtener_paso(id_paso)
    imagenes = listar_imagenes(id_paso) if paso.get("permite_imagenes") else []
    return render_template("troubleshooting.html", paso=paso, id_paso=id_paso, imagenes=imagenes)


@app.route("/troubleshooting/<id_paso>/imagenes", methods=["POST"])
def subir_imagen_troubleshooting(id_paso):
    if not session.get("usuario_logueado"):
        return redirect(url_for("login"))

    flash("La subida de imagenes esta desactivada.", "warning")
    return redirect(url_for("troubleshooting", id_paso=id_paso))


if __name__ == "__main__":
    validar_arbol_decision()
    app.run(debug=True)
