"""
Parser de comandos del sistema de taller mecánico
"""
from typing import List, Optional, Any
from dataclasses import dataclass, field
from . token import Token, TokenType
from . lexer import tokenize


@dataclass
class Command:
    """Representa un comando parseado"""
    entity: str
    action: str
    params: List[Any] = field(default_factory=list)
    subtype: Optional[str] = None
    
    def __repr__(self):
        return f"Command(entity='{self.entity}', action='{self.action}', params={self.params}, subtype='{self.subtype}')"


class Parser:
    """Parser de comandos"""
    
    # Entidades válidas
    ENTITIES = [
        TokenType.USUARIO, TokenType.VEHICULO, TokenType.SERVICIO,
        TokenType. CITA, TokenType.DIAGNOSTICO, TokenType.ORDEN, TokenType.PAGO
    ]
    
    # Subtipos de usuario
    SUBTYPES = [
        TokenType.CLIENTE, TokenType.MECANICO, 
        TokenType.SECRETARIA, TokenType.PROPIETARIO
    ]
    
    # Acciones válidas
    ACTIONS = [
        TokenType.MOSTRAR, TokenType.AGREGAR, TokenType.MODIFICAR,
        TokenType. ELIMINAR, TokenType.VER, TokenType.REPORTE
    ]
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t. type != TokenType.EOF]
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        """Avanza al siguiente token"""
        self. pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def parse(self) -> Optional[Command]:
        """Parsea los tokens en un comando"""
        try:
            if not self.tokens or len(self.tokens) < 2:
                return None
            
            entity = None
            action = None
            subtype = None
            params = []
            
            # Verificar primer token
            if self.current_token.type in self.SUBTYPES:
                # Es un subtipo de usuario (cliente, mecanico, etc)
                subtype = self.current_token.value
                entity = 'usuario'
                self.advance()
                
                # Siguiente debe ser acción
                if self.current_token and self.current_token.type in self.ACTIONS:
                    action = self.current_token. value
                    self.advance()
                
                # Agregar subtipo como primer parámetro
                params.append(subtype)
                
            elif self.current_token.type in self.ENTITIES:
                # Es una entidad normal
                entity = self.current_token.value
                self.advance()
                
                # Siguiente debe ser acción
                if self.current_token and self.current_token.type in self. ACTIONS:
                    action = self.current_token.value
                    self.advance()
            else:
                return None
            
            # Extraer parámetros (tokens dentro de corchetes)
            in_bracket = False
            while self.current_token:
                if self.current_token.type == TokenType.LBRACKET:
                    in_bracket = True
                elif self.current_token.type == TokenType.RBRACKET: 
                    in_bracket = False
                elif self.current_token.type == TokenType.SEMICOLON: 
                    pass  # Ignorar punto y coma
                elif in_bracket:
                    # Agregar valor del token como parámetro
                    params.append(self.current_token.value)
                
                self.advance()
            
            return Command(
                entity=entity,
                action=action,
                params=params,
                subtype=subtype
            )
            
        except Exception as e:
            print(f"❌ Error en parser: {e}")
            return None


def parse_command(text: str) -> Optional[Command]:
    """
    Parsea un comando de texto
    
    Args:
        text (str): Texto del comando
    
    Returns:
        Command:  Comando parseado o None si hay error
    """
    try:
        tokens = tokenize(text)
        parser = Parser(tokens)
        return parser.parse()
    except Exception as e: 
        print(f"❌ Error al parsear comando: {e}")
        return None