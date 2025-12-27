from .base import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
from config.database import db

class Pago(BaseModel):
    """Modelo de Pago"""
    
    table_name = 'pagos'
    fields = ['id', 'codigo', 'orden_trabajo_id', 'monto_total', 'monto_pagado',
              'monto_pendiente', 'tipo_pago', 'numero_cuotas', 'cuotas_pagadas',
              'estado', 'fecha_vencimiento', 'observaciones', 'created_at', 'updated_at']
    
    @classmethod
    def generar_codigo(cls) -> str:
        """Genera código único para pago"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"PAG-{timestamp}"
    
    @classmethod
    def registrar_detalle_pago(cls, pago_id: int, monto: float, 
                               metodo_pago: str, numero_cuota: int = 1,
                               numero_comprobante: str = None, 
                               recibido_por: int = None) -> int:
        """Registra un detalle de pago (efectivo o QR)"""
        query = """
            INSERT INTO pago_detalles 
            (pago_id, numero_cuota, monto, metodo_pago, numero_comprobante, 
             fecha_pago, hora_pago, recibido_por)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME, %s)
            RETURNING id
        """
        result = db.execute(query, (pago_id, numero_cuota, monto, metodo_pago, 
                                    numero_comprobante, recibido_por))
        
        # Actualizar monto_pagado y cuotas_pagadas en la tabla pagos
        query_update = """
            UPDATE pagos 
            SET monto_pagado = monto_pagado + %s,
                cuotas_pagadas = cuotas_pagadas + 1,
                estado = CASE 
                    WHEN monto_pagado + %s >= monto_total THEN 'pagado_total'
                    WHEN monto_pagado + %s > 0 THEN 'pagado_parcial'
                    ELSE estado
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        db.execute(query_update, (monto, monto, monto, pago_id), fetch=False)
        
        return result[0]['id']
    
    @classmethod
    def get_detalles(cls, pago_id: int) -> List[Dict]:
        """Obtiene detalles de pagos (cuotas)"""
        query = """
            SELECT pd.*, u.nombre as recibido_por_nombre
            FROM pago_detalles pd
            LEFT JOIN usuarios u ON pd.recibido_por = u.id
            WHERE pd.pago_id = %s
            ORDER BY pd.numero_cuota
        """
        return db.execute(query, (pago_id,))
    
    @classmethod
    def find_by_estado(cls, estado: str) -> List[Dict]:
        """Obtiene pagos por estado"""
        return cls.find_all({'estado': estado})
    
    @classmethod
    def find_pendientes(cls) -> List[Dict]:
        """Obtiene pagos pendientes"""
        query = f"""
            SELECT * FROM {cls.table_name} 
            WHERE estado IN ('pendiente', 'pagado_parcial')
            ORDER BY fecha_vencimiento ASC
        """
        return db.execute(query)