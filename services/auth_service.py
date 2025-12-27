from typing import Optional, Dict
from models.usuario import Usuario

class AuthService:
    """Servicio de autenticación de usuarios"""
    
    def __init__(self):
        self.login_attempts = {}
    
    def authenticate_by_email(self, email: str) -> Optional[Dict]:
        """
        Autentica un usuario solo por email (sin password)
        Útil para comandos por correo donde el email ya está validado
        
        Args:
            email:  Email del usuario
        
        Returns:
            Dict con datos del usuario si existe, None si no
        """
        user = Usuario.find_by_email(email)
        
        if not user:
            return {
                'success': False,
                'message':  'Usuario no encontrado en el sistema',
                'user':  None
            }
        
        return {
            'success': True,
            'message': 'Usuario autenticado',
            'user': {
                'id': user['id'],
                'nombre': user['nombre'],
                'email':  user['email'],
                'tipo': user['tipo']
            }
        }
    
    def authenticate(self, email: str, password: str) -> Dict:
        """
        Autentica un usuario con email y password
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
        
        Returns: 
            Dict con resultado de autenticación
        """
        user = Usuario.find_by_email(email)
        
        if not user:
            return {
                'success': False,
                'message': 'Email o contraseña incorrectos',
                'user':  None
            }
        
        # Verificar contraseña
        if Usuario.verify_password(password, user['password_hash']):
            return {
                'success': True,
                'message': 'Autenticación exitosa',
                'user': {
                    'id':  user['id'],
                    'nombre': user['nombre'],
                    'email': user['email'],
                    'tipo': user['tipo']
                }
            }
        else:
            return {
                'success': False,
                'message': 'Email o contraseña incorrectos',
                'user': None
            }