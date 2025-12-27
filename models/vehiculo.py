from typing import List, Dict, Optional
from . base import BaseModel
from config. database import db

class Vehiculo(BaseModel):
    """Modelo de Vehículo"""
    
    table_name = 'vehiculos'
    fields = ['id', 'cliente_id', 'placa', 'marca', 'modelo', 'anio',
              'color', 'kilometraje', 'foto', 'observaciones', 'estado',
              'created_at', 'updated_at']
    
    @classmethod
    def find_by_cliente(cls, cliente_id: int) -> List[Dict]:
        """Obtiene vehículos de un cliente"""
        return cls.find_all({'cliente_id': cliente_id})
    
    @classmethod
    def find_by_placa(cls, placa: str) -> Optional[Dict]:
        """Busca vehículo por placa"""
        query = f"SELECT * FROM {cls.table_name} WHERE placa = %s"
        results = db.execute(query, (placa,))
        return results[0] if results else None