from typing import Dict, Any, Optional, List
import logging
from . base_interpreter import BaseInterpreter
from .validators import ParameterValidator, ValidationError
from lexer.parser import Command
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.cita import Cita
from models.diagnostico import Diagnostico
from models.orden_trabajo import OrdenTrabajo
from models.pago import Pago

class CommandInterpreter(BaseInterpreter):
    """Intérprete de comandos del sistema"""
    
    # Mapeo de entidades a modelos
    MODELS = {
        'usuario': Usuario,
        'cliente': Usuario,
        'mecanico': Usuario,
        'secretaria': Usuario,
        'propietario': Usuario,
        'vehiculo': Vehiculo,
        'servicio': Servicio,
        'cita':   Cita,
        'diagnostico': Diagnostico,
        'orden':  OrdenTrabajo,
        'pago': Pago,
    }
    
    # Campos por entidad
    ENTITY_FIELDS = {
        'usuario': ['nombre', 'email', 'password', 'telefono', 'direccion', 'tipo'],
        'vehiculo': ['cliente_id', 'placa', 'marca', 'modelo', 'anio', 'color', 'kilometraje'],
        'servicio':   ['nombre', 'descripcion', 'tipo', 'precio_base', 'duracion_estimada'],
        'cita':   ['cliente_id', 'vehiculo_id', 'fecha', 'hora', 'motivo'],
        'diagnostico': ['cita_id', 'mecanico_id', 'fecha_diagnostico', 'descripcion_problema', 'diagnostico', 'recomendaciones'],
        'orden': ['diagnostico_id', 'mecanico_id', 'fecha_inicio', 'costo_mano_obra', 'costo_repuestos'],
        'pago': ['orden_trabajo_id', 'monto_total', 'tipo_pago', 'numero_cuotas'],
    }
    
    # Validadores por campo
    FIELD_VALIDATORS = {
        'email': ParameterValidator.validate_email,
        'telefono': ParameterValidator.validate_phone,
        'placa': ParameterValidator.validate_placa,
        'fecha':   ParameterValidator.validate_date,
        'fecha_diagnostico': ParameterValidator.validate_date,
        'fecha_inicio': ParameterValidator. validate_date,
        'hora': ParameterValidator.validate_time,
        'tipo':  lambda v:   ParameterValidator.validate_tipo_usuario(v),
    }
    
    def __init__(self):
        self.logger = logging.getLogger('CommandInterpreter')
        self.validator = ParameterValidator()
    
    def interpret(self, command: Command, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Interpreta y ejecuta un comando"""
        try:
            # Validar
            if not self.validate(command):
                return self. format_error(f"Comando inválido: {command}")
            
            # Log
            self.logger.info(f"🔧 Interpretando:   {command.entity} {command.action}")
            
            # Obtener handler
            handler_name = f"_handle_{command.action}"
            if not hasattr(self, handler_name):
                return self.format_error(f"Acción no soportada: {command.action}")
            
            handler = getattr(self, handler_name)
            
            # Ejecutar
            result = handler(command, context)
            
            # Log resultado
            status = "✅" if result['success'] else "❌"
            self.logger. info(f"{status} Resultado: {result['message']}")
            
            return result
        
        except ValidationError as e: 
            return self.format_error(str(e))
        except Exception as e:
            self. logger.error(f"❌ Error en intérprete: {e}", exc_info=True)
            return self.format_error(f"Error interno: {str(e)}")
    
    def validate(self, command: Command) -> bool:
        """Valida que el comando sea ejecutable"""
        # Validar entidad
        if command.entity not in self.MODELS and command.entity != 'system':
            return False
        
        # Validar acción
        valid_actions = ['mostrar', 'ver', 'agregar', 'modificar', 'eliminar', 'reporte', 'ayuda']
        if command.action not in valid_actions:
            return False
        
        return True
    
    # ========================================================================
    # HANDLERS DE ACCIONES
    # ========================================================================
    
    def _handle_mostrar(self, command: Command, context: Dict) -> Dict[str, Any]:
        """Handler para acción MOSTRAR (listar todos)"""
        model = self._get_model(command.entity)
        
        # Si es subtipo de usuario, filtrar por tipo
        if command. entity in ['cliente', 'mecanico', 'secretaria', 'propietario']:
            data = Usuario.find_by_tipo(command.entity)
        else:
            data = model.find_all()
        
        return self.format_success(
            f"Se encontraron {len(data)} registro(s)",
            data
        )
    
    def _handle_ver(self, command:  Command, context:   Dict) -> Dict[str, Any]:
        """Handler para acción VER (detalle de uno)"""
        # Validar parámetros
        try:
            self.validator.validate_required_params(command.params, 1, command.entity, 'ver')
        except ValidationError as e:
            return self. format_error(str(e))
        
        # Obtener ID
        try:
            id_registro = int(command.params[0])
        except ValueError:
            return self.format_error("El ID debe ser un número entero")
        
        # Buscar
        model = self._get_model(command.entity)
        data = model.find_by_id(id_registro)
        
        if not data:
            return self.format_error(f"No se encontró {command.entity} con ID {id_registro}")
        
        return self.format_success(
            f"{command.entity. capitalize()} encontrado",
            data
        )
    
    def _handle_agregar(self, command: Command, context:  Dict) -> Dict[str, Any]:
        """Handler para acción AGREGAR (crear)"""
        entity_key = self._get_entity_key(command.entity)
        fields = self.ENTITY_FIELDS. get(entity_key, [])
        
        # Validar cantidad de parámetros
        try:  
            self.validator.validate_required_params(command.params, len(fields), command.entity, 'agregar')
        except ValidationError as e:
            return self.format_error(str(e))
        
        # Crear diccionario de datos
        data = {field: command.params[i] for i, field in enumerate(fields)}
        
        # Validar campos
        validation_errors = self._validate_fields(data)
        if validation_errors:  
            return self.format_error("Errores de validación:   " + ", ".join(validation_errors))
        
        # Agregar tipo si es usuario
        if entity_key == 'usuario': 
            data['tipo'] = command. entity
        
        # Generar código si es necesario
        model = self._get_model(command.entity)
        if hasattr(model, 'generar_codigo'):
            data['codigo'] = model.generar_codigo()
        
        # Crear registro
        try:
            if entity_key == 'usuario':  
                nuevo_id = Usuario.create_with_password(data)
            else:
                nuevo_id = model.create(data)
            
            return self.format_success(
                f"{command.entity.capitalize()} creado exitosamente con ID:  {nuevo_id}",
                {'id': nuevo_id}
            )
        except Exception as e:
            return self.format_error(f"Error al crear:   {str(e)}")
    
    def _handle_modificar(self, command: Command, context: Dict) -> Dict[str, Any]:
        """Handler para acción MODIFICAR (actualizar)"""
        entity_key = self._get_entity_key(command.entity)
        fields = ['id'] + self.ENTITY_FIELDS.get(entity_key, [])
        
        # Validar parámetros
        try:  
            self.validator.validate_required_params(command.params, len(fields), command.entity, 'modificar')
        except ValidationError as e:
            return self.format_error(str(e))
        
        # Obtener ID
        try: 
            id_registro = int(command.params[0])
        except ValueError:
            return self. format_error("El ID debe ser un número entero")
        
        # Crear diccionario de datos (sin el ID)
        data = {fields[i]: command.params[i] for i in range(1, len(fields))}
        
        # Validar campos
        validation_errors = self._validate_fields(data)
        if validation_errors: 
            return self.format_error("Errores de validación:  " + ", ".  join(validation_errors))
        
        # Actualizar
        model = self._get_model(command.entity)
        try:
            if model.update(id_registro, data):
                return self.format_success(f"{command.entity.capitalize()} actualizado exitosamente")
            else:
                return self.format_error(f"No se encontró {command.entity} con ID {id_registro}")
        except Exception as e:
            return self.format_error(f"Error al actualizar: {str(e)}")
    
    def _handle_eliminar(self, command: Command, context: Dict) -> Dict[str, Any]:
        """Handler para acción ELIMINAR"""
        # Validar parámetros
        try:
            self.validator.validate_required_params(command.params, 1, command. entity, 'eliminar')
        except ValidationError as e:  
            return self.format_error(str(e))
        
        # Obtener ID
        try:
            id_registro = int(command.params[0])
        except ValueError:
            return self.format_error("El ID debe ser un número entero")
        
        # Eliminar
        model = self._get_model(command.entity)
        try:
            if model. delete(id_registro):
                return self.format_success(f"{command.entity.capitalize()} eliminado exitosamente")
            else:
                return self.format_error(f"No se encontró {command.entity} con ID {id_registro}")
        except Exception as e:
            return self.format_error(f"Error al eliminar: {str(e)}")
    
    def _handle_reporte(self, command: Command, context: Dict) -> Dict[str, Any]:
        """Handler para acción REPORTE"""
        model = self._get_model(command.entity)
        
        total = model.count()
        report_data = {'total': total}
        
        # Reportes específicos por entidad
        if command.entity == 'usuario':
            for tipo in ['cliente', 'mecanico', 'secretaria', 'propietario']:
                count = Usuario.count({'tipo': tipo})
                report_data[f'total_{tipo}s'] = count
        
        elif command.entity == 'cita':
            for estado in ['pendiente', 'confirmada', 'completada', 'cancelada']: 
                count = Cita.count({'estado': estado})
                report_data[f'estado_{estado}'] = count
        
        elif command.entity == 'pago':
            for estado in ['pendiente', 'pagado_parcial', 'pagado_total']: 
                count = Pago.count({'estado': estado})
                report_data[f'estado_{estado}'] = count
        
        return self.format_success(
            f"Reporte de {command.entity}s generado",
            report_data
        )
    
    def _handle_ayuda(self, command: Command, context: Dict) -> Dict[str, Any]:
        """Handler para comando AYUDA"""
        help_text = {
            'comandos_disponibles': [
                'usuario mostrar',
                'usuario ver [id]',
                'usuario agregar [nombre; email; password; telefono; direccion; tipo]',
                'vehiculo mostrar',
                'servicio mostrar',
                'cita mostrar',
                'cita reporte'
            ]
        }
        return self.format_success("Ayuda del sistema", help_text)
    
    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================
    
    def _get_model(self, entity: str):
        """Obtiene el modelo correspondiente a una entidad"""
        return self.MODELS.get(entity)
    
    def _get_entity_key(self, entity:  str) -> str:
        """Obtiene la clave de entidad normalizada"""
        if entity in ['cliente', 'mecanico', 'secretaria', 'propietario']:
            return 'usuario'
        return entity
    
    def _validate_fields(self, data: Dict[str, Any]) -> List[str]:
        """Valida todos los campos según sus reglas"""
        errors = []
        
        for field, value in data.items():
            # Validar si hay un validador específico
            if field in self.FIELD_VALIDATORS:
                validator = self.FIELD_VALIDATORS[field]
                if not validator(value):
                    errors.append(f"{field}: valor inválido '{value}'")
        
        return errors