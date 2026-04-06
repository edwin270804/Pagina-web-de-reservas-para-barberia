import schedule
import time
from datetime import datetime, timedelta
from models.db import get_db
from services.whatsapp import enviar_whatsapp

def revisar_citas():
    db = get_db()

    ahora = datetime.now()
    en_una_hora = ahora + timedelta(hours=1)

    citas = db.execute("""
        SELECT c.id, cl.nombre, cl.telefono, c.fecha, c.hora, c.notificado
        FROM citas c
        JOIN clientes cl ON c.cliente_id = cl.id
    """).fetchall()

    for c in citas:
        try:
            fecha_hora_cita = datetime.strptime(
                f"{c['fecha']} {c['hora']}",
                "%Y-%m-%d %H:%M"
            )
        except ValueError:
            print("Cita con formato inválido:", c['fecha'], c['hora'])
            continue

        #si no ha sido notificado
        if c["notificado"] == 0 and ahora <= fecha_hora_cita <= en_una_hora:

            mensaje = f"Hola {c['nombre']}, recuerda tu cita en 1 hora 💈"
            enviar_whatsapp(c["telefono"], mensaje)

            # MARCAR COMO NOTIFICADO
            db.execute(
                "UPDATE citas SET notificado = 1 WHERE id = ?",
                (c["id"],)
            )
            db.commit()

    db.close()


def iniciar_scheduler():
    schedule.every(1).minutes.do(revisar_citas)

    while True:
        schedule.run_pending()
        time.sleep(1)


        