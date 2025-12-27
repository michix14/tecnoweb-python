from .base import BaseModel
from datetime import datetime
from typing import List, Dict
from config.database import db

class OrdenTrabajo(BaseModel):
    """Modelo de Orden de Trabajo"""
    
    table_name = 'ordenes_trabajo'
    fields = ['id', 'codigo', 'diagnostico_id', 'mecanico_id', 'fecha_creacion',
              'fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real',
              'costo_mano_obra', 'costo_repuestos', 'subtotal', 'estado',
              'observaciones', 'created_at', 'updated_at']
    
    @classmethod
    def generar_codigo(cls) -> str:
        """Genera código único para orden de trabajo"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"ORD-{timestamp}"
    
    @classmethod
    def agregar_servicio(cls, orden_id: int, servicio_id: int, 
                         cantidad: int = 1, precio_unitario: float = 0) -> int:
        """Agrega un servicio a la orden de trabajo"""
        query = """
            INSERT INTO orden_servicios 
            (orden_trabajo_id, servicio_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        result = db.execute(query, (orden_id, servicio_id, cantidad, precio_unitario))
        return result[0]['id']
    
    @classmethod
    def get_servicios(cls, orden_id: int) -> List[Dict]:
        """Obtiene servicios de una orden de trabajo"""
        query = """
            SELECT os.*, s.nombre as servicio_nombre, s.descripcion as servicio_descripcion
            FROM orden_servicios os
            INNER JOIN servicios s ON os.servicio_id = s.id
            WHERE os.orden_trabajo_id = %s
            ORDER BY os.id
        """
        return db.execute(query, (orden_id,))
    
    @classmethod
    def find_by_mecanico(cls, mecanico_id: int) -> List[Dict]:
        """Obtiene órdenes de trabajo de un mecánico"""
        return cls.find_all({'mecanico_id': mecanico_id})
    
    @classmethod
    def find_by_estado(cls, estado: str) -> List[Dict]:
        """Obtiene órdenes de trabajo por estado"""
        return cls.find_all({'estado': estado})