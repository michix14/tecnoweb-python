#!/usr/bin/env python3
"""
Script de prueba para envío de correos
Taller Mecánico - Sistema de Gestión

Uso: 
    python test_email.py
"""

import sys
import os

# Agregar directorio raíz al path
sys.path. insert(0, os.path. dirname(os.path.abspath(__file__)))

from services.email_sender import EmailSender
from config. settings import settings

def print_header():
    """Imprime encabezado"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🧪  TEST DE ENVÍO DE CORREOS                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def test_simple_email():
    """Prueba envío simple"""
    print("\n📧 Test 1: Envío simple de correo")
    print("─" * 60)
    
    sender = EmailSender()
    
    to_email = input("Ingrese email destino: ").strip()
    
    if not to_email: 
        print("❌ Email vacío.  Abortando.")
        return False
    
    print(f"\n📤 Enviando correo de prueba a: {to_email}")
    
    subject = f"🔧 Test - {settings.APP_NAME}"
    
    html_body = """
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #28a745;">✅ Test de Correo Exitoso</h2>
        <p>Este es un correo de prueba del sistema <strong>Taller Mecánico</strong>.</p>
        
        <h3>Características: </h3>
        <ul>
            <li>✅ Soporte UTF-8 completo</li>
            <li>✅ Caracteres especiales:  Ñ á é í ó ú</li>
            <li>✅ Formato HTML</li>
            <li>✅ Emojis:  🚗 🔧 ✅ 📧</li>
        </ul>
        
        <p>Si recibiste este correo, la configuración SMTP está correcta.</p>
        
        <hr>
        <p style="font-size: 12px; color: #666;">
            Este es un mensaje automático de prueba del sistema {app_name}
        </p>
    </body>
    </html>
    """.format(app_name=settings.APP_NAME)
    
    text_body = f"""
✅ TEST DE CORREO EXITOSO

Este es un correo de prueba del sistema {settings.APP_NAME}. 

Características:
  ✅ Soporte UTF-8 completo
  ✅ Caracteres especiales:  Ñ á é í ó ú
  ✅ Formato texto plano
  ✅ Emojis: 🚗 🔧 ✅ 📧

Si recibiste este correo, la configuración SMTP está correcta. 

