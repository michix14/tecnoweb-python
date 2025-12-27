import poplib
import email
from email.header import decode_header, Header
from typing import List, Dict, Optional
import logging
import hashlib
import os
import re
import base64
import quopri
from config. settings import settings

class EmailReader: 
    """Lee correos usando POP3 con soporte multi-proveedor (Gmail, Hotmail, Yahoo, etc.)"""
    
    def __init__(self):
        self.logger = logging. getLogger('EmailReader')
        self.pop3 = None
        self.processed_ids = self._load_processed_ids()
    
    def _load_processed_ids(self) -> set:
        """Carga IDs de correos ya procesados"""
        os.makedirs(os.path.dirname(settings. PROCESSED_EMAILS_FILE), exist_ok=True)
        
        if os.path.exists(settings.PROCESSED_EMAILS_FILE):
            with open(settings.PROCESSED_EMAILS_FILE, 'r', encoding='utf-8') as f:
                return set(line. strip() for line in f.readlines())
        return set()
    
    def _save_processed_id(self, email_id: str):
        """Guarda ID de correo procesado"""
        self.processed_ids.add(email_id)
        
        # Limitar tamaño del archivo
        if len(self. processed_ids) > settings.MAX_PROCESSED_HISTORY:
            self.processed_ids = set(list(self.processed_ids)[-settings.MAX_PROCESSED_HISTORY:])
        
        with open(settings.PROCESSED_EMAILS_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.processed_ids))
    
    def connect(self) -> bool:
        """Conecta al servidor POP3"""
        try: 
            self.logger.info(f"🔌 Conectando a {settings. POP3_HOST}:{settings.POP3_PORT}...")
            
            if settings.POP3_USE_SSL:
                self.pop3 = poplib.POP3_SSL(settings.POP3_HOST, settings.POP3_PORT, timeout=30)
            else:
                self.pop3 = poplib.POP3(settings.POP3_HOST, settings.POP3_PORT, timeout=30)
            
            # Autenticar
            self.pop3.user(settings.POP3_USER)
            self.pop3.pass_(settings.POP3_PASSWORD)
            
            # Obtener estadísticas
            num_messages, mailbox_size = self.pop3.stat()
            
            self.logger.info(f"✅ Conectado a POP3: {settings.POP3_HOST}")
            self.logger.info(f"📊 Mensajes en servidor: {num_messages}, Tamaño:  {mailbox_size} bytes")
            
            return True
        
        except poplib.error_proto as e:
            self.logger. error(f"❌ Error de autenticación POP3: {e}")
            return False
        
        except Exception as e:
            self.logger.error(f"❌ Error conectando a POP3: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del servidor POP3"""
        if self. pop3:
            try:
                self.pop3.quit()
                self.logger. info("🔌 Desconectado de POP3")
            except: 
                pass
    
    def get_new_emails(self) -> List[Dict]:
        """Obtiene correos nuevos (no procesados)"""
        try:
            # Obtener número de mensajes
            num_messages = len(self.pop3.list()[1])
            
            if num_messages == 0:
                return []
            
            self.logger.info(f"📬 Total de mensajes en servidor: {num_messages}")
            
            emails = []
            
            # Iterar sobre todos los mensajes (del más nuevo al más viejo)
            for i in range(num_messages, 0, -1):
                email_data = self._fetch_email(i)
                
                if email_data:
                    # Verificar si ya fue procesado
                    email_hash = email_data['hash']
                    
                    if email_hash not in self.processed_ids:
                        emails.append(email_data)
                        self. logger.info(f"📨 Nuevo correo #{i}: {email_data['from_email']} - {email_data['subject'][: 50]}")
                    else:
                        self.logger.debug(f"⏭️ Correo #{i} ya procesado anteriormente")
            
            return emails
        
        except Exception as e: 
            self.logger.error(f"❌ Error obteniendo correos:  {e}", exc_info=True)
            return []
    
    def _fetch_email(self, message_num: int) -> Optional[Dict]:
        """Obtiene datos de un correo específico"""
        try:
            # Obtener el mensaje completo
            response, lines, octets = self.pop3.retr(message_num)
            
            # Unir todas las líneas
            email_bytes = b'\r\n'.join(lines)
            
            # Parsear el mensaje
            email_message = email.message_from_bytes(email_bytes)
            
            # Generar hash único del correo
            email_hash = self._generate_email_hash(email_message)
            
            # Decodificar subject (mejorado para todos los proveedores)
            subject = self._decode_header(email_message.get('Subject', ''))
            
            # Obtener remitente (mejorado)
            from_header = email_message.get('From', '')
            from_email = self._extract_email(from_header)
            from_name = self._extract_name(from_header)
            
            # Obtener fecha
            date = email_message.get('Date', '')
            
            # Message ID
            message_id = email_message.get('Message-ID', '')
            
            # Obtener cuerpo (mejorado para multipart)
            body = self._get_email_body(email_message)
            
            # Detectar proveedor (para debugging)
            provider = self._detect_provider(email_message)
            
            return {
                'index': message_num,
                'hash': email_hash,
                'message_id': message_id,
                'from_email': from_email,
                'from_name': from_name,
                'subject': subject,
                'body':  body,
                'date': date,
                'provider': provider,
                'raw':  email_message
            }
        
        except Exception as e:
            self. logger.error(f"❌ Error procesando correo #{message_num}:  {e}", exc_info=True)
            return None
    
    def _generate_email_hash(self, email_message) -> str:
        """Genera hash único del correo para evitar duplicados"""
        # Usar Message-ID si existe (más confiable)
        message_id = email_message.get('Message-ID', '')
        if message_id:
            return hashlib.sha256(message_id.encode('utf-8')).hexdigest()[:32]
        
        # Si no, usar combinación de campos
        unique_str = (
            email_message.get('From', '') +
            email_message.get('Date', '') +
            email_message.get('Subject', '') +
            str(email_message.get('Content-Type', ''))
        )
        return hashlib.sha256(unique_str. encode('utf-8', errors='ignore')).hexdigest()[:32]
    
    def _decode_header(self, header: str) -> str:
        """
        Decodifica header con soporte para Gmail, Hotmail, Yahoo
        Soporta: UTF-8, Base64, Quoted-Printable, ISO-8859-1
        """
        if not header:
            return ''
        
        try:
            decoded_parts = decode_header(header)
            decoded_string = ''
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    # Lista extendida de encodings (orden de prioridad)
                    encodings_to_try = [
                        encoding,              # El especificado
                        'utf-8',              # UTF-8 (Gmail, moderno)
                        'iso-8859-1',         # Latin-1 (Hotmail/Outlook)
                        'windows-1252',       # Windows (Hotmail/Outlook)
                        'us-ascii',           # ASCII (Yahoo)
                        'latin-1',            # Fallback
                        'cp1252',             # Windows español
                    ]
                    
                    decoded = None
                    for enc in encodings_to_try:
                        if enc is None: 
                            continue
                        try:
                            decoded = part.decode(enc, errors='strict')
                            break
                        except (UnicodeDecodeError, LookupError, AttributeError):
                            continue
                    
                    # Último recurso: replace
                    if decoded is None: 
                        decoded = part.decode('utf-8', errors='replace')
                    
                    decoded_string += decoded
                else: 
                    decoded_string += str(part)
            
            return decoded_string.strip()
        
        except Exception as e:
            self.logger.warning(f"⚠️ Error decodificando header, usando fallback: {e}")
            # Fallback: intentar decodificar directamente
            try:
                return header.encode('latin-1').decode('utf-8', errors='replace')
            except:
                return str(header)
    
    def _extract_email(self, from_header: str) -> str:
        """
        Extrae email del header From
        Formatos soportados:
        - nombre <email@example.com>
        - email@example.com
        - <email@example.com>
        """
        if not from_header: 
            return ''
        
        # Decodificar primero (puede tener encoding)
        from_header = self._decode_header(from_header)
        
        # Buscar patrón <email>
        match = re.search(r'<([^>]+)>', from_header)
        if match:
            return match.group(1).strip().lower()
        
        # Buscar email sin < >
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_header)
        if match:
            return match.group(0).strip().lower()
        
        return from_header.strip('<>').lower()
    
    def _extract_name(self, from_header:  str) -> str:
        """
        Extrae nombre del header From
        """
        if not from_header:
            return ''
        
        # Decodificar
        from_header = self._decode_header(from_header)
        
        # Si tiene formato:  nombre <email>
        match = re.match(r'(.+?)\s*<', from_header)
        if match:
            name = match.group(1).strip().strip('"').strip("'")
            return name
        
        # Si no tiene nombre, usar parte antes del @
        email_match = re.search(r'([\w\.-]+)@', from_header)
        if email_match:
            return email_match.group(1)
        
        return ''
    
    def _get_email_body(self, email_message) -> str:
        """
        Obtiene el cuerpo del correo con soporte robusto para: 
        - Gmail: multipart/alternative con text/plain
        - Hotmail/Outlook: multipart/mixed, quoted-printable
        - Yahoo:  multipart/alternative, base64
        """
        body = ''
        
        if email_message. is_multipart():
            # Procesar multipart (Gmail, Hotmail, Yahoo)
            body = self._extract_multipart_body(email_message)
        else:
            # Mensaje simple (raro, pero posible)
            body = self._decode_payload(email_message)
        
        return body. strip()
    
    def _extract_multipart_body(self, email_message) -> str:
        """Extrae cuerpo de mensaje multipart"""
        text_parts = []
        html_parts = []
        
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition', ''))
            
            # Ignorar adjuntos
            if 'attachment' in content_disposition: 
                continue
            
            # Preferir text/plain
            if content_type == 'text/plain':
                text_content = self._decode_payload(part)
                if text_content:
                    text_parts.append(text_content)
            
            # Guardar HTML como fallback
            elif content_type == 'text/html':
                html_content = self._decode_payload(part)
                if html_content:
                    html_parts.append(html_content)
        
        # Preferir texto plano
        if text_parts:
            return '\n\n'.join(text_parts)
        
        # Si solo hay HTML, convertir a texto (simple)
        if html_parts: 
            return self._html_to_text('\n\n'.join(html_parts))
        
        return ''
    
    def _decode_payload(self, part) -> str:
        """
        Decodifica payload con soporte para: 
        - Base64 (Gmail, Yahoo)
        - Quoted-Printable (Hotmail/Outlook)
        - 7bit, 8bit (ASCII)
        """
        try:
            # Obtener charset
            charset = part.get_content_charset() or 'utf-8'
            
            # Obtener transfer encoding
            transfer_encoding = part.get('Content-Transfer-Encoding', '').lower()
            
            # Obtener payload
            payload = part.get_payload(decode=True)
            
            if not payload:
                # Intentar sin decode
                payload = part.get_payload(decode=False)
                if isinstance(payload, list):
                    return ''
                if not isinstance(payload, bytes):
                    payload = str(payload).encode('utf-8')
            
            # Decodificar según transfer encoding
            if transfer_encoding == 'base64':
                try:
                    payload = base64.b64decode(payload)
                except: 
                    pass
            
            elif transfer_encoding == 'quoted-printable':
                try: 
                    payload = quopri. decodestring(payload)
                except: 
                    pass
            
            # Decodificar con charset
            encodings_to_try = [
                charset,
                'utf-8',
                'iso-8859-1',
                'windows-1252',
                'us-ascii',
                'latin-1'
            ]
            
            for encoding in encodings_to_try: 
                if not encoding:
                    continue
                try:
                    return payload. decode(encoding, errors='strict')
                except (UnicodeDecodeError, LookupError, AttributeError):
                    continue
            
            # Último recurso
            return payload.decode('utf-8', errors='replace')
        
        except Exception as e: 
            self.logger.error(f"❌ Error decodificando payload: {e}")
            return ''
    
    def _html_to_text(self, html:  str) -> str:
        """Convierte HTML simple a texto plano"""
        import re
        
        # Eliminar scripts y estilos
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re. DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Eliminar tags HTML
        text = re.sub(r'<br\s*/? >', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decodificar entidades HTML
        try:
            import html as html_parser
            text = html_parser. unescape(text)
        except:
            pass
        
        # Limpiar espacios múltiples
        text = re. sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'  +', ' ', text)
        
        return text.strip()
    
    def _detect_provider(self, email_message) -> str:
        """Detecta el proveedor del correo (para debugging)"""
        received = email_message.get('Received', '').lower()
        x_mailer = email_message.get('X-Mailer', '').lower()
        message_id = email_message.get('Message-ID', '').lower()
        
        if 'gmail' in received or 'google' in received or 'gmail.com' in message_id:
            return 'Gmail'
        elif 'outlook' in received or 'hotmail' in received or 'microsoft' in x_mailer:
            return 'Outlook/Hotmail'
        elif 'yahoo' in received or 'yahoo.com' in message_id:
            return 'Yahoo'
        elif 'tecnoweb' in received or 'tecnoweb.org.bo' in message_id:
            return 'Tecnoweb'
        else: 
            return 'Desconocido'
    
    def mark_as_processed(self, email_data: dict):
        """Marca correo como procesado"""
        email_hash = email_data['hash']
        self._save_processed_id(email_hash)
        self.logger. debug(f"✓ Correo marcado como procesado: {email_hash}")
    
    def delete_email(self, message_num:  int):
        """Elimina correo del servidor (¡CUIDADO!)"""
        if settings.POP3_DELETE_AFTER_READ:
            try:
                self.pop3.dele(message_num)
                self.logger.info(f"🗑️ Correo #{message_num} eliminado del servidor")
            except Exception as e: 
                self.logger.error(f"❌ Error eliminando correo #{message_num}: {e}")