import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # ==============================================
    # Aplicación
    # ==============================================
    APP_NAME = os.getenv('APP_NAME', 'Taller Mecánico')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # ==============================================
    # Base de datos
    # ==============================================
    DB_HOST = os. getenv('DB_HOST', 'mail.tecnoweb.org.bo')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'db_grupo01sa')
    DB_USER = os.getenv('DB_USER', 'grupo01sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'grup001grup001*')
    
    # ==============================================
    # Selección de servidor SMTP (solo envío)
    # ==============================================
    EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'tecnoweb').lower()
    
    # ==============================================
    # SMTP - Configuración dinámica según servidor
    # ==============================================
    @classmethod
    def get_smtp_config(cls):
        """Retorna configuración SMTP según EMAIL_SERVER"""
        server = cls.EMAIL_SERVER
        
        if server == 'gmail':
            return {
                'SMTP_HOST': os.getenv('SMTP_HOST_GMAIL', 'smtp.gmail.com'),
                'SMTP_PORT': int(os.getenv('SMTP_PORT_GMAIL', 465)),
                'SMTP_USE_SSL': os.getenv('SMTP_USE_SSL_GMAIL', 'True').lower() == 'true',
                'SMTP_USER': os.getenv('SMTP_USER_GMAIL', ''),
                'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD_GMAIL', ''),
                'SMTP_FROM_EMAIL': os.getenv('SMTP_FROM_EMAIL_GMAIL', ''),
                'SMTP_FROM_NAME': os.getenv('SMTP_FROM_NAME_GMAIL', cls.APP_NAME),
            }
        
        elif server == 'tecnoweb':
            return {
                'SMTP_HOST': os.getenv('SMTP_HOST_TECNOWEB', 'tecnoweb.org. bo'),
                'SMTP_PORT': int(os.getenv('SMTP_PORT_TECNOWEB', 25)),
                'SMTP_USE_SSL':  os.getenv('SMTP_USE_SSL_TECNOWEB', 'False').lower() == 'true',
                'SMTP_USER': os.getenv('SMTP_USER_TECNOWEB', ''),
                'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD_TECNOWEB', ''),
                'SMTP_FROM_EMAIL':  os.getenv('SMTP_FROM_EMAIL_TECNOWEB', ''),
                'SMTP_FROM_NAME': os.getenv('SMTP_FROM_NAME_TECNOWEB', cls. APP_NAME),
            }
        
        else:
            raise ValueError(f"EMAIL_SERVER inválido: {server}. Use 'gmail' o 'tecnoweb'")
    
    # Cargar configuración SMTP
    _smtp_config = None
    
    @classmethod
    def _load_smtp_config(cls):
        if cls._smtp_config is None:
            cls._smtp_config = cls.get_smtp_config()
        return cls._smtp_config
    
    # ==============================================
    # SMTP Properties (Envío)
    # ==============================================
    @property
    def SMTP_HOST(self):
        return self._load_smtp_config()['SMTP_HOST']
    
    @property
    def SMTP_PORT(self):
        return self._load_smtp_config()['SMTP_PORT']
    
    @property
    def SMTP_USE_SSL(self):
        return self._load_smtp_config()['SMTP_USE_SSL']
    
    @property
    def SMTP_USER(self):
        return self._load_smtp_config()['SMTP_USER']
    
    @property
    def SMTP_PASSWORD(self):
        return self._load_smtp_config()['SMTP_PASSWORD']
    
    @property
    def SMTP_FROM_EMAIL(self):
        return self._load_smtp_config()['SMTP_FROM_EMAIL']
    
    @property
    def SMTP_FROM_NAME(self):
        return self._load_smtp_config()['SMTP_FROM_NAME']
    
    # ==============================================
    # POP3 - SIEMPRE TECNOWEB (Recepción)
    # ==============================================
    POP3_HOST = os.getenv('POP3_HOST', 'mail.tecnoweb. org.bo')
    POP3_PORT = int(os. getenv('POP3_PORT', 110))
    POP3_USE_SSL = os. getenv('POP3_USE_SSL', 'False').lower() == 'true'
    POP3_USER = os. getenv('POP3_USER', '')
    POP3_PASSWORD = os.getenv('POP3_PASSWORD', '')
    
    # ==============================================
    # Procesamiento de emails
    # ==============================================
    POP3_CHECK_INTERVAL = int(os.getenv('POP3_CHECK_INTERVAL', 30))
    POP3_DELETE_AFTER_READ = os.getenv('POP3_DELETE_AFTER_READ', 'False').lower() == 'true'
    MAX_PROCESSED_HISTORY = int(os.getenv('MAX_PROCESSED_HISTORY', 1000))
    
    # ==============================================
    # Seguridad
    # ==============================================
    ALLOWED_EMAILS = [e.strip() for e in os.getenv('ALLOWED_EMAILS', '').split(',') if e.strip()]
    REQUIRE_AUTH = os.getenv('REQUIRE_AUTH', 'False').lower() == 'true'
    
    # ==============================================
    # Archivos
    # ==============================================
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    PROCESSED_EMAILS_FILE = os.getenv('PROCESSED_EMAILS_FILE', 'data/processed_emails.txt')


# Instancia global
settings = Settings()