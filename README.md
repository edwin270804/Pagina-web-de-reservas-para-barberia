# 💈 Jr Barbershop - Sistema de Reservas

Sistema web completo para la gestión de citas en una barbería, desarrollado con **Flask (Python)** y tecnologías modernas de frontend.

---

## 🚀 Características principales

- 📅 Reservas de citas en línea
- ❌ Cancelación de citas mediante token seguro
- 🔄 Reagendado de citas
- 📧 Envío automático de correos
- ⭐ Sistema de testimonios con calificación
- 🎨 Interfaz moderna con animaciones
- 🔒 Validación de datos en frontend y backend

---

## 🛠 Tecnologías utilizadas

**Backend:**
- Python
- Flask
- SQLite
- Threading (scheduler de tareas)

**Frontend:**
- HTML5
- CSS3 (animaciones y diseño responsivo)
- JavaScript (DOM + Fetch API)

---

## 📦 Estructura del proyecto
proyecto/
├─ static/
│ ├─ css/
│ ├─ js/
│ └─ recursos/
├─ templates/
├─ models/
├─ services/
├─ app.py
├─ .env
└─ .gitignore

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/edwin270804/Pagina-web-de-reservas-para-barberia.git
cd Pagina-web-de-reservas-para-barberia
Crear y activar entorno virtual:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate
Instalar dependencias:
pip install flask
Crear archivo .env con tus credenciales:
EMAIL_USER=tu_correo
EMAIL_PASS=tu_password
SECRET_KEY=clave_secreta
Ejecutar el proyecto:
python app.py

Abrir en el navegador:

http://127.0.0.1:5000
📡 API Endpoints
Método	Ruta	Descripción
POST	/crear_cita	Crear nueva cita
GET	/citas	Listar todas las citas
GET	/cancelar/<token>	Vista de cancelación de cita
POST	/confirmar_cancelacion/<token>	Cancelar cita
GET	/reagendar/<token>	Vista de reagendar cita
POST	/confirmar_reagendado/<token>	Reagendar cita
POST	/crear_testimonio	Crear un testimonio
GET	/testimonios	Listar testimonios
🔒 Seguridad
Validación de datos en backend
Tokens únicos para acciones sensibles
Prevención de duplicación de citas
🎯 Mejoras futuras
Panel de administrador
Autenticación de usuarios
Pagos en línea
Notificaciones por WhatsApp

👨‍💻 Autor

Edwin Segura
GitHub: edwin270804
