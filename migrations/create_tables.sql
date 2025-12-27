-- ============================================================================
-- SISTEMA DE GESTIÓN - TALLER MECÁNICO
-- Script de creación de base de datos
-- ============================================================================

-- ============================================================================
-- TABLA:  USUARIOS (Propietario, Secretaria, Mecánico, Cliente)
-- ============================================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    tipo VARCHAR(20) CHECK (tipo IN ('propietario', 'secretaria', 'mecanico', 'cliente')) NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('activo', 'inactivo')) DEFAULT 'activo',
    foto TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para usuarios
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo);
CREATE INDEX idx_usuarios_estado ON usuarios(estado);

COMMENT ON TABLE usuarios IS 'Tabla de usuarios del sistema (propietarios, secretarias, mecánicos, clientes)';
COMMENT ON COLUMN usuarios.tipo IS 'Tipo de usuario:  propietario, secretaria, mecanico, cliente';
COMMENT ON COLUMN usuarios.password_hash IS 'Hash bcrypt de la contraseña';

-- ============================================================================
-- TABLA: VEHÍCULOS
-- ============================================================================
CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio INT CHECK (anio >= 1900 AND anio <= 2100),
    color VARCHAR(30),
    kilometraje INT DEFAULT 0 CHECK (kilometraje >= 0),
    foto TEXT,
    observaciones TEXT,
    estado VARCHAR(20) CHECK (estado IN ('activo', 'inactivo')) DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Índices para vehículos
CREATE INDEX idx_vehiculos_cliente ON vehiculos(cliente_id);
CREATE INDEX idx_vehiculos_placa ON vehiculos(placa);
CREATE INDEX idx_vehiculos_estado ON vehiculos(estado);

COMMENT ON TABLE vehiculos IS 'Tabla de vehículos registrados en el taller';
COMMENT ON COLUMN vehiculos.placa IS 'Placa única del vehículo (formato: XXX-9999)';

-- ============================================================================
-- TABLA: SERVICIOS
-- ============================================================================
CREATE TABLE servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(20) CHECK (tipo IN ('diagnostico', 'mantenimiento', 'reparacion')) NOT NULL,
    precio_base NUMERIC(10, 2) NOT NULL CHECK (precio_base >= 0),
    duracion_estimada INT CHECK (duracion_estimada > 0), -- minutos
    estado VARCHAR(20) CHECK (estado IN ('activo', 'inactivo')) DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para servicios
CREATE INDEX idx_servicios_tipo ON servicios(tipo);
CREATE INDEX idx_servicios_estado ON servicios(estado);

COMMENT ON TABLE servicios IS 'Catálogo de servicios ofrecidos por el taller';
COMMENT ON COLUMN servicios. tipo IS 'Tipo de servicio: diagnostico, mantenimiento, reparacion';
COMMENT ON COLUMN servicios.duracion_estimada IS 'Duración estimada en minutos';

-- ============================================================================
-- TABLA: CITAS
-- ============================================================================
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    cliente_id INT NOT NULL,
    vehiculo_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo TEXT,
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'confirmada', 'en_proceso', 'completada', 'cancelada')) DEFAULT 'pendiente',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id) ON DELETE CASCADE
);

-- Índices para citas
CREATE INDEX idx_citas_codigo ON citas(codigo);
CREATE INDEX idx_citas_cliente ON citas(cliente_id);
CREATE INDEX idx_citas_vehiculo ON citas(vehiculo_id);
CREATE INDEX idx_citas_fecha ON citas(fecha);
CREATE INDEX idx_citas_estado ON citas(estado);

COMMENT ON TABLE citas IS 'Citas agendadas para servicios';
COMMENT ON COLUMN citas.codigo IS 'Código único generado automáticamente (CIT-YYYYMMDDHHMMSS)';

-- ============================================================================
-- TABLA: DIAGNÓSTICOS
-- ============================================================================
CREATE TABLE diagnosticos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    cita_id INT NOT NULL,
    mecanico_id INT NOT NULL,
    fecha_diagnostico DATE NOT NULL,
    descripcion_problema TEXT NOT NULL,
    diagnostico TEXT NOT NULL,
    recomendaciones TEXT,
    estado VARCHAR(20) CHECK (estado IN ('en_revision', 'completado', 'aprobado_cliente', 'rechazado_cliente')) DEFAULT 'en_revision',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE CASCADE,
    FOREIGN KEY (mecanico_id) REFERENCES usuarios(id) ON DELETE RESTRICT
);

