# 🔧 Sistema de Gestión - Taller Mecánico

Sistema de gestión de taller mecánico con **procesamiento de comandos por correo electrónico** usando **POP3** y **SMTP**.

## 🌟 Características

- ✅ **Comandos por correo**:  Envía comandos en el asunto del correo
- ✅ **Procesamiento automático**: Daemon revisa constantemente nuevos correos
- ✅ **Respuestas formateadas**: HTML y texto plano
- ✅ **CRUD completo**: Usuarios, Vehículos, Servicios, Citas, Diagnósticos, Órdenes, Pagos
- ✅ **Analizador léxico**: Parser de comandos tipo CLI
- ✅ **Intérprete robusto**: Validación de parámetros y manejo de errores
- ✅ **Seguridad**:  Autenticación por email, passwords encriptados con bcrypt
- ✅ **PostgreSQL**: Base de datos robusta

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- Cuenta de correo con POP3/SMTP (Gmail recomendado)

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/michix14/tecnoweb-python.git
cd tecnoweb-python

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus credenciales

# 5. Crear base de datos
createdb taller_mecanico
psql -d taller_mecanico -f migrations/create_tables.sql

# 6. Ejecutar daemon
python run_daemon.py
```

## 📧 Configuración de Gmail

### 1. Habilitar POP3
- Gmail → Configuración → Reenvío y correo POP/IMAP
- Habilitar POP para todos los mensajes

### 2. Generar App Password
- Ir a:  https://myaccount.google.com/apppasswords
- Generar contraseña para "Correo"
- Usar esa contraseña en `.env`

## 🎮 Uso

### Enviar comandos por correo

**Asunto del correo:**
```
usuario mostrar
```

```
vehiculo agregar [2; SCZ-5678; Honda; Civic; 2021; Rojo; 30000]
```

```
cita reporte
```

### Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `usuario mostrar` | Lista todos los usuarios | - |
| `usuario ver [id]` | Muestra detalle de usuario | `usuario ver [1]` |
| `usuario agregar [...]` | Crea nuevo usuario | `usuario agregar [José Pérez; jose@mail.com; pass123; 70123456; Av. Principal; cliente]` |
| `usuario modificar [id; ...]` | Actualiza usuario | `usuario modificar [1; Juan Pérez; juan@mail. com; pass456; 71234567; Calle 2; cliente]` |
| `usuario eliminar [id]` | Elimina usuario | `usuario eliminar [5]` |
| `usuario reporte` | Genera reporte de usuarios | - |

**Similar para:** `vehiculo`, `servicio`, `cita`, `diagnostico`, `orden`, `pago`

## 📁 Estructura del Proyecto

```
tecnoweb-python/
├── config/              # Configuración
├── models/              # Modelos de datos
├── lexer/               # Analizador léxico
├── interpreter/         # Intérprete de comandos
├── services/            # Servicios (email, auth)
├── daemon/              # Daemon principal
├── cli/                 # Utilidades CLI
├── migrations/          # Scripts SQL
├── tests/               # Tests unitarios
├── logs/                # Logs del sistema
├── data/                # Datos persistentes
└── run_daemon.py        # Script principal
```

## 🔒 Seguridad

- ✅ Passwords hasheados con bcrypt
- ✅ Lista blanca de emails autorizados
- ✅ Validación de parámetros
- ✅ Logs de auditoría

## 🐛 Troubleshooting

### Error de conexión POP3
```bash
telnet pop.gmail.com 995
```

### Revisar logs
```bash
tail -f logs/daemon.log
```

### Verificar BD
```bash
psql -d taller_mecanico -c "SELECT COUNT(*) FROM usuarios;"
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Test de correo
python test_email. py
```

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 👨‍💻 Autor

**michix14** - [GitHub](https://github.com/michix14)

## 🤝 Contribuciones

Las contribuciones son bienvenidas.  Por favor: 

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
