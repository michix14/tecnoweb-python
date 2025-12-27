from .base import BaseModel
from datetime import datetime
from typing import List, Dict
from config.database import db

class Diagnostico(BaseModel):
    """Modelo de Diagnóstico"""
    
    table_name = 'diagnosticos'
    fields = ['id', 'codigo', 'cita_id', 'mecanico_id', 'fecha_diagnostico',
              'descripcion_problema', 'diagnostico', 'recomendaciones',
              'estado', 'created_at', 'updated_at']
    
    @classmethod
    def generar_codigo(cls) -> str:
        """Genera código único para diagnóstico"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"DIAG-{timestamp}"
    
    @classmethod
    def find_by_mecanico(cls, mecanico_id: int) -> List[Dict]:
        """Obtiene diagnósticos de un mecánico"""
        return cls. find_all({'mecanico_id': mecanico_id})
    
    @classmethod
    def find_by_estado(cls, estado: str) -> List[Dict]:
        """Obtiene diagnósticos por estado"""
        return cls.find_all({'estado': estado})