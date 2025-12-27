"""
Tests para el intérprete de comandos
"""
import unittest
import sys
import os

# Agregar directorio raíz al path
sys. path.insert(0, os. path.dirname(os.path. dirname(os.path.abspath(__file__))))

from interpreter.command_interpreter import CommandInterpreter
from interpreter.validators import ParameterValidator, ValidationError
from lexer.parser import Command

class TestParameterValidator(unittest.TestCase):
    """Tests para validadores de parámetros"""
    
    def test_validate_email_valid(self):
        """Test validación de email válido"""
        self.assertTrue(ParameterValidator. validate_email('test@example.com'))
        self.assertTrue(ParameterValidator.validate_email('user. name@domain.co.uk'))
        self.assertTrue(ParameterValidator.validate_email('user+tag@example.com'))
    
    def test_validate_email_invalid(self):
        """Test validación de email inválido"""
        self.assertFalse(ParameterValidator.validate_email('invalid-email'))
        self.assertFalse(ParameterValidator.validate_email('missing@domain'))
        self.assertFalse(ParameterValidator.validate_email('@nodomain.com'))
        self.assertFalse(ParameterValidator.validate_email('no-at-sign. com'))
    
    def test_validate_phone_valid(self):
        """Test validación de teléfono válido"""
        self.assertTrue(ParameterValidator.validate_phone('70123456'))
        self.assertTrue(ParameterValidator.validate_phone('+591 70123456'))
        self.assertTrue(ParameterValidator.validate_phone('591-70-123456'))
    
    def test_validate_phone_invalid(self):
        """Test validación de teléfono inválido"""
        self. assertFalse(ParameterValidator.validate_phone('123'))  # Muy corto
        self.assertFalse(ParameterValidator. validate_phone('abc'))
    
    def test_validate_placa_valid(self):
        """Test validación de placa válida (Bolivia)"""
        self.assertTrue(ParameterValidator.validate_placa('SCZ-1234'))
        self.assertTrue(ParameterValidator. validate_placa('LPZ-5678'))
        self.assertTrue(ParameterValidator.validate_placa('scz-1234'))  # Case insensitive
    
    def test_validate_placa_invalid(self):
        """Test validación de placa inválida"""
        self.assertFalse(ParameterValidator.validate_placa('1234-SCZ'))
        self.assertFalse(ParameterValidator. validate_placa('SCZ1234'))
        self.assertFalse(ParameterValidator. validate_placa('INVALID'))
    
    def test_validate_date_valid(self):
        """Test validación de fecha válida"""
        self.assertTrue(ParameterValidator.validate_date('2025-01-15'))
        self.assertTrue(ParameterValidator.validate_date('2024-12-31'))
    
    def test_validate_date_invalid(self):
        """Test validación de fecha inválida"""
        self.assertFalse(ParameterValidator.validate_date('15-01-2025'))
        self.assertFalse(ParameterValidator.validate_date('2025/01/15'))
        self.assertFalse(ParameterValidator.validate_date('invalid'))
    
    def test_validate_time_valid(self):
        """Test validación de hora válida"""
        self.assertTrue(ParameterValidator.validate_time('09:00'))
        self.assertTrue(ParameterValidator.validate_time('23:59'))
        self.assertTrue(ParameterValidator.validate_time('00:00'))
    
    def test_validate_time_invalid(self):
        """Test validación de hora inválida"""
        self.assertFalse(ParameterValidator.validate_time('25:00'))
        self.assertFalse(ParameterValidator.validate_time('9:00'))  # Debe ser 09:00
        self.assertFalse(ParameterValidator. validate_time('invalid'))
    
    def test_validate_tipo_usuario_valid(self):
        """Test validación de tipo de usuario válido"""
        self.assertTrue(ParameterValidator.validate_tipo_usuario('cliente'))
        self.assertTrue(ParameterValidator.validate_tipo_usuario('mecanico'))
        self.assertTrue(ParameterValidator.validate_tipo_usuario('secretaria'))
        self.assertTrue(ParameterValidator.validate_tipo_usuario('propietario'))
    
    def test_validate_tipo_usuario_invalid(self):
        """Test validación de tipo de usuario inválido"""
        self.assertFalse(ParameterValidator. validate_tipo_usuario('admin'))
        self.assertFalse(ParameterValidator.validate_tipo_usuario('usuario'))
        self.assertFalse(ParameterValidator.validate_tipo_usuario('invalid'))
    
    def test_validate_number_valid(self):
        """Test validación de número válido"""
        self.assertTrue(ParameterValidator.validate_number(100))
        self.assertTrue(ParameterValidator.validate_number('200'))
        self.assertTrue(ParameterValidator.validate_number(50.5))
    
    def test_validate_number_with_range(self):
        """Test validación de número con rango"""
        self.assertTrue(ParameterValidator.validate_number(50, min_value=0, max_value=100))
        self.assertFalse(ParameterValidator.validate_number(150, min_value=0, max_value=100))
        self.assertFalse(ParameterValidator.validate_number(-10, min_value=0))
    
    def test_validate_required_params(self):
        """Test validación de parámetros requeridos"""
        # Debe lanzar ValidationError si no coinciden
        with self.assertRaises(ValidationError):
            ParameterValidator.validate_required_params(
                params=['a', 'b'], 
                expected_count=3, 
                entity='usuario', 
                action='agregar'
            )
        
        # No debe lanzar excepción si coinciden
        try:
            ParameterValidator. validate_required_params(
                params=['a', 'b', 'c'], 
                expected_count=3, 
                entity='usuario', 
                action='agregar'
            )
        except ValidationError:
            self.fail("validate_required_params raised ValidationError unexpectedly")