---
Este es un mensaje automático de prueba
    """
    
    success = sender.send_email(
        to_email=to_email,
        subject=subject,
        body_html=html_body,
        body_text=text_body
    )
    
    if success:
        print("✅ Correo enviado exitosamente")
        print(f"📬 Revisa la bandeja de entrada de:  {to_email}")
        return True
    else:
        print("❌ Error al enviar correo")
        print("💡 Verifica la configuración SMTP en . env")
        return False

def test_command_response():
    """Prueba envío de respuesta de comando"""
    print("\n\n📧 Test 2: Respuesta de comando")
    print("─" * 60)
    
    sender = EmailSender()
    
    to_email = input("Ingrese email destino: ").strip()
    
    if not to_email: 
        print("❌ Email vacío. Abortando.")
        return False
    
    print(f"\n📤 Enviando respuesta de comando a: {to_email}")
    
    # Datos de prueba
    test_data = [
        {'id': 1, 'nombre': 'Juan Pérez', 'email': 'juan@example.com', 'tipo': 'cliente'},
        {'id': 2, 'nombre': 'María García', 'email': 'maria@example.com', 'tipo': 'cliente'},
        {'id': 3, 'nombre': 'José López', 'email': 'jose@example.com', 'tipo': 'mecanico'}
    ]
    
    success = sender.send_command_response(
        to_email=to_email,
        command="usuario mostrar",
        success=True,
        message="Se encontraron 3 usuario(s)",
        data=test_data
    )
    
    if success:
        print("✅ Respuesta de comando enviada exitosamente")
        print(f"📬 Revisa la bandeja de entrada de: {to_email}")
        return True
    else: 
        print("❌ Error al enviar respuesta")
        return False

def test_caracteres_especiales():
    """Prueba caracteres especiales"""
    print("\n\n📧 Test 3: Caracteres especiales (Ñ, tildes, emojis)")
    print("─" * 60)
    
    sender = EmailSender()
    
    to_email = input("Ingrese email destino:  ").strip()
    
    if not to_email:
        print("❌ Email vacío. Abortando.")
        return False
    
    print(f"\n📤 Enviando con caracteres especiales a: {to_email}")
    
    subject = "Prueba:  Ñoño José María - Símbolos € £ ¥"
    
    html_body = """
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>🔤 Test de Caracteres Especiales</h2>
        
        <h3>Español: </h3>
        <ul>
            <li>Ñ ñ - España, año, niño, señor</li>
            <li>Tildes: á é í ó ú</li>
            <li>Mayúsculas:  Á É Í Ó Ú</li>
            <li>Diéresis: ü - pingüino, güero</li>
        </ul>
        
        <h3>Símbolos:</h3>
        <ul>
            <li>Monedas: € £ ¥ $</li>
            <li>Otros:  © ® ™ § ¶</li>
        </ul>
        
        <h3>Emojis: </h3>
        <p style="font-size: 24px;">
            🚗 🔧 🛠️ ⚙️ 🔩 ✅ ❌ ⚠️ 📧 📨 📬 📭 🎉 👍
        </p>
        
        <h3>Nombres con caracteres especiales:</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th style="padding:  8px;">Nombre</th>
                <th style="padding: 8px;">Email</th>
            </tr>
            <tr>
                <td style="padding:  8px;">José María Peña</td>
                <td style="padding: 8px;">jose@example.com</td>
            </tr>
            <tr>
                <td style="padding: 8px;">María José Núñez</td>
                <td style="padding: 8px;">maria@example.com</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Iñaki Año</td>
                <td style="padding: 8px;">inaki@example.com</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    success = sender.send_email(
        to_email=to_email,
        subject=subject,
        body_html=html_body
    )
    
    if success:
        print("✅ Correo con caracteres especiales enviado")
        print("🔍 Verifica que se vean correctamente:")
        print("   - Ñ y ñ")
        print("   - Tildes (á, é, í, ó, ú)")
        print("   - Símbolos (€, £, ¥)")
        print("   - Emojis (🚗, 🔧, ✅)")
        return True
    else:
        print("❌ Error al enviar correo")
        return False

def main():
    """Función principal"""
    print_header()
    
    print("Configuración actual:")
    print(f"  📧 SMTP Host: {settings.SMTP_HOST}:{settings.SMTP_PORT}")
    print(f"  👤 Usuario: {settings.SMTP_USER}")
    print(f"  📤 From: {settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>")
    print("\n")
    
    # Menú de opciones
    while True:
        print("\n" + "═" * 60)
        print("MENÚ DE TESTS")
        print("═" * 60)
        print("1. Test simple de envío")
        print("2. Test de respuesta de comando")
        print("3. Test de caracteres especiales")
        print("4. Ejecutar todos los tests")
        print("0. Salir")
        print("─" * 60)
        
        opcion = input("Seleccione una opción:  ").strip()
        
        if opcion == "1":
            test_simple_email()
        elif opcion == "2": 
            test_command_response()
        elif opcion == "3": 
            test_caracteres_especiales()
        elif opcion == "4":
            email = input("\nIngrese email para todos los tests: ").strip()
            if email:
                # Ejecutar todos los tests con el mismo email
                import time
                tests = [test_simple_email, test_command_response, test_caracteres_especiales]
                for i, test in enumerate(tests, 1):
                    print(f"\n{'═'*60}")
                    print(f"Ejecutando test {i}/{len(tests)}")
                    print(f"{'═'*60}")
                    # Mockear input para usar el email proporcionado
                    import builtins
                    original_input = builtins.input
                    builtins.input = lambda _: email
                    test()
                    builtins. input = original_input
                    if i < len(tests):
                        time.sleep(2)  # Pausa entre tests
        elif opcion == "0":
            print("\n👋 Saliendo...")
            break
        else: 
            print("❌ Opción inválida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario")
        sys.exit(0)
    except Exception as e: 
        print(f"\n❌ Error:  {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)