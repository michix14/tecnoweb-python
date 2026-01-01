"""
Analizador léxico (Lexer) para el sistema de taller mecánico
"""
from typing import List
from . token import Token, TokenType


class Lexer:
    """Analizador léxico para comandos del sistema"""
    
    # Mapeo de palabras clave (case-insensitive)
    KEYWORDS = {
        # Entidades
        'usuario': TokenType. USUARIO,
        'vehiculo': TokenType.VEHICULO,
        'servicio': TokenType.SERVICIO,
        'cita': TokenType.CITA,
        'diagnostico': TokenType.DIAGNOSTICO,
        'orden': TokenType.ORDEN,
        'pago': TokenType.PAGO,
        
        # Subtipos
        'cliente': TokenType.CLIENTE,
        'mecanico': TokenType.MECANICO,
        'secretaria': TokenType.SECRETARIA,
        'propietario': TokenType.PROPIETARIO,
        
        # Acciones
        'mostrar': TokenType.MOSTRAR,
        'agregar': TokenType.AGREGAR,
        'modificar': TokenType.MODIFICAR,
        'eliminar': TokenType.ELIMINAR,
        'ver': TokenType.VER,
        'reporte': TokenType.REPORTE,
        
        # Especiales
        'ayuda': TokenType.AYUDA,
        'salir': TokenType.SALIR,
        'limpiar': TokenType.LIMPIAR,
        'clear': TokenType.LIMPIAR,
        'exit': TokenType. SALIR,
        'help': TokenType.AYUDA,
    }
    
    def __init__(self, text: str):
        self.text = text. strip()
        self.pos = 0
        self.current_char = self.text[0] if self.text else None
    
    def advance(self):
        """Avanza al siguiente carácter"""
        self.pos += 1
        if self.pos < len(self. text):
            self.current_char = self.text[self. pos]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        """Salta espacios en blanco"""
        while self. current_char is not None and self.current_char.isspace():
            self.advance()
    
    def read_word(self):
        """Lee una palabra hasta encontrar espacio o símbolo especial"""
        start_pos = self.pos
        result = ''
        
        # Leer caracteres alfanuméricos y algunos símbolos permitidos
        while (self.current_char is not None and 
               not self.current_char.isspace() and 
               self.current_char not in '[];'):
            result += self.current_char
            self.advance()
        
        return result, start_pos
    
    def read_bracket_content(self):
        """Lee el contenido dentro de corchetes, separando por punto y coma"""
        start_pos = self.pos
        params = []
        current_param = ''
        
        # Saltar '['
        self.advance()
        
        while self.current_char is not None and self.current_char != ']':
            if self.current_char == ';':
                # Guardar parámetro acumulado (trimmed)
                param = current_param.strip()
                if param:
                    # Intentar convertir a número
                    try:
                        if '.' in param:
                            params.append(float(param))
                        else:
                            params.append(int(param))
                    except ValueError:
                        params.append(param)
                
                current_param = ''
                self. advance()
            else:
                current_param += self.current_char
                self.advance()
        
        # Agregar último parámetro
        param = current_param.strip()
        if param:
            try: 
                if '.' in param:
                    params.append(float(param))
                else: 
                    params.append(int(param))
            except ValueError: 
                params.append(param)
        
        # Saltar ']'
        if self.current_char == ']':
            self.advance()
        
        return params, start_pos
    
    def tokenize(self) -> List[Token]:
        """Convierte el texto en lista de tokens"""
        tokens = []
        
        while self.current_char is not None:
            # Saltar espacios en blanco
            self.skip_whitespace()
            
            if self.current_char is None:
                break
            
            # Corchete de apertura [ - leer todo el contenido
            if self. current_char == '[':
                params, start_pos = self.read_bracket_content()
                
                # Agregar tokens:  LBRACKET, params, RBRACKET
                tokens.append(Token(TokenType. LBRACKET, '[', start_pos))
                
                for i, param in enumerate(params):
                    if isinstance(param, (int, float)):
                        tokens.append(Token(TokenType. NUMBER, param, start_pos))
                    else:
                        tokens.append(Token(TokenType.STRING, param, start_pos))
                    
                    # Agregar punto y coma entre parámetros (excepto el último)
                    if i < len(params) - 1:
                        tokens.append(Token(TokenType.SEMICOLON, ';', start_pos))
                
                tokens.append(Token(TokenType.RBRACKET, ']', start_pos))
                continue
            
            # Leer palabra o número
            word, start_pos = self.read_word()
            
            if not word:
                # Si no se leyó nada, avanzar para evitar bucle infinito
                self.advance()
                continue
            
            # Verificar si es una keyword (case-insensitive)
            word_lower = word.lower()
            token_type = self.KEYWORDS.get(word_lower)
            
            if token_type: 
                # Es una keyword - guardar el valor original
                tokens. append(Token(token_type, word, start_pos))
            else:
                # Intentar convertir a número
                try: 
                    if '.' in word:
                        value = float(word)
                        tokens.append(Token(TokenType.NUMBER, value, start_pos))
                    else:
                        value = int(word)
                        tokens.append(Token(TokenType. NUMBER, value, start_pos))
                except ValueError:
                    # Es un string
                    tokens.append(Token(TokenType. STRING, word, start_pos))
        
        # Agregar EOF al final
        tokens.append(Token(TokenType.EOF, '', self.pos))
        return tokens


# Función helper para mantener compatibilidad
def tokenize(text: str) -> List[Token]:
    """
    Función helper para tokenizar texto
    
    Args: 
        text (str): Texto del comando
    
    Returns: 
        List[Token]: Lista de tokens
    """
    lexer = Lexer(text)
    return lexer.tokenize()