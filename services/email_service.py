from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from datetime import datetime



load_dotenv()

API_KEY = os.getenv("SENDGRID_API_KEY")

def enviar_correo(destinatario, nombre, fecha, hora, barbero, token,tipo="reagendado"):
    try:

        meses = {
    "01": "enero", "02": "febrero", "03": "marzo",
    "04": "abril", "05": "mayo", "06": "junio",
    "07": "julio", "08": "agosto", "09": "septiembre",
    "10": "octubre", "11": "noviembre", "12": "diciembre"
}

        dt = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_formateada = f"{dt.day:02d} de {meses[dt.strftime('%m')]} de {dt.year}"
        hora_obj = datetime.strptime(hora, "%H:%M")
        hora_formateada = hora_obj.strftime("%I:%M %p")
        if tipo == "reagendado":
            titulo = "Tu cita fue reagendada 🔄"
            mensaje_estado = "ha sido reagendada"
        else:
            titulo = "Cita confirmada 💈"
            mensaje_estado = "ha sido confirmada"
        email = Mail(
            from_email= "edwin.moreno1184@gmail.com",
            to_emails= destinatario,
            subject= titulo,
            html_content= f"""
<html>
<body style="margin:0; padding:0; background:#0f0f0f; font-family:Arial, sans-serif;">

<div style="max-width:500px; margin:40px auto; background:#1a1a1a; border-radius:12px; padding:30px; text-align:center; color:#fff; box-shadow:0 0 20px rgba(0,0,0,0.5);">

    <!-- LOGO -->
    <img src="https://i.imgur.com/J5YUXz0.png" 
        style="width:90px; margin-bottom:15px; border-radius:10px;">

    <h1 style="color:#d4af37; margin-bottom:5px;">Jr BarberShop</h1>
    <p style="color:#aaa; margin-top:0;">Estilo & Precisión</p>

    <hr style="border:none; border-top:1px solid #333; margin:20px 0;">

    <!-- MENSAJE -->
    <h2 style="margin-bottom:10px;">Hola {nombre} 👋</h2>
    <p style="color:#ccc;">
        Tu cita ha sido <strong style="color:#d4af37;">{mensaje_estado}</strong>
    </p>

    <!-- DATOS -->
    <div style="background:#111; padding:20px; border-radius:10px; margin-top:20px; text-align:left;">
        <p>📅 <strong>Fecha:</strong> {fecha_formateada}</p>
        <p>⏰ <strong>Hora:</strong> {hora_formateada}</p>
        <p>💇🏽 <strong>Barbero:</strong> {barbero}</p>
    </div>

    <!-- BOTÓN -->
    <a href="http://127.0.0.1:5000/cancelar/{token}"
    style="display:inline-block; margin-top:25px; padding:14px 25px; background:#ee8277; color:#fff; text-decoration:none; border-radius:8px; font-weight:bold;">
        Cancelar cita ❌
    </a>

    <a href="http://127.0.0.1:5000/reagendar/{token}"
    style="display:inline-block; margin-top:15px; padding:14px 25px; background:#c9a227; color:#000; text-decoration:none; border-radius:8px; font-weight:bold;">
        Reagendar cita 🔄
    </a>

    <p style="margin-top:25px; font-size:14px; color:#777;">
        Te esperamos 💈
    </p>

    <p style="font-size:12px; color:#777;">
    © 2026 Jr BarberShop 💈<br>
    contacto@barberia.com<br>
    Rivas,Nicaragua
</p>

<span style="color:#555;">Este es un correo automático, por favor no responder.</span>

</div>

</body>
</html>
"""
        )

        sg = SendGridAPIClient(API_KEY)
        response = sg.send(email)

        print("Correo Enviado:",response.status_code)
        return True
    
    except Exception as e:
        print("Error enviando correo:",e)
        return False