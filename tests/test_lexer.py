"""
Tests para el analizador léxico (Lexer y Parser)
"""
import unittest
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer.lexer import Lexer, tokenize
from lexer.parser import Parser, parse_command
from lexer.token import Token, TokenType

class TestLexer(unittest.TestCase):
    """Tests para el Lexer"""
    
    def test_tokenize_simple_command(self):
        """Test tokenización de comando simple"""
        tokens = tokenize("usuario mostrar")
        
        self.assertEqual(len(tokens), 3)  # usuario, mostrar, EOF
        self.assertEqual(tokens[0].type, TokenType. USUARIO)
        self.assertEqual(tokens[1].type, TokenType.MOSTRAR)
        self.assertEqual(tokens[2].type, TokenType.EOF)
    
    def test_tokenize_command_with_params(self):
        """Test tokenización con parámetros"""
        tokens = tokenize("usuario agregar [Juan; juan@mail.com; pass123]")
        
        # Verificar que hay tokens STRING
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertEqual(len(string_tokens), 3)
        self.assertEqual(string_tokens[0].value, 'Juan')
        self.assertEqual(string_tokens[1].value, 'juan@mail.com')
        self.assertEqual(string_tokens[2].value, 'pass123')
    
    def test_tokenize_numbers(self):
        """Test tokenización de números"""
        tokens = tokenize("vehiculo agregar [1; SCZ-1234; Toyota; 2020; 45000]")
        
        number_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
        self.assertGreater(len(number_tokens), 0)
    
    def test_tokenize_special_characters(self):
        """Test con caracteres especiales (ñ, tildes)"""
        tokens = tokenize("usuario agregar [José María; jose@mail.com]")
        
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        self.assertIn('José María', [t.value for t in string_tokens])
    
    def test_keywords_case_insensitive(self):
        """Test que keywords son case-insensitive"""
        tokens1 = tokenize("USUARIO MOSTRAR")
        tokens2 = tokenize("usuario mostrar")
        tokens3 = tokenize("Usuario Mostrar")
        
        self.assertEqual(tokens1[0].type, TokenType.USUARIO)
        self.assertEqual(tokens2[0].type, TokenType. USUARIO)
        self.assertEqual(tokens3[0].type, TokenType.USUARIO)

class TestParser(unittest.TestCase):
    """Tests para el Parser"""
    
    def test_parse_simple_command(self):
        """Test parseo de comando simple"""
        command = parse_command("usuario mostrar")
        
        self.assertIsNotNone(command)
        self.assertEqual(command.entity, 'usuario')
        self.assertEqual(command.action, 'mostrar')
        self.assertEqual(len(command.params), 0)
    
    def test_parse_command_with_id(self):
        """Test parseo con ID"""
        command = parse_command("usuario ver [5]")
        
        self. assertIsNotNone(command)
        self.assertEqual(command. entity, 'usuario')
        self.assertEqual(command.action, 'ver')
        self.assertEqual(len(command.params), 1)
        self.assertEqual(command. params[0], 5)
    
    def test_parse_command_with_multiple_params(self):
        """Test parseo con múltiples parámetros"""
        command = parse_command("usuario agregar [Juan; juan@mail.com; pass123; 70123456; Calle 1; cliente]")
        
        self.assertIsNotNone(command)
        self.assertEqual(command.entity, 'usuario')
        self.assertEqual(command.action, 'agregar')
        self.assertEqual(len(command.params), 6)
        self.assertEqual(command.params[0], 'Juan')
        self.assertEqual(command.params[1], 'juan@mail.com')
        self.assertEqual(command.params[5], 'cliente')
    
    def test_parse_vehiculo_command(self):
        """Test parseo de comando de vehículo"""
        command = parse_command("vehiculo agregar [2; SCZ-1234; Toyota; Corolla; 2020; Blanco; 45000]")
        
        self.assertIsNotNone(command)
        self.assertEqual(command.entity, 'vehiculo')
        self.assertEqual(command. action, 'agregar')
        self.assertEqual(len(command.params), 7)
    
    def test_parse_reporte_command(self):
        """Test parseo de comando reporte"""
        command = parse_command("cita reporte")
        
        self.assertIsNotNone(command)
        self.assertEqual(command.entity, 'cita')
        self.assertEqual(command.action, 'reporte')
    
    def test_parse_invalid_command(self):
        """Test parseo de comando inválido"""
        command = parse_command("asdfghjkl")
        
        # Debe retornar None o lanzar excepción
        self.assertIsNone(command)
    
    def test_parse_cliente_subtype(self):
        """Test parseo de subtipo cliente"""
        command = parse_command("cliente mostrar")
        
        self. assertIsNotNone(command)
        self.assertEqual(command. entity, 'cliente')
        self.assertEqual(command.action, 'mostrar')
    
    def test_parse_mecanico_subtype(self):
        """Test parseo de subtipo mecánico"""
        command = parse_command("mecanico mostrar")
        
        self.assertIsNotNone(command)
        self.assertEqual(command.entity, 'mecanico')
        self.assertEqual(command.action, 'mostrar')

class TestTokenTypes(unittest.TestCase):
    """Tests para tipos de tokens"""
    
    def test_entity_tokens(self):
        """Test que todas las entidades son reconocidas"""
        entities = ['usuario', 'vehiculo', 'servicio', 'cita', 'diagnostico', 'orden', 'pago']
        
        for entity in entities:
            tokens = tokenize(f"{entity} mostrar")
            self.assertNotEqual(tokens[0].type, TokenType.STRING)
    
    def test_action_tokens(self):
        """Test que todas las acciones son reconocidas"""
        actions = ['mostrar', 'agregar', 'modificar', 'eliminar', 'ver', 'reporte']
        
        for action in actions: 
            tokens = tokenize(f"usuario {action}")
            self.assertNotEqual(tokens[1].type, TokenType.STRING)
    
    def test_special_commands(self):
        """Test comandos especiales"""
        special = ['ayuda', 'salir', 'limpiar']
        
        for cmd in special:
            tokens = tokenize(cmd)
            self.assertNotEqual(tokens[0].type, TokenType.STRING)

if __name__ == '__main__': 
    # Ejecutar tests con verbose
    unittest.main(verbosity=2)