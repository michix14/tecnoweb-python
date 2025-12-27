"""
Modelo base para todos los modelos de datos
"""
from config. database import db

class BaseModel:
    """Clase base para modelos de datos"""
    
    table_name = None
    fields = []
    
    @classmethod
    def find_all(cls):
        """
        Obtiene todos los registros de la tabla
        
        Returns:
            list: Lista de dicts con los registros
        """
        query = f"SELECT * FROM {cls. table_name}"
        result = db.execute(query, fetch_all=True)
        return result if result is not None else []
    
    @classmethod
    def find_by_id(cls, id):
        """
        Busca un registro por ID
        
        Args:
            id (int): ID del registro
        
        Returns:
            dict:  Registro encontrado o None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE id = %s"
        return db.execute(query, (id,), fetch_one=True)
    
    @classmethod
    def create(cls, data):
        """
        Crea un nuevo registro
        
        Args:
            data (dict): Datos del registro
        
        Returns:
            int: ID del registro creado o None
        """
        # Filtrar solo campos válidos
        valid_data = {k: v for k, v in data.items() if k in cls.fields and k != 'id'}
        
        if not valid_data: 
            return None
        
        # Construir query
        columns = ', '.join(valid_data.keys())
        placeholders = ', '.join(['%s'] * len(valid_data))
        query = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders}) RETURNING id"
        
        # Ejecutar
        result = db.execute(query, tuple(valid_data.values()), fetch_one=True)
        return result['id'] if result else None
    
    @classmethod
    def update(cls, id, data):
        """
        Actualiza un registro
        
        Args:
            id (int): ID del registro
            data (dict): Datos a actualizar
        
        Returns: 
            bool: True si se actualizó, False si no
        """
        # Filtrar solo campos válidos
        valid_data = {k: v for k, v in data.items() if k in cls.fields and k != 'id'}
        
        if not valid_data:
            return False
        
        # Construir query
        set_clause = ', '.join([f"{k} = %s" for k in valid_data.keys()])
        query = f"UPDATE {cls.table_name} SET {set_clause} WHERE id = %s"
        
        # Ejecutar
        params = tuple(valid_data.values()) + (id,)
        rowcount = db.execute(query, params)
        
        return rowcount > 0 if rowcount is not None else False
    
    @classmethod
    def delete(cls, id):
        """
        Elimina un registro
        
        Args:
            id (int): ID del registro
        
        Returns:
            bool: True si se eliminó, False si no
        """
        query = f"DELETE FROM {cls.table_name} WHERE id = %s"
        rowcount = db.execute(query, (id,))
        return rowcount > 0 if rowcount is not None else False
    
    @classmethod
    def count(cls):
        """
        Cuenta total de registros
        
        Returns:
            int:  Número de registros
        """
        query = f"SELECT COUNT(*) as total FROM {cls.table_name}"
        result = db.execute(query, fetch_one=True)
        return result['total'] if result else 0
    
    @classmethod
    def exists(cls, id):
        """
        Verifica si existe un registro con el ID dado
        
        Args:
            id (int): ID a verificar
        
        Returns: 
            bool: True si existe, False si no
        """
        query = f"SELECT EXISTS(SELECT 1 FROM {cls.table_name} WHERE id = %s) as exists"
        result = db.execute(query, (id,), fetch_one=True)
        return result['exists'] if result else False