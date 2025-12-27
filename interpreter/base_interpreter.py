from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from lexer.parser import Command

class BaseInterpreter(ABC):
    """Clase base abstracta para intérpretes"""
    
    @abstractmethod
    def interpret(self, command: Command, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Interpreta y ejecuta un comando
        
        Args: 
            command: Comando parseado
            context: Contexto de ejecución (sesión, permisos, etc.)
        
        Returns:
            Dict con resultado:   {'success': bool, 'message': str, 'data': Any}
        """
        pass
    
    @abstractmethod
    def validate(self, command: Command) -> bool:
        """
        Valida que el comando sea ejecutable
        
        Args:  
            command: Comando a validar
        
        Returns: 
            True si es válido, False en caso contrario
        """
        pass
    
    def format_error(self, message: str) -> Dict[str, Any]:
        """Formatea un mensaje de error"""
        return {
            'success': False,
            'message':  message,
            'data': None
        }
    
    def format_success(self, message: str, data: Any = None) -> Dict[str, Any]:
        """Formatea un mensaje de éxito"""
        return {
            'success': True,
            'message': message,
            'data': data
        }