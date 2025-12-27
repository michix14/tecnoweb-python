"""
Tests para los modelos de datos
NOTA: Estos tests requieren conexión a la base de datos de prueba
"""
import unittest
import sys
import os
from functools import wraps

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os. path.dirname(os.path. abspath(__file__))))

from models. usuario import Usuario
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.cita import Cita


# ============================================================================
# DECORADOR PARA TESTS DE BD
# ============================================================================

def requires_database(func):
    """
    Decorador que salta el test si no hay conexión a BD
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            from config. database import db
            conn = db.get_connection()
            if conn: 
                conn.close()
                return func(self, *args, **kwargs)
            else:
                self.skipTest("Base de datos no disponible")
        except Exception as e:
            self.skipTest(f"Error conectando a BD: {e}")
    return wrapper


# ============================================================================
# TESTS DE USUARIO
# ============================================================================

class TestUsuarioModel(unittest.TestCase):
    """Tests para el modelo Usuario"""
    
    def test_hash_password(self):
        """Test generación de hash de contraseña"""
        password = "test123"
        hashed = Usuario.hash_password(password)
        
        self.assertIsNotNone(hashed)
        self.assertNotEqual(password, hashed)
        self.assertTrue(hashed.startswith('$2b$'))  # bcrypt
        print(f"  ✅ Hash generado:  {hashed[: 20]}...")
    
    def test_verify_password_correct(self):
        """Test verificación de contraseña correcta"""
        password = "test123"
        hashed = Usuario.hash_password(password)
        
        self.assertTrue(Usuario.verify_password(password, hashed))
        print(f"  ✅ Contraseña correcta verificada")
    
    def test_verify_password_incorrect(self):
        """Test verificación de contraseña incorrecta"""
        password = "test123"
        wrong_password = "wrong456"
        hashed = Usuario.hash_password(password)
        
        self. assertFalse(Usuario.verify_password(wrong_password, hashed))
        print(f"  ✅ Contraseña incorrecta rechazada")
    
    def test_password_hash_unique(self):
        """Test que cada hash es único (por el salt)"""
        password = "test123"
        hash1 = Usuario.hash_password(password)
        hash2 = Usuario.hash_password(password)
        
        # Los hashes deben ser diferentes (diferentes salts)
        self.assertNotEqual(hash1, hash2)
        
        # Pero ambos deben verificar correctamente
        self.assertTrue(Usuario.verify_password(password, hash1))
        self.assertTrue(Usuario.verify_password(password, hash2))
        print(f"  ✅ Hashes únicos pero ambos válidos")


# ============================================================================
# TESTS DE VEHÍCULO
# ============================================================================

class TestVehiculoModel(unittest.TestCase):
    """Tests para el modelo Vehículo"""
    
    def test_table_name(self):
        """Test nombre de tabla"""
        self.assertEqual(Vehiculo.table_name, 'vehiculos')
        print(f"  ✅ Tabla:  {Vehiculo.table_name}")
    
    def test_fields_exist(self):
        """Test que los campos esperados existen"""
        expected_fields = ['id', 'cliente_id', 'placa', 'marca', 'modelo']
        
        for field in expected_fields: 
            self.assertIn(field, Vehiculo.fields)
        
        print(f"  ✅ Campos verificados: {', '.join(expected_fields)}")


# ============================================================================
# TESTS DE SERVICIO
# ============================================================================

class TestServicioModel(unittest.TestCase):
    """Tests para el modelo Servicio"""
    
    def test_table_name(self):
        """Test nombre de tabla"""
        self.assertEqual(Servicio. table_name, 'servicios')
        print(f"  ✅ Tabla: {Servicio.table_name}")
    
    def test_fields_exist(self):
        """Test que los campos esperados existen"""
        expected_fields = ['id', 'nombre', 'tipo', 'precio_base']
        
        for field in expected_fields:
            self. assertIn(field, Servicio.fields)
        
        print(f"  ✅ Campos verificados: {', '. join(expected_fields)}")


# ============================================================================
# TESTS DE CITA
# ============================================================================

class TestCitaModel(unittest.TestCase):
    """Tests para el modelo Cita"""
    
    def test_generar_codigo(self):
        """Test que el código tenga el formato correcto"""
        codigo = Cita.generar_codigo()
        
        # Verificar que comienza con CIT-
        self. assertTrue(codigo.startswith('CIT-'), 
                       f"El código debe comenzar con 'CIT-', pero es: {codigo}")
        
        # Verificar formato: CIT-YYYYMMDDHHMMSS-XXXX (23 caracteres total)
        # CIT- (4) + YYYYMMDDHHMMSS (14) + - (1) + XXXX (4) = 23
        self.assertEqual(len(codigo), 23, 
                        f"El código debe tener 23 caracteres, pero tiene {len(codigo)}: {codigo}")
        
        # Verificar formato con regex
        import re
        pattern = r'^CIT-\d{14}-\d{4}$'
        self.assertRegex(codigo, pattern,
                        f"El código no cumple el formato CIT-YYYYMMDDHHMMSS-XXXX:  {codigo}")
        
        print(f"  ✅ Código generado correctamente: {codigo}")
    
    def test_generar_codigo_unique(self):
        """Test que códigos generados son únicos"""
        import time
        
        codigos = set()
        
        # Generar 50 códigos
        for _ in range(50):
            codigo = Cita.generar_codigo()
            codigos.add(codigo)
            time.sleep(0.001)  # 1ms de pausa
        
        # Todos deben ser únicos
        self.assertEqual(len(codigos), 50,
                        f"Se esperaban 50 códigos únicos, se obtuvieron {len(codigos)}")
        
        print(f"  ✅ Generados 50 códigos únicos")


# ============================================================================
# TESTS DE MÉTODOS BASE
# ============================================================================

class TestBaseModelMethods(unittest.TestCase):
    """Tests para métodos del BaseModel"""
    
    def test_model_has_crud_methods(self):
        """Test que los modelos tienen métodos CRUD"""
        crud_methods = ['find_all', 'find_by_id', 'create', 'update', 'delete', 'count']
        
        models = [
            ('Usuario', Usuario),
            ('Vehiculo', Vehiculo),
            ('Servicio', Servicio),
            ('Cita', Cita)
        ]
        
        for model_name, model in models:
            for method in crud_methods:
                self.assertTrue(hasattr(model, method),
                              f"{model_name} debe tener método {method}")
        
        print(f"  ✅ Todos los modelos tienen métodos CRUD:  {', '.join(crud_methods)}")
    
    def test_model_table_names(self):
        """Test que los modelos tienen nombres de tabla correctos"""
        expected = {
            'Usuario': 'usuarios',
            'Vehiculo':  'vehiculos',
            'Servicio': 'servicios',
            'Cita':  'citas'
        }
        
        self.assertEqual(Usuario.table_name, expected['Usuario'])
        self.assertEqual(Vehiculo.table_name, expected['Vehiculo'])
        self.assertEqual(Servicio.table_name, expected['Servicio'])
        self.assertEqual(Cita.table_name, expected['Cita'])
        
        print(f"  ✅ Nombres de tabla correctos")


# ============================================================================
# TESTS DE INTEGRACIÓN CON BD
# ============================================================================

class TestDatabaseIntegration(unittest.TestCase):
    """
    Tests de integración con base de datos
    Se ejecutarán automáticamente si hay conexión a BD
    Se saltarán si no hay conexión disponible
    """
    
    @classmethod
    def setUpClass(cls):
        """Setup antes de todos los tests de la clase"""
        try:
            from config.database import db
            conn = db.get_connection()
            if conn:
                conn. close()
                print("\n  ✅ Conexión a BD disponible - Tests habilitados")
                cls.db_available = True
            else:
                print("\n  ⚠️  BD no disponible - Tests serán saltados")
                cls. db_available = False
        except Exception as e:
            print(f"\n  ⚠️  Error de BD: {e} - Tests serán saltados")
            cls.db_available = False
    
    @requires_database
    def test_find_all_usuarios(self):
        """Test obtener todos los usuarios"""
        usuarios = Usuario.find_all()
        
        self.assertIsInstance(usuarios, list, "find_all() debe retornar una lista")
        
        if len(usuarios) > 0:
            print(f"  ✅ Encontrados {len(usuarios)} usuarios")
            
            # Verificar estructura del primer usuario
            primer_usuario = usuarios[0]
            self.assertIsInstance(primer_usuario, dict, "Cada usuario debe ser un dict")
            
            # Verificar campos requeridos
            campos_requeridos = ['id', 'nombre', 'email', 'tipo']
            for campo in campos_requeridos:
                self.assertIn(campo, primer_usuario, 
                            f"Usuario debe tener campo '{campo}'")
            
            # Mostrar primeros 3 usuarios
            print(f"  📋 Primeros usuarios:")
            for u in usuarios[:3]:
                print(f"     - {u['nombre']} ({u['email']}) - {u['tipo']}")
        else:
            print("  ⚠️  No hay usuarios en la BD")
    
    @requires_database
    def test_find_by_email(self):
        """Test buscar usuario por email"""
        # Primero obtener un email existente
        usuarios = Usuario.find_all()
        
        if len(usuarios) > 0:
            email_existente = usuarios[0]['email']
            
            # Buscar por email
            usuario = Usuario. find_by_email(email_existente)
            
            # Verificaciones
            self.assertIsNotNone(usuario, f"Debe encontrar usuario con email {email_existente}")
            self.assertIsInstance(usuario, dict, "find_by_email() debe retornar un dict")
            self.assertEqual(usuario['email'], email_existente, "El email debe coincidir")
            
            print(f"  ✅ Usuario encontrado: {usuario['nombre']} ({email_existente})")
            
            # Test con email inexistente
            usuario_inexistente = Usuario.find_by_email('noexiste@ejemplo.com')
            self.assertIsNone(usuario_inexistente, 
                            "No debe encontrar usuario con email inexistente")
            print(f"  ✅ Correctamente retorna None para email inexistente")
        else:
            self.skipTest("No hay usuarios en la BD para probar")
    
    @requires_database
    def test_find_by_id(self):
        """Test buscar usuario por ID"""
        usuarios = Usuario.find_all()
        
        if len(usuarios) > 0:
            id_existente = usuarios[0]['id']
            
            # Buscar por ID
            usuario = Usuario.find_by_id(id_existente)
            
            # Verificaciones
            self.assertIsNotNone(usuario, f"Debe encontrar usuario con ID {id_existente}")
            self.assertEqual(usuario['id'], id_existente, "El ID debe coincidir")
            
            print(f"  ✅ Usuario encontrado por ID: {usuario['nombre']}")
            
            # Test con ID inexistente
            usuario_inexistente = Usuario.find_by_id(99999)
            self.assertIsNone(usuario_inexistente, 
                            "No debe encontrar usuario con ID inexistente")
            print(f"  ✅ Correctamente retorna None para ID inexistente")
        else:
            self. skipTest("No hay usuarios en la BD para probar")
    
    @requires_database
    def test_count_usuarios(self):
        """Test contar usuarios"""
        count = Usuario.count()
        
        # Verificaciones
        self.assertIsInstance(count, int, "count() debe retornar un entero")
        self.assertGreaterEqual(count, 0, "count() no puede ser negativo")
        
        print(f"  ✅ Total de usuarios en BD: {count}")
        
        # Verificar que coincide con find_all
        usuarios = Usuario. find_all()
        self.assertEqual(count, len(usuarios), 
                        "count() debe coincidir con len(find_all())")
    
    @requires_database
    def test_vehiculo_operations(self):
        """Test operaciones básicas con vehículos"""
        vehiculos = Vehiculo.find_all()
        
        self. assertIsInstance(vehiculos, list, "find_all() debe retornar lista")
        print(f"  ✅ Encontrados {len(vehiculos)} vehículos")
        
        if len(vehiculos) > 0:
            vehiculo = vehiculos[0]
            campos_esperados = ['id', 'placa', 'marca', 'modelo']
            
            for campo in campos_esperados:
                self.assertIn(campo, vehiculo, 
                            f"Vehículo debe tener campo '{campo}'")
            
            print(f"  📋 Primer vehículo:  {vehiculo. get('placa')} - {vehiculo.get('marca')} {vehiculo.get('modelo')}")
    
    @requires_database
    def test_servicio_operations(self):
        """Test operaciones básicas con servicios"""
        servicios = Servicio.find_all()
        
        self.assertIsInstance(servicios, list, "find_all() debe retornar lista")
        print(f"  ✅ Encontrados {len(servicios)} servicios")
        
        if len(servicios) > 0:
            servicio = servicios[0]
            campos_esperados = ['id', 'nombre', 'descripcion', 'precio_base']
            
            for campo in campos_esperados: 
                self.assertIn(campo, servicio, 
                            f"Servicio debe tener campo '{campo}'")
            
            print(f"  📋 Primer servicio: {servicio.get('nombre')} - Bs.  {servicio.get('precio_base')}")
    
    @requires_database
    def test_cita_operations(self):
        """Test operaciones básicas con citas"""
        citas = Cita.find_all()
        
        self.assertIsInstance(citas, list, "find_all() debe retornar lista")
        print(f"  ✅ Encontradas {len(citas)} citas")
        
        if len(citas) > 0:
            cita = citas[0]
            campos_esperados = ['id', 'codigo', 'fecha', 'hora', 'estado']
            
            for campo in campos_esperados:
                self.assertIn(campo, cita, 
                            f"Cita debe tener campo '{campo}'")
            
            print(f"  📋 Primera cita: {cita.get('codigo')} - {cita.get('fecha')} {cita.get('hora')}")


# ============================================================================
# EJECUTAR TESTS
# ============================================================================

if __name__ == '__main__':
    # Banner inicial
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TESTS DE MODELOS - TALLER MECÁNICO" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    # Configurar runner con más detalle
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen final
    total_tests = result.testsRun
    passed = total_tests - len(result.failures) - len(result.errors) - len(result.skipped)
    failed = len(result.failures)
    errors = len(result. errors)
    skipped = len(result.skipped)
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 23 + "RESUMEN DE TESTS" + " " * 29 + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  ✅ Exitosos:   {passed: 3d} / {total_tests:3d}" + " " * 48 + "║")
    print(f"║  ❌ Fallidos:   {failed:3d} / {total_tests:3d}" + " " * 48 + "║")
    print(f"║  💥 Errores:   {errors:3d} / {total_tests:3d}" + " " * 48 + "║")
    print(f"║  ⏭️  Saltados:   {skipped:3d} / {total_tests:3d}" + " " * 48 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    # Exit code
    if result.wasSuccessful():
        print("🎉 ¡TODOS LOS TESTS PASARON!\n")
        sys.exit(0)
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.\n")
        sys.exit(1)