import logging
from typing import Dict, Optional
from lexer. parser import parse_command
from interpreter.command_interpreter import CommandInterpreter
from config.settings import settings

class EmailCommandProcessor:
    """Procesa comandos recibidos por correo electrónico"""
    
    def __init__(self):
        self.logger = logging.getLogger('EmailProcessor')
        self.interpreter = CommandInterpreter()
    
    def process_email_command(self, email_data: Dict) -> Dict:
        """
        Procesa un comando recibido por correo
        
        Args:
            email_data:  Diccionario con datos del correo
                - from_email:  Email del remitente
                - subject: Asunto (contiene el comando)
                - body:  Cuerpo del correo
                - etc.
        
        Returns:
            Dict con resultado:  
                - success: bool
                - message: str
                - data: Any
        """
        from_email = email_data['from_email']
        subject = email_data['subject']
        
        self.logger.info(f"📨 Procesando correo de {from_email}:  {subject}")
        
        # 1. Parsear comando del subject
        command = parse_command(subject)
        
        if not command:
            self.logger.error(f"❌ No se pudo parsear el comando: {subject}")
            return {
                'success':  False,
                'message': f'No se pudo parsear el comando: "{subject}". Verifique la sintaxis.',
                'data': None
            }
        
        # 2. Crear contexto de ejecución (sin usuario registrado)
        context = {
            'user_id': None,
            'nombre': from_email. split('@')[0],  # Usar parte antes del @
            'email': from_email,
            'tipo': 'invitado'
        }
        
        self. logger.info(f"👤 Email: {from_email}")
        self.logger.info(f"🔧 Comando: {command.entity} {command.action}")
        
        # 3. INTERPRETAR Y EJECUTAR
        try:
            result = self. interpreter.interpret(command, context)
            
            # Log del resultado
            if result['success']: 
                self.logger.info(f"✅ Éxito: {result['message']}")
            else:
                self.logger.warning(f"⚠️ Fallo: {result['message']}")
            
            return result
        
        except Exception as e: 
            self. logger.error(f"❌ Error ejecutando comando: {e}", exc_info=True)
            return {
                'success':  False,
                'message': f'Error al ejecutar comando: {str(e)}',
                'data': None
            }