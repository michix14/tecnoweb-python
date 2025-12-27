from typing import List, Dict, Optional
import bcrypt
from . base import BaseModel
from config.database import db

class Usuario(BaseModel):
    """Modelo de Usuario (Propietario, Secretaria, Mecánico, Cliente)"""
    
    table_name = 'usuarios'
    fields = ['id', 'nombre', 'email', 'password_hash', 'telefono', 
              'direccion', 'tipo', 'estado', 'foto', 'created_at', 'updated_at']
    
    @classmethod
    def create_with_password(cls, data: Dict) -> int:
        """Crea usuario con hash de contraseña"""
        if 'password' in data:
            password = data. pop('password')
            data['password_hash'] = cls. hash_password(password)
        
        return cls.create(data)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash de contraseña con bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifica contraseña contra hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional[Dict]:
        """Busca usuario por email"""
        query = f"SELECT * FROM {cls.table_name} WHERE email = %s"
        return db.execute(query, (email,), fetch_one=True)
    
    @classmethod
    def find_by_tipo(cls, tipo: str) -> List[Dict]:
        """Obtiene usuarios por tipo"""
        return cls.find_all({'tipo': tipo})