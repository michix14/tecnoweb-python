import smtplib
from email.mime.text import MIMEText
from email.mime. multipart import MIMEMultipart
from email.header import Header
from typing import Optional
import logging
from config. settings import settings

class EmailSender:
    """Envía correos usando SMTP con soporte multi-servidor"""
    
    def __init__(self):
        self.logger = logging. getLogger('EmailSender')
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        body_html: str, 
        body_text: Optional[str] = None,
        in_reply_to: Optional[str] = None,
        references: Optional[str] = None
    ) -> bool:
        """
        Envía un correo electrónico con soporte UTF-8 y multi-servidor
        
        Args: 
            to_email:  Email del destinatario
            subject:  Asunto del correo
            body_html: Cuerpo en HTML
            body_text:  Cuerpo en texto plano (opcional)
            in_reply_to: Message-ID del correo original (para respuestas)
            references: Referencias del hilo de conversación
        
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        try:  
            # Crear mensaje con charset UTF-8
            msg = MIMEMultipart('alternative')
            msg.set_charset('utf-8')
            
            # Headers
            msg['From'] = f"{settings. SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg['To'] = to_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # Headers para threading (respuestas)
            if in_reply_to:
                msg['In-Reply-To'] = in_reply_to
            if references: 
                msg['References'] = references
            
            # Agregar cuerpo en texto plano
            if body_text:
                part_text = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(part_text)
            
            # Agregar cuerpo en HTML
            part_html = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part_html)
            
            # Conectar según configuración (SSL, TLS o Plain)
            if settings.SMTP_USE_SSL:
                # Modo SSL (puerto 465 - típicamente Gmail)
                self.logger.debug(f"Conectando vía SSL a {settings.SMTP_HOST}:{settings.SMTP_PORT}")
                server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)
                
                # Autenticar
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                
                # Enviar
                server.send_message(msg)
                server.quit()
                
            else:
                # Modo Plain/TLS (puerto 25/587 - típicamente Tecnoweb)
                self.logger. debug(f"Conectando a {settings.SMTP_HOST}:{settings.SMTP_PORT}")
                server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)
                
                # Intentar STARTTLS
                try:
                    server.starttls()
                    self.logger.debug("STARTTLS activado")
                except Exception as e:
                    self. logger.debug(f"STARTTLS no disponible: {e}")
                
                # Autenticar si hay credenciales
                if settings. SMTP_USER and settings. SMTP_PASSWORD:
                    try:
                        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                        self.logger.debug("Autenticación exitosa")
                    except Exception as e:
                        self.logger.warning(f"Autenticación falló (continuando sin auth): {e}")
                
                # Enviar
                server. send_message(msg)
                server.quit()
            
            self.logger.info(f"✅ Correo enviado a {to_email}:  {subject[: 50]}...")
            return True
        
        except smtplib.SMTPAuthenticationError as e:
            self. logger.error(f"❌ Error de autenticación SMTP: {e}")
            return False
        
        except smtplib.SMTPException as e:
            self.logger.error(f"❌ Error SMTP enviando a {to_email}: {e}")
            return False
        
        except Exception as e:
            self.logger.error(f"❌ Error general enviando correo a {to_email}: {e}", exc_info=True)
            return False
    
    def send_command_response(
        self, 
        to_email: str, 
        command: str, 
        success: bool, 
        message:  str, 
        data: Optional[dict] = None,
        in_reply_to:  Optional[str] = None
    ) -> bool:
        """
        Envía respuesta de comando ejecutado
        
        Args: 
            to_email: Email del destinatario
            command: Comando ejecutado
            success: Si fue exitoso o no
            message: Mensaje de resultado
            data: Datos de respuesta (opcional)
            in_reply_to: Message-ID del correo original
        
        Returns:
            True si se envió correctamente
        """
        # Subject
        status = "✅ Éxito" if success else "❌ Error"
        subject = f"Re: {command} - {status}"
        
        # Generar HTML
        html = self._generate_response_html(command, success, message, data)
        
        # Generar texto plano
        text = self._generate_response_text(command, success, message, data)
        
        return self.send_email(
            to_email=to_email,
            subject=subject,
            body_html=html,
            body_text=text,
            in_reply_to=in_reply_to
        )
    
    def _generate_response_html(self, command: str, success: bool, message: str, data: Optional[dict]) -> str:
        """Genera HTML de respuesta con diseño mejorado"""
        color = '#28a745' if success else '#dc3545'
        icon = '✅' if success else '❌'
        status = 'ÉXITO' if success else 'ERROR'
        
        html = f"""
        <! DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: {color};
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    padding: 30px;
                }}
                . command-box {{
                    background-color:  #f8f9fa;
                    border-left: 4px solid {color};
                    padding: 15px;
                    margin: 15px 0;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                }}
                .message-box {{
                    background-color: #e7f3ff;
                    border-left: 4px solid #0066cc;
                    padding:  15px;
                    margin: 15px 0;
                }}
                table {{
                    border-collapse:  collapse;
                    width: 100%;
                    margin-top: 20px;
                    font-size: 14px;
                }}
                th, td {{
                    border:  1px solid #dee2e6;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #e9ecef;
                    font-weight: 600;
                    color: #495057;
                }}
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                tr:hover {{
                    background-color: #e9ecef;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #6c757d;
                    border-top: 1px solid #dee2e6;
                }}
                .badge {{
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                    font-weight: 600;
                    background-color: {color};
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{icon} {status}</h1>
                    <p style="margin:  5px 0 0 0; opacity: 0.9;">Sistema de Gestión - {settings.APP_NAME}</p>
                </div>
                
                <div class="content">
                    <h3>📋 Comando Ejecutado: </h3>
                    <div class="command-box">
                        {self._escape_html(command)}
                    </div>
                    
                    <h3>💬 Resultado:</h3>
                    <div class="message-box">
                        {self._escape_html(message)}
                    </div>
                    
                    {self._format_data_html(data) if data else ''}
                </div>
                
                <div class="footer">
                    <p><strong>{settings.APP_NAME}</strong></p>
                    <p>Este es un mensaje automático generado por el sistema</p>
                    <p style="margin-top: 10px; color: #adb5bd;">
                        No responda a este correo.  Para consultas, contacte al administrador.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_response_text(self, command:  str, success: bool, message:  str, data: Optional[dict]) -> str:
        """Genera respuesta en texto plano"""
        icon = '✅' if success else '❌'
        status = 'ÉXITO' if success else 'ERROR'
        
        text = f"""
╔════════════════════════════════════════════════════════════════╗
║  {icon} {status. center(58)} ║
╚════════════════════════════════════════════════════════════════╝

Sistema:  {settings.APP_NAME}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 COMANDO EJECUTADO:
   {command}

💬 RESULTADO:
   {message}

{self._format_data_text(data) if data else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Este es un mensaje automático generado por el sistema. 
No responda a este correo. 
        """
        
        return text. strip()
    
    def _format_data_html(self, data) -> str:
        """Formatea datos como tabla HTML"""
        if not data: 
            return ''
        
        if isinstance(data, list) and len(data) > 0:
            # Lista de registros
            headers = list(data[0].keys()) if isinstance(data[0], dict) else []
            
            if not headers:
                return f'<pre>{str(data)}</pre>'
            
            # Generar headers
            headers_html = ''.join([f'<th>{self._escape_html(str(h))}</th>' for h in headers])
            
            # Generar filas
            rows_html = ''
            for row in data: 
                cells = ''. join([
                    f'<td>{self._escape_html(str(row.get(h, "")))}</td>' 
                    for h in headers
                ])
                rows_html += f'<tr>{cells}</tr>'
            
            return f"""
            <h3>📊 Datos ({len(data)} registro{'s' if len(data) != 1 else ''}):</h3>
            <table>
                <thead>
                    <tr>{headers_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            """
        
        elif isinstance(data, dict):
            # Registro único
            rows = ''.join([
                f'<tr><th>{self._escape_html(str(k))}</th><td>{self._escape_html(str(v))}</td></tr>' 
                for k, v in data.items()
            ])
            return f"""
            <h3>📊 Datos: </h3>
            <table>{rows}</table>
            """
        
        else:
            return f'<pre>{self._escape_html(str(data))}</pre>'
    
    def _format_data_text(self, data) -> str:
        """Formatea datos como texto plano con tabulate"""
        if not data: 
            return ''
        
        try:
            from tabulate import tabulate
            
            if isinstance(data, list) and len(data) > 0:
                result = f"📊 DATOS ({len(data)} registro{'s' if len(data) != 1 else ''}):\n\n"
                result += tabulate(data, headers='keys', tablefmt='grid')
                return result
            
            elif isinstance(data, dict):
                result = "📊 DATOS:\n\n"
                result += tabulate(data.items(), headers=['Campo', 'Valor'], tablefmt='grid')
                return result
            
            else:
                return f"📊 DATOS:\n\n{str(data)}"
        
        except Exception as e:
            self.logger.warning(f"Error formateando datos con tabulate: {e}")
            return f"📊 DATOS:\n\n{str(data)}"
    
    def _escape_html(self, text:  str) -> str:
        """Escapa caracteres HTML para prevenir XSS"""
        if not isinstance(text, str):
            text = str(text)
        
        return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))