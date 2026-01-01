"""
Modelo de Usuario (Propietario, Secretaria, Mecánico, Cliente)
"""
from typing import List, Dict, Optional
import bcrypt
from .  base import BaseModel
from config. database import db


class Usuario(BaseModel):
    """Modelo de Usuario (Propietario, Secretaria, Mecánico, Cliente)"""
    
    table_name = 'usuarios'
    fields = ['id', 'nombre', 'email', 'password_hash', 'telefono', 
              'direccion', 'tipo', 'estado', 'foto', 'created_at', 'updated_at']
    
    @classmethod
    def create_with_password(cls, data: Dict) -> Optional[int]:
        """
        Crea usuario con hash de contraseña
        
        Args:
            data (dict): Datos del usuario (debe incluir 'password')
        
        Returns:
            int: ID del usuario creado o None
        """
        # Hacer copia para no modificar el dict original
        data_copy = data.copy()
        
        # Hashear password si existe
        if 'password' in data_copy:
            password = data_copy.pop('password')
            data_copy['password_hash'] = cls. hash_password(password)
        
        # Asegurar que tenga estado por defecto
        if 'estado' not in data_copy: 
            data_copy['estado'] = 'activo'
        
        # Log para debug
        import logging
        logger = logging.getLogger('Usuario')
        logger.debug(f"Creando usuario con datos: {list(data_copy.keys())}")
        
        # Crear usando el método base
        return cls.create(data_copy)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera hash de contraseña con bcrypt
        
        Args: 
            password (str): Contraseña en texto plano
        
        Returns: 
            str: Hash de la contraseña
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verifica contraseña contra hash
        
        Args: 
            password (str): Contraseña en texto plano
            password_hash (str): Hash almacenado
        
        Returns:
            bool: True si coincide, False si no
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional[Dict]:
        """
        Busca usuario por email
        
        Args:
            email (str): Email del usuario
        
        Returns:
            dict: Usuario encontrado o None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE email = %s"
        return db.execute(query, (email,), fetch_one=True)
    
    @classmethod
    def find_by_tipo(cls, tipo: str) -> List[Dict]:
        """
        Obtiene usuarios por tipo
        
        Args: 
            tipo (str): Tipo de usuario (cliente, mecanico, etc)
        
        Returns:
            list: Lista de usuarios del tipo especificado
        """
        query = f"SELECT * FROM {cls.table_name} WHERE tipo = %s"
        result = db.execute(query, (tipo,), fetch_all=True)
        return result if result is not None else []
    
    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[Dict]:
        """
        Autentica un usuario
        
        Args: 
            email (str): Email del usuario
            password (str): Contraseña en texto plano
        
        Returns:
            dict: Usuario si credenciales correctas, None si no
        """
        user = cls.find_by_email(email)
        
        if not user:
            return None
        
        if cls.verify_password(password, user['password_hash']):
            return user
        
        return None