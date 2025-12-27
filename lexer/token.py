from enum import Enum
from dataclasses import dataclass
from typing import Any

class TokenType(Enum):
    """Tipos de tokens del lenguaje de comandos"""
    
    # Entidades
    USUARIO = 'usuario'
    VEHICULO = 'vehiculo'
    SERVICIO = 'servicio'
    CITA = 'cita'
    DIAGNOSTICO = 'diagnostico'
    ORDEN = 'orden'
    PAGO = 'pago'
    
    # Subtipos de usuario
    CLIENTE = 'cliente'
    MECANICO = 'mecanico'
    SECRETARIA = 'secretaria'
    PROPIETARIO = 'propietario'
    
    # Acciones CRUD
    MOSTRAR = 'mostrar'
    AGREGAR = 'agregar'
    MODIFICAR = 'modificar'
    ELIMINAR = 'eliminar'
    VER = 'ver'
    REPORTE = 'reporte'
    
    # Acciones especiales
    AYUDA = 'ayuda'
    SALIR = 'salir'
    LIMPIAR = 'limpiar'
    
    # Símbolos
    LBRACKET = '['
    RBRACKET = ']'
    SEMICOLON = ';'
    
    # Literales
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    
    # Otros
    EOF = 'EOF'
    UNKNOWN = 'UNKNOWN'

@dataclass
class Token:
    """Representa un token del lenguaje"""
    type: TokenType
    value: Any
    position: int
    
    def __repr__(self):
        return f"Token({self.type. value}, {self.value}, pos={self.position})"