class TestCommandInterpreter(unittest.TestCase):
    """Tests para el intérprete de comandos"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.interpreter = CommandInterpreter()
        self.context = {
            'user_id': 1,
            'nombre': 'Test User',
            'email': 'test@example.com',
            'tipo':  'propietario'
        }
    
    def test_validate_command_valid(self):
        """Test validación de comando válido"""
        command = Command('usuario', 'mostrar', [])
        self.assertTrue(self.interpreter.validate(command))
    
    def test_validate_command_invalid_entity(self):
        """Test validación con entidad inválida"""
        command = Command('invalid', 'mostrar', [])
        self.assertFalse(self.interpreter.validate(command))
    
    def test_validate_command_invalid_action(self):
        """Test validación con acción inválida"""
        command = Command('usuario', 'invalid', [])
        self.assertFalse(self.interpreter. validate(command))
    
    def test_get_model(self):
        """Test obtención de modelo"""
        from models.usuario import Usuario
        from models.vehiculo import Vehiculo
        
        self.assertEqual(self.interpreter._get_model('usuario'), Usuario)
        self.assertEqual(self. interpreter._get_model('vehiculo'), Vehiculo)
    
    def test_get_entity_key(self):
        """Test normalización de entidad"""
        self.assertEqual(self.interpreter._get_entity_key('cliente'), 'usuario')
        self.assertEqual(self.interpreter._get_entity_key('mecanico'), 'usuario')
        self.assertEqual(self.interpreter._get_entity_key('vehiculo'), 'vehiculo')
    
    def test_format_error(self):
        """Test formateo de error"""
        result = self.interpreter. format_error("Test error")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], "Test error")
        self.assertIsNone(result['data'])
    
    def test_format_success(self):
        """Test formateo de éxito"""
        result = self.interpreter.format_success("Test success", {'id': 1})
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Test success")
        self.assertIsNotNone(result['data'])
        self.assertEqual(result['data']['id'], 1)

class TestInterpreterHandlers(unittest.TestCase):
    """Tests para handlers del intérprete (requieren BD)"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.interpreter = CommandInterpreter()
        self.context = {
            'user_id': 1,
            'nombre': 'Test User',
            'email': 'test@example.com',
            'tipo': 'propietario'
        }
    
    def test_handle_ayuda(self):
        """Test handler de ayuda"""
        command = Command('system', 'ayuda', [])
        result = self.interpreter._handle_ayuda(command, self.context)
        
        self.assertTrue(result['success'])
        self.assertIn('comandos', result['message']. lower())

if __name__ == '__main__': 
    unittest.main(verbosity=2)