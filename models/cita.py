from .base import BaseModel
from datetime import datetime
from typing import List, Dict

class Cita(BaseModel):
    """Modelo de Cita"""
    
    table_name = 'citas'
    fields = ['id', 'codigo', 'cliente_id', 'vehiculo_id', 'fecha', 'hora',
              'motivo', 'estado', 'observaciones', 'created_at', 'updated_at']
    
    @staticmethod
    def generar_codigo() -> str:
        """
        Genera un código único para la cita
        Formato: CIT-YYYYMMDDHHMMSS-XXXX (random)
        """
        import random
        from datetime import datetime
    
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
        return f'CIT-{timestamp}-{random_suffix}'
    
    @classmethod
    def find_by_cliente(cls, cliente_id: int) -> List[Dict]:
        """Obtiene citas de un cliente"""
        return cls.find_all({'cliente_id': cliente_id})
    
    @classmethod
    def find_by_estado(cls, estado: str) -> List[Dict]:
        """Obtiene citas por estado"""
        return cls.find_all({'estado': estado})
    
    @classmethod
    def find_pendientes(cls) -> List[Dict]:
        """Obtiene citas pendientes"""
        return cls.find_all({'estado': 'pendiente'})