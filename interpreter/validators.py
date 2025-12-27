from typing import Any, List
import re
from datetime import datetime

class ValidationError(Exception):
    """Excepción para errores de validación"""
    pass

class ParameterValidator: 
    """Validador de parámetros de comandos"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida formato de teléfono"""
        # Acepta:   70123456, +591 70123456, etc.
        pattern = r'^[\+]?[0-9\s\-\(\)]{7,20}$'
        return bool(re.match(pattern, str(phone)))
    
    @staticmethod
    def validate_placa(placa: str) -> bool:
        """Valida formato de placa (Bolivia:  XXX-9999)"""
        pattern = r'^[A-Z]{2,3}-[0-9]{4}$'
        return bool(re.match(pattern, str(placa).upper()))
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Valida formato de fecha (YYYY-MM-DD)"""
        try:
            datetime.strptime(str(date_str), '%Y-%m-%d')
            return True
        except ValueError: 
            return False
    
    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Valida formato de hora (HH:MM)"""
        try:
            datetime.strptime(str(time_str), '%H:%M')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_tipo_usuario(tipo: str) -> bool:
        """Valida tipo de usuario"""
        return str(tipo).lower() in ['propietario', 'secretaria', 'mecanico', 'cliente']
    
    @staticmethod
    def validate_number(value: Any, min_value: float = None, max_value: float = None) -> bool:
        """Valida que sea un número y esté en rango"""
        try:
            num = float(value)
            if min_value is not None and num < min_value:
                return False
            if max_value is not None and num > max_value: 
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_required_params(params: List, expected_count: int, entity:  str, action: str) -> None:
        """Valida que se proporcionen todos los parámetros requeridos"""
        if len(params) != expected_count:
            raise ValidationError(
                f"Se esperaban {expected_count} parámetros para '{entity} {action}', "
                f"pero se recibieron {len(params)}"
            )