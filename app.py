from flask import Flask, request, jsonify, render_template, redirect, url_for
from models.db import get_db
from services.email_service import enviar_correo
from services.recordatorios import iniciar_scheduler
import threading
import secrets
from datetime import datetime
import re

app = Flask(__name__)

# =========================
# RUTA PRINCIPAL
# =========================
@app.route('/')
def inicio():
    return render_template('index.html')


# =========================
# CREAR CITA
# =========================
@app.route('/crear_cita', methods=['POST'])
def crear_cita():
    data = request.json

    nombre = data.get("nombre")
    telefono = data.get("telefono")
    email = data.get("email")
    barbero_id = data.get("barbero_id")
    fecha = data.get("fecha")
    hora = data.get("hora")

    #VALIDAR CAMPOS
    if not all([nombre, telefono, email, barbero_id, fecha, hora]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if len(nombre.strip()) < 3:
        return jsonify({"error": "Nombre muy corto"}), 400

    if not telefono.isdigit() or len(telefono) < 8:
        return jsonify({"error": "Teléfono inválido"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Email inválido"}), 400

    #VALIDAR FECHA Y HORA
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        hora_obj = datetime.strptime(hora, "%H:%M")
    except:
        return jsonify({"error": "Formato de fecha u hora inválido"}), 400

    if fecha_obj.date() < datetime.now().date():
        return jsonify({"error": "No puedes seleccionar fechas pasadas"}), 400

    if fecha_obj.weekday() == 6:
        return jsonify({"error": "No trabajamos domingos"}), 400

    if hora_obj.hour < 9 or hora_obj.hour >= 18:
        return jsonify({"error": "Horario fuera de servicio (9AM - 6PM)"}), 400

    db = get_db()

    #VALIDAR BARBERO
    barbero = db.execute(
        "SELECT * FROM barberos WHERE id = ?",
        (barbero_id,)
    ).fetchone()

    if not barbero:
        db.close()
        return jsonify({"error": "Barbero no válido"}), 400

    #VALIDAR DISPONIBILIDAD
    existe = db.execute("""
        SELECT * FROM citas
        WHERE barbero_id = ? AND fecha = ? AND hora = ?
    """, (barbero_id, fecha, hora)).fetchone()

    if existe:
        db.close()
        return jsonify({"error": "Esta hora ya está ocupada"}), 400

    #CLIENTE
    cliente = db.execute(
        "SELECT * FROM clientes WHERE email = ?",
        (email,)
    ).fetchone()

    if cliente:
        cliente_id = cliente["id"]
    else:
        cursor = db.execute(
            "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)",
            (nombre, telefono, email)
        )
        cliente_id = cursor.lastrowid

    #EVITAR DUPLICADO DEL CLIENTE
    duplicada = db.execute("""
        SELECT * FROM citas
        WHERE cliente_id = ? AND fecha = ? AND hora = ?
    """, (cliente_id, fecha, hora)).fetchone()

    if duplicada:
        db.close()
        return jsonify({"error": "Ya tienes una cita en ese horario"}), 400

    try:
        token = secrets.token_urlsafe(16)

        db.execute("""
            INSERT INTO citas (cliente_id, barbero_id, fecha, hora, token)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente_id, barbero_id, fecha, hora, token))

        db.commit()

        enviar_correo(
            email,
            nombre,
            fecha,
            hora,
            barbero["nombre"],
            token
        )

        return jsonify({"mensaje": "Cita creada correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db.close()


# =========================
# VER CITAS
# =========================
@app.route('/citas', methods=['GET'])
def ver_citas():
    db = get_db()

    citas = db.execute("""
        SELECT c.id, cl.nombre, cl.telefono, b.nombre as barbero, c.fecha, c.hora
        FROM citas c
        JOIN clientes cl ON c.cliente_id = cl.id
        JOIN barberos b ON c.barbero_id = b.id
    """).fetchall()

    db.close()

    return jsonify([dict(c) for c in citas])


# =========================
# CANCELAR
# =========================
@app.route('/cancelar/<token>')
def pagina_cancelar(token):
    db = get_db()

    cita = db.execute("""
        SELECT c.id, cl.nombre, b.nombre as barbero, c.fecha, c.hora
        FROM citas c
        JOIN clientes cl ON c.cliente_id = cl.id
        JOIN barberos b ON c.barbero_id = b.id
        WHERE c.token = ?
    """, (token,)).fetchone()

    db.close()

    if not cita:
        return "<h2>Cita no encontrada ❌</h2>"

    return render_template("cancelar.html", cita=cita, token=token)


@app.route('/confirmar_cancelacion/<token>', methods=['POST'])
def confirmar_cancelacion(token):
    db = get_db()

    res = db.execute("DELETE FROM citas WHERE token = ?", (token,))
    db.commit()
    db.close()

    if res.rowcount == 0:
        return "<h2>Esta cita ya fue cancelada</h2>"

    return redirect(url_for('cancelado'))


@app.route('/cancelado')
def cancelado():
    return render_template('cancelado.html')


# =========================
# REAGENDAR
# =========================
@app.route('/reagendar/<token>')
def pagina_reagendar(token):
    db = get_db()

    cita = db.execute("""
        SELECT c.id, cl.nombre, cl.email, b.nombre as barbero, c.fecha, c.hora
        FROM citas c
        JOIN clientes cl ON c.cliente_id = cl.id
        JOIN barberos b ON c.barbero_id = b.id
        WHERE c.token = ?
    """, (token,)).fetchone()

    db.close()

    if not cita:
        return "<h2>Cita no encontrada</h2>"

    return render_template("reagendar.html", cita=cita, token=token)


@app.route('/confirmar_reagendado/<token>', methods=['POST'])
def confirmar_reagendado(token):

    nueva_fecha = request.form.get("fecha")
    nueva_hora = request.form.get("hora")

    try:
        fecha_obj = datetime.strptime(nueva_fecha, "%Y-%m-%d")
        hora_obj = datetime.strptime(nueva_hora, "%H:%M")
    except:
        return "<h2>❌ Formato inválido</h2>"

    # VALIDACIONES
    if fecha_obj.date() < datetime.now().date():
        return "<h2>❌ Fecha pasada</h2>"

    if fecha_obj.weekday() == 6:
        return "<h2>❌ No trabajamos domingos</h2>"

    if hora_obj.hour < 9 or hora_obj.hour >= 18:
        return "<h2>❌ Fuera de horario</h2>"

    db = get_db()

    cita = db.execute("""
        SELECT cl.nombre, cl.email, b.nombre as barbero
        FROM citas c
        JOIN clientes cl ON c.cliente_id = cl.id
        JOIN barberos b ON c.barbero_id = b.id
        WHERE c.token = ?
    """, (token,)).fetchone()

    if not cita:
        db.close()
        return "<h2>Cita no encontrada ❌</h2>"

    # VALIDAR OCUPADO
    ocupado = db.execute("""
        SELECT * FROM citas
        WHERE fecha = ? AND hora = ? AND token != ?
    """, (nueva_fecha, nueva_hora, token)).fetchone()

    if ocupado:
        db.close()
        return "<h2>❌ Hora ocupada</h2>"

    db.execute("""
        UPDATE citas
        SET fecha = ?, hora = ?
        WHERE token = ?
    """, (nueva_fecha, nueva_hora, token))

    db.commit()
    db.close()

    enviar_correo(
        cita["email"],
        cita["nombre"],
        nueva_fecha,
        nueva_hora,
        cita["barbero"],
        token,
        tipo="reagendado"
    )

    return "<h2>🔄 Cita reagendada correctamente 💈</h2>"


# =========================
# TESTIMONIOS
# =========================
@app.route('/crear_testimonio', methods=['POST'])
def crear_testimonio():
    data = request.json

    nombre = data.get("nombre")
    comentario = data.get("comentario")
    estrellas = data.get("estrellas")

    if not nombre or not comentario or not estrellas:
        return jsonify({"error": "Campos obligatorios"}), 400

    if len(comentario) < 5:
        return jsonify({"error": "Comentario muy corto"}), 400

    if int(estrellas) < 1 or int(estrellas) > 5:
        return jsonify({"error": "Estrellas inválidas"}), 400

    db = get_db()

    db.execute("""
        INSERT INTO testimonios (nombre, comentario, estrellas)
        VALUES (?, ?, ?)
    """, (nombre, comentario, estrellas))

    db.commit()
    db.close()

    return jsonify({"mensaje": "Guardado"})


@app.route('/testimonios')
def obtener_testimonios():
    db = get_db()

    data = db.execute("""
        SELECT nombre, comentario, estrellas
        FROM testimonios
        ORDER BY id DESC
    """).fetchall()

    db.close()

    return jsonify([dict(t) for t in data])


# =========================
# INICIO
# =========================
if __name__ == '__main__':
    hilo = threading.Thread(target=iniciar_scheduler)
    hilo.daemon = True
    hilo.start()

    app.run(debug=True)