-- Índices para diagnósticos
CREATE INDEX idx_diagnosticos_codigo ON diagnosticos(codigo);
CREATE INDEX idx_diagnosticos_cita ON diagnosticos(cita_id);
CREATE INDEX idx_diagnosticos_mecanico ON diagnosticos(mecanico_id);
CREATE INDEX idx_diagnosticos_estado ON diagnosticos(estado);

COMMENT ON TABLE diagnosticos IS 'Diagnósticos técnicos realizados';
COMMENT ON COLUMN diagnosticos.codigo IS 'Código único generado automáticamente (DIAG-YYYYMMDDHHMMSS)';

-- ============================================================================
-- TABLA: ÓRDENES DE TRABAJO
-- ============================================================================
CREATE TABLE ordenes_trabajo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    diagnostico_id INT NOT NULL,
    mecanico_id INT NOT NULL,
    fecha_creacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_inicio DATE,
    fecha_fin_estimada DATE,
    fecha_fin_real DATE,
    costo_mano_obra NUMERIC(10, 2) DEFAULT 0 CHECK (costo_mano_obra >= 0),
    costo_repuestos NUMERIC(10, 2) DEFAULT 0 CHECK (costo_repuestos >= 0),
    subtotal NUMERIC(10, 2) GENERATED ALWAYS AS (costo_mano_obra + costo_repuestos) STORED,
    estado VARCHAR(20) CHECK (estado IN ('presupuestada', 'aprobada', 'en_proceso', 'completada', 'entregada', 'cancelada')) DEFAULT 'presupuestada',
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos(id) ON DELETE CASCADE,
    FOREIGN KEY (mecanico_id) REFERENCES usuarios(id) ON DELETE RESTRICT
);

-- Índices para órdenes de trabajo
CREATE INDEX idx_ordenes_codigo ON ordenes_trabajo(codigo);
CREATE INDEX idx_ordenes_diagnostico ON ordenes_trabajo(diagnostico_id);
CREATE INDEX idx_ordenes_mecanico ON ordenes_trabajo(mecanico_id);
CREATE INDEX idx_ordenes_estado ON ordenes_trabajo(estado);

COMMENT ON TABLE ordenes_trabajo IS 'Órdenes de trabajo del taller';
COMMENT ON COLUMN ordenes_trabajo.codigo IS 'Código único generado automáticamente (ORD-YYYYMMDDHHMMSS)';
COMMENT ON COLUMN ordenes_trabajo.subtotal IS 'Calculado automáticamente (mano de obra + repuestos)';

-- ============================================================================
-- TABLA: DETALLE DE SERVICIOS EN ORDEN DE TRABAJO
-- ============================================================================
CREATE TABLE orden_servicios (
    id SERIAL PRIMARY KEY,
    orden_trabajo_id INT NOT NULL,
    servicio_id INT NOT NULL,
    descripcion TEXT,
    cantidad INT DEFAULT 1 CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal NUMERIC(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    
    FOREIGN KEY (orden_trabajo_id) REFERENCES ordenes_trabajo(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE RESTRICT
);

-- Índices para orden_servicios
CREATE INDEX idx_orden_servicios_orden ON orden_servicios(orden_trabajo_id);
CREATE INDEX idx_orden_servicios_servicio ON orden_servicios(servicio_id);

COMMENT ON TABLE orden_servicios IS 'Detalle de servicios incluidos en cada orden de trabajo';

-- ============================================================================
-- TABLA: PAGOS
-- ============================================================================
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    orden_trabajo_id INT NOT NULL,
    monto_total NUMERIC(10, 2) NOT NULL CHECK (monto_total > 0),
    monto_pagado NUMERIC(10, 2) DEFAULT 0 CHECK (monto_pagado >= 0),
    monto_pendiente NUMERIC(10, 2) GENERATED ALWAYS AS (monto_total - monto_pagado) STORED,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('contado', 'credito')) NOT NULL,
    numero_cuotas INT DEFAULT 1 CHECK (numero_cuotas > 0),
    cuotas_pagadas INT DEFAULT 0 CHECK (cuotas_pagadas >= 0),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'pagado_parcial', 'pagado_total', 'vencido')) DEFAULT 'pendiente',
    fecha_vencimiento DATE,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (orden_trabajo_id) REFERENCES ordenes_trabajo(id) ON DELETE RESTRICT,
    
    CONSTRAINT cuotas_validas CHECK (cuotas_pagadas <= numero_cuotas),
    CONSTRAINT credito_tiene_cuotas CHECK (
        (tipo_pago = 'contado' AND numero_cuotas = 1) OR
        (tipo_pago = 'credito' AND numero_cuotas > 1)
    )
);

