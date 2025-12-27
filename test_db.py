#!/usr/bin/env python
"""
Script dedicado para probar solo la integración con BD
"""
import sys
import os

# Agregar path
sys.path.insert(0, os.path.dirname(os. path.abspath(__file__)))

# Cargar . env
from dotenv import load_dotenv
load_dotenv()

print("\n" + "╔" + "═" * 68 + "╗")
print("║" + " " * 15 + "TEST DE CONEXIÓN A BASE DE DATOS" + " " * 21 + "║")
print("╚" + "═" * 68 + "╝\n")

# 1. Verificar variables de entorno
print("📋 Variables de entorno:")
print(f"   DB_HOST: {os.getenv('DB_HOST')}")
print(f"   DB_PORT: {os.getenv('DB_PORT')}")
print(f"   DB_NAME:  {os.getenv('DB_NAME')}")
print(f"   DB_USER: {os. getenv('DB_USER')}")
print()

# 2. Test de conexión directa con psycopg2
print("🔌 Test 1: Conexión directa con psycopg2")
print("─" * 70)

try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    print("✅ Conexión psycopg2 exitosa")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"✅ PostgreSQL:  {version[: 60]}...")
    
    cursor.close()
    conn.close()
    
except Exception as e: 
    print(f"❌ Error: {e}")
    sys.exit(1)

print()

# 3. Test con nuestro módulo database
print("🔌 Test 2: Conexión con módulo database. py")
print("─" * 70)

try:
    from config.database import db
    
    conn = db.get_connection()
    
    if conn:
        print("✅ Conexión database.py exitosa")
        conn.close()
    else:
        print("❌ get_connection() retornó None")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error:  {e}")
    sys.exit(1)

print()

# 4. Test con modelos
print("🔌 Test 3: Consultas con modelos")
print("─" * 70)

try:
    from models.usuario import Usuario
    from models.vehiculo import Vehiculo
    from models. servicio import Servicio
    from models.cita import Cita
    
    modelos = [
        ('Usuario', Usuario),
        ('Vehículo', Vehiculo),
        ('Servicio', Servicio),
        ('Cita', Cita)
    ]
    
    for nombre, modelo in modelos:
        try:
            registros = modelo.find_all()
            print(f"✅ {nombre}: {len(registros)} registros")
        except Exception as e:
            print(f"❌ {nombre}: Error - {e}")
    
except Exception as e:
    print(f"❌ Error general: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("╔" + "═" * 68 + "╗")
print("║" + " " * 20 + "🎉 TODOS LOS TESTS PASARON" + " " * 21 + "║")
print("╚" + "═" * 68 + "╝\n")

# 5. Ejecutar tests unitarios de BD
print("🧪 Ejecutando tests unitarios de integración...")
print("="*70 + "\n")

import unittest
from tests.test_models import TestDatabaseIntegration

suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseIntegration)
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

sys.exit(0 if result. wasSuccessful() else 1)