from typing import List, Dict
from .base import BaseModel

class Servicio(BaseModel):
    """Modelo de Servicio"""
    
    table_name = 'servicios'
    fields = ['id', 'nombre', 'descripcion', 'tipo', 'precio_base',
              'duracion_estimada', 'estado', 'created_at', 'updated_at']
    
    @classmethod
    def find_by_tipo(cls, tipo: str) -> List[Dict]:
        """Obtiene servicios por tipo (diagnostico, mantenimiento, reparacion)"""
        return cls.find_all({'tipo': tipo})
    
    @classmethod
    def find_activos(cls) -> List[Dict]:
        """Obtiene solo servicios activos"""
        return cls.find_all({'estado':  'activo'})