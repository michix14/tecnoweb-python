import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración
SMTP_HOST = os.getenv('SMTP_HOST_GMAIL', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT_GMAIL', 465))
SMTP_USE_SSL = os.getenv('SMTP_USE_SSL_GMAIL', 'True').lower() == 'true'
SMTP_USER = os.getenv('SMTP_USER_GMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD_GMAIL')
FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL_GMAIL')
TO_EMAIL = "michixcard@gmail.com"  # Cambia por un correo de prueba

# Crear mensaje
msg = MIMEText("Hola, este es un correo de prueba usando SSL directo.")
msg['Subject'] = "Prueba SSL Gmail"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# Conexión y envío
try:
    if SMTP_USE_SSL:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    else:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("✅ Correo enviado correctamente usando SSL directo.")
except Exception as e:
    print("❌ Error enviando correo:", e)
