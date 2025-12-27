import time
import logging
import signal
import sys
from threading import Event
from services.email_reader import EmailReader
from services.email_sender import EmailSender
from services.email_processor import EmailCommandProcessor
from config.settings import settings
from config.database import db

class EmailDaemon:  
    """Daemon que revisa correos constantemente usando POP3"""
    
    def __init__(self):
        self.running = Event()
        self.running.set()
        
        self.email_reader = EmailReader()
        self.email_sender = EmailSender()
        self.email_processor = EmailCommandProcessor()
        
        self.setup_logging()
        self.setup_signal_handlers()
        
        self.processed_count = 0
        self.error_count = 0
        self.cycle_count = 0
    
    def setup_logging(self):
        """Configura logging"""
        import os
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO if settings.DEBUG else logging.WARNING,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('EmailDaemon')
    
    def setup_signal_handlers(self):
        """Configura manejadores de señales para shutdown graceful"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal. SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Maneja señales de terminación"""
        self.logger. info(f"⚠️ Señal {signum} recibida.  Deteniendo daemon...")
        self.stop()
    
    def start(self):
        """Inicia el daemon"""
        self. logger.info(f"{'='*70}")
        self.logger.info(f"🚀 Iniciando {settings.APP_NAME} Email Daemon (POP3)")
        self.logger. info(f"{'='*70}")
        self.logger.info(f"📧 Monitoreando: {settings.POP3_USER}")
        self.logger.info(f"🖥️ Servidor POP3: {settings.POP3_HOST}:{settings.POP3_PORT}")
        self.logger.info(f"⏱️ Intervalo de revisión: {settings. POP3_CHECK_INTERVAL}s")
        self.logger.info(f"🗑️ Eliminar después de leer: {settings.POP3_DELETE_AFTER_READ}")
        self.logger.info(f"🔒 Requiere autenticación: {settings. REQUIRE_AUTH}")
        self.logger.info(f"{'='*70}\n")
        
        try:
            # Loop principal
            while self.running. is_set():
                self.cycle_count += 1
                self.logger.info(f"\n{'─'*70}")
                self.logger.info(f"🔄 Ciclo #{self.cycle_count} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info(f"{'─'*70}")
                
                self.check_emails()
                
                # Esperar antes de la siguiente revisión
                if self.running.is_set():
                    self.logger.info(f"💤 Esperando {settings.POP3_CHECK_INTERVAL}s hasta el próximo ciclo.. .\n")
                    self.running.wait(settings.POP3_CHECK_INTERVAL)
        
        except Exception as e:
            self.logger.error(f"❌ Error crítico en daemon: {e}", exc_info=True)
        
        finally:
            self. cleanup()
    
    def check_emails(self):
        """Revisa correos nuevos (conecta y desconecta cada vez)"""
        self.logger. info("🔍 Conectando a servidor POP3...")
        
        # Conectar
        if not self.email_reader.connect():
            self.logger.error("❌ No se pudo conectar a POP3")
            self.error_count += 1
            return
        
        try:
            # Obtener correos nuevos
            emails = self.email_reader.get_new_emails()
            
            if not emails:
                self.logger.info("📭 No hay correos nuevos para procesar")
            else:
                self.logger. info(f"📬 Encontrados {len(emails)} correo(s) nuevo(s)")
                
                # Procesar cada correo
                for email_data in emails:  
                    self.process_email(email_data)
            
            # Reset contador de errores si fue exitoso
            self.error_count = 0
        
        except Exception as e:  
            self.logger.error(f"❌ Error revisando correos: {e}", exc_info=True)
            self.error_count += 1
        
        finally:
            # Siempre desconectar
            self.email_reader.disconnect()
    
    def process_email(self, email_data:  dict):
        """Procesa un correo individual"""
        from_email = email_data['from_email']
        subject = email_data['subject']
        email_hash = email_data['hash']
        message_id = email_data['message_id']
        
        self. logger.info(f"\n{'┌'+'─'*68+'┐'}")
        self.logger.info(f"│ ⚙️ PROCESANDO CORREO{' '*49}│")
        self.logger.info(f"{'├'+'─'*68+'┤'}")
        self.logger.info(f"│ De: {from_email[: 60]: <60}│")
        self.logger. info(f"│ Nombre: {email_data['from_name'][: 57]:<57}│")
        self.logger.info(f"│ Asunto: {subject[:57]: <57}│")
        self.logger.info(f"│ Fecha: {email_data['date'][:58]:<58}│")
        self.logger.info(f"{'└'+'─'*68+'┘'}")
        
        try:
            # Procesar comando
            result = self.email_processor.process_email_command(email_data)
            
            # Log del resultado
            if result['success']: 
                self.logger. info(f"✅ Comando ejecutado:  {result['message']}")
                
                # Mostrar datos si existen
                if result.get('data'):
                    data = result['data']
                    if isinstance(data, list):
                        self.logger. info(f"📊 Datos:  {len(data)} registro(s)")
                    elif isinstance(data, dict):
                        self.logger.info(f"📊 Datos: {len(data)} campo(s)")
            else:
                self.logger. warning(f"⚠️ Comando falló: {result['message']}")
            
            # Enviar respuesta
            self.logger.info("📤 Enviando respuesta por correo...")
            sent = self.email_sender.send_command_response(
                to_email=from_email,
                command=subject,
                success=result['success'],
                message=result['message'],
                data=result. get('data'),
                in_reply_to=message_id
            )
            
            if sent:
                self.logger. info("✅ Respuesta enviada correctamente")
            else:
                self.logger.error("❌ Error enviando respuesta")
            
            # Marcar como procesado
            self. email_reader.mark_as_processed(email_data)
            
            # Eliminar del servidor si está configurado
            if settings.POP3_DELETE_AFTER_READ:
                self.email_reader.delete_email(email_data['index'])
            
            self.processed_count += 1
            self.logger.info(f"✓ Total procesados en esta sesión: {self.processed_count}")
        
        except Exception as e: 
            self.logger.error(f"❌ Error procesando correo: {e}", exc_info=True)
            
            # Intentar enviar correo de error
            try:
                self.email_sender.send_command_response(
                    to_email=from_email,
                    command=subject,
                    success=False,
                    message=f"Error interno del sistema:  {str(e)}",
                    data=None,
                    in_reply_to=message_id
                )
                self.logger.info("📧 Correo de error enviado al usuario")
            except:  
                self.logger.error("❌ No se pudo enviar correo de error")
    
    def stop(self):
        """Detiene el daemon"""
        self. logger.info("\n🛑 Deteniendo daemon...")
        self.running.clear()
    
    def cleanup(self):
        """Limpia recursos"""
        self.logger.info("\n🧹 Limpiando recursos...")
        
        try:
            self.email_reader.disconnect()
        except:
            pass
        
        try:
            db.close()
        except:
            pass
        
        self.logger. info(f"\n{'='*70}")
        self.logger.info(f"📊 ESTADÍSTICAS FINALES")
        self.logger. info(f"{'='*70}")
        self.logger.info(f"   - Ciclos ejecutados: {self.cycle_count}")
        self.logger.info(f"   - Correos procesados: {self.processed_count}")
        self.logger.info(f"   - Errores: {self.error_count}")
        self.logger. info(f"{'='*70}")
        self.logger.info("👋 Daemon detenido correctamente\n")