from typing import List, Dict, Any

class ResponseFormatter:
    """Formatea respuestas para diferentes salidas"""
    
    @staticmethod
    def format_list(data: List[Dict], title: str = "Resultados") -> Dict[str, Any]:
        """Formatea lista de registros"""
        if not data:  
            return {
                'success': True,
                'message': 'No se encontraron registros',
                'data': []
            }
        
        return {
            'success': True,
            'message': f'Se encontraron {len(data)} registro(s)',
            'data': data
        }
    
    @staticmethod
    def format_detail(data: Dict, title: str = "Detalle") -> Dict[str, Any]:
        """Formatea detalle de un registro"""
        if not data:  
            return {
                'success': False,
                'message': 'Registro no encontrado',
                'data': None
            }
        
        return {
            'success':  True,
            'message': f'{title} encontrado',
            'data':  data
        }
    
    @staticmethod
    def format_success(message: str, data: Any = None) -> Dict[str, Any]:
        """Formatea respuesta exitosa"""
        return {
            'success': True,
            'message': message,
            'data': data
        }
    
    @staticmethod
    def format_error(message: str) -> Dict[str, Any]: 
        """Formatea respuesta de error"""
        return {
            'success': False,
            'message': message,
            'data': None
        }
    
    @staticmethod
    def format_table(data: List[Dict], headers: List[str] = None) -> str:
        """Formatea datos como tabla de texto"""
        if not data: 
            return "No hay datos para mostrar"
        
        from tabulate import tabulate
        
        try:
            if headers:
                return tabulate(data, headers=headers, tablefmt='grid')
            else:
                return tabulate(data, headers='keys', tablefmt='grid')
        except Exception: 
            return str(data)