"""
Módulo de conexión a la base de datos PostgreSQL
"""
import psycopg2
from psycopg2 import pool
import logging
from config.settings import settings

class Database:
    """Clase para manejar la conexión a PostgreSQL"""
    
    def __init__(self):
        self.logger = logging.getLogger('Database')
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Inicializa el pool de conexiones"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # Mínimo de conexiones
                10,  # Máximo de conexiones
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD
            )
            
            if self.connection_pool:
                self.logger.info(f"✅ Pool de conexiones creado:  {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
            else:
                self.logger. error("❌ No se pudo crear el pool de conexiones")
                
        except Exception as e:
            self.logger.error(f"❌ Error creando pool de conexiones: {e}")
            self.connection_pool = None
    
    def get_connection(self):
        """
        Obtiene una conexión del pool
        
        Returns: 
            psycopg2.connection: Conexión a la BD o None si falla
        """
        try:
            if self.connection_pool:
                conn = self.connection_pool.getconn()
                if conn:
                    return conn
                else:
                    self.logger.error("❌ No se pudo obtener conexión del pool")
                    return None
            else:
                # Si no hay pool, crear conexión directa
                self.logger.warning("⚠️ Pool no disponible, creando conexión directa...")
                return psycopg2.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    database=settings.DB_NAME,
                    user=settings. DB_USER,
                    password=settings.DB_PASSWORD
                )
        except Exception as e:
            self.logger.error(f"❌ Error obteniendo conexión: {e}")
            return None
    
    def return_connection(self, conn):
        """
        Retorna una conexión al pool
        
        Args:
            conn: Conexión a retornar
        """
        try:
            if self.connection_pool and conn:
                self.connection_pool.putconn(conn)
        except Exception as e:
            self.logger.error(f"❌ Error retornando conexión al pool: {e}")
    
    def close_all_connections(self):
        """Cierra todas las conexiones del pool"""
        try:
            if self.connection_pool:
                self.connection_pool.closeall()
                self.logger.info("✅ Todas las conexiones cerradas")
        except Exception as e:
            self.logger.error(f"❌ Error cerrando conexiones: {e}")
    
    def execute(self, query, params=None, fetch_one=False, fetch_all=False):
        """
        Ejecuta una query SQL
        
        Args:
            query (str): Query SQL
            params (tuple/list): Parámetros de la query
            fetch_one (bool): Retorna solo un registro como dict
            fetch_all (bool): Retorna todos los registros como lista de dicts
        
        Returns:
            dict/list/int: Resultados según el tipo de query
        """
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            
            if not conn: 
                self.logger.error("❌ No se pudo obtener conexión")
                return None
            
            cursor = conn. cursor()
            cursor.execute(query, params or ())
            
            # Si es un SELECT que retorna un registro
            if fetch_one: 
                result = cursor.fetchone()
                if result:
                    # Convertir a dict
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
            
            # Si es un SELECT que retorna múltiples registros
            elif fetch_all:
                results = cursor.fetchall()
                if results:
                    # Convertir a lista de dicts
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in results]
                return []
            
            # Si es INSERT/UPDATE/DELETE
            else:
                conn. commit()
                return cursor.rowcount
                
        except Exception as e:
            self.logger. error(f"❌ Error ejecutando query: {e}")
            self.logger.error(f"   Query: {query}")
            self.logger.error(f"   Params: {params}")
            if conn:
                conn.rollback()
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.return_connection(conn)
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Método legacy para compatibilidad
        
        Args:
            query (str): Query SQL a ejecutar
            params (tuple): Parámetros para la query
            fetch (bool): Si debe hacer fetch de resultados
        
        Returns: 
            list: Resultados de la query o None si falla
        """
        return self. execute(query, params, fetch_all=fetch)


# Instancia global
db = Database()