-- Índices para pagos
CREATE INDEX idx_pagos_codigo ON pagos(codigo);
CREATE INDEX idx_pagos_orden ON pagos(orden_trabajo_id);
CREATE INDEX idx_pagos_estado ON pagos(estado);
CREATE INDEX idx_pagos_vencimiento ON pagos(fecha_vencimiento);

COMMENT ON TABLE pagos IS 'Registro de pagos (contado o a crédito)';
COMMENT ON COLUMN pagos.codigo IS 'Código único generado automáticamente (PAG-YYYYMMDDHHMMSS)';
COMMENT ON COLUMN pagos.tipo_pago IS 'Tipo de pago: contado (1 cuota) o credito (múltiples cuotas)';

-- ============================================================================
-- TABLA: DETALLE DE PAGOS (Efectivo o QR)
-- ============================================================================
CREATE TABLE pago_detalles (
    id SERIAL PRIMARY KEY,
    pago_id INT NOT NULL,
    numero_cuota INT NOT NULL CHECK (numero_cuota > 0),
    monto NUMERIC(10, 2) NOT NULL CHECK (monto > 0),
    metodo_pago VARCHAR(20) CHECK (metodo_pago IN ('efectivo', 'qr')) NOT NULL,
    numero_comprobante VARCHAR(50),
    banco VARCHAR(50),
    referencia TEXT,
    fecha_pago DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_pago TIME NOT NULL DEFAULT CURRENT_TIME,
    recibido_por INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (pago_id) REFERENCES pagos(id) ON DELETE CASCADE,
    FOREIGN KEY (recibido_por) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Índices para pago_detalles
CREATE INDEX idx_pago_detalles_pago ON pago_detalles(pago_id);
CREATE INDEX idx_pago_detalles_fecha ON pago_detalles(fecha_pago);
CREATE INDEX idx_pago_detalles_metodo ON pago_detalles(metodo_pago);

COMMENT ON TABLE pago_detalles IS 'Detalle de cada pago realizado (cuotas)';
COMMENT ON COLUMN pago_detalles.metodo_pago IS 'Método de pago: efectivo o qr';

-- ============================================================================
-- TRIGGERS PARA UPDATED_AT
-- ============================================================================

-- Función genérica para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas con updated_at
CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vehiculos_updated_at BEFORE UPDATE ON vehiculos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_servicios_updated_at BEFORE UPDATE ON servicios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_citas_updated_at BEFORE UPDATE ON citas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnosticos_updated_at BEFORE UPDATE ON diagnosticos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ordenes_updated_at BEFORE UPDATE ON ordenes_trabajo
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pagos_updated_at BEFORE UPDATE ON pagos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista de citas con información completa
CREATE OR REPLACE VIEW v_citas_completas AS
SELECT 
    c.id,
    c.codigo,
    c.fecha,
    c.hora,
    c.estado,
    c.motivo,
    u.nombre AS cliente_nombre,
    u.email AS cliente_email,
    u.telefono AS cliente_telefono,
    v.placa,
    v.marca,
    v.modelo,
    v.anio,
    c.created_at
FROM citas c
INNER JOIN usuarios u ON c.cliente_id = u.id
INNER JOIN vehiculos v ON c. vehiculo_id = v.id;

-- Vista de órdenes con totales
CREATE OR REPLACE VIEW v_ordenes_completas AS
SELECT 
    o.id,
    o.codigo,
    o.estado,
    o.fecha_creacion,
    o.fecha_inicio,
    o.fecha_fin_real,
    o.costo_mano_obra,
    o.costo_repuestos,
    o.subtotal,
    m.nombre AS mecanico_nombre,
    d.codigo AS diagnostico_codigo,
    c.codigo AS cita_codigo,
    u.nombre AS cliente_nombre,
    v.placa
FROM ordenes_trabajo o
INNER JOIN usuarios m ON o.mecanico_id = m.id
INNER JOIN diagnosticos d ON o.diagnostico_id = d.id
INNER JOIN citas c ON d.cita_id = c. id
INNER JOIN usuarios u ON c.cliente_id = u.id
INNER JOIN vehiculos v ON c.vehiculo_id = v.id;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE '✅ Base de datos creada exitosamente';
    RAISE NOTICE '📊 Tablas creadas:  8';
    RAISE NOTICE '🔍 Índices creados: múltiples';
    RAISE NOTICE '⚙️  Triggers creados: 7';
    RAISE NOTICE '👁️  Vistas creadas:  2';
END $$;