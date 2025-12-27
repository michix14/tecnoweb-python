#!/usr/bin/env python3
"""
Daemon de procesamiento de comandos por correo (POP3)
Taller Mecánico - Sistema de Gestión

Uso:
    python run_daemon. py
    
    O en background:
    nohup python run_daemon.py > output.log 2>&1 &
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daemon.email_daemon import EmailDaemon
from config.settings import settings

def print_banner():
    """Imprime banner de inicio"""
    banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🔧  {settings.APP_NAME. upper().center(59)}  🔧   ║
║                                                                   ║
║              EMAIL COMMAND DAEMON (POP3)                          ║
║                                                                   ║
║   Procesamiento automático de comandos por correo electrónico    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Configuración:
  📧 Email:          {settings.POP3_USER}
  🖥️  Servidor:      {settings.POP3_HOST}:{settings.POP3_PORT}
  ⏱️  Intervalo:     {settings.POP3_CHECK_INTERVAL}s
  🔒 Autenticación: {'Activada' if settings. REQUIRE_AUTH else 'Desactivada'}
  🐛 Debug:         {'Activado' if settings.DEBUG else 'Desactivado'}

Presiona Ctrl+C para detener el daemon
"""
    print(banner)

def main():
    """Función principal"""
    try:
        print_banner()
        
        # Crear instancia del daemon
        daemon = EmailDaemon()
        
        # Iniciar daemon
        daemon.start()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupción manual detectada (Ctrl+C)")
        print("Deteniendo daemon de forma segura...")
        
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        print("\n👋 Daemon finalizado")
        sys.exit(0)

if __name__ == "__main__":
    main()