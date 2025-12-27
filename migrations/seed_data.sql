-- ============================================================================
-- DATOS INICIALES DE PRUEBA
-- Sistema de Gestión - Taller Mecánico
-- ============================================================================

-- Limpiar datos existentes (CUIDADO: solo para desarrollo)
TRUNCATE TABLE pago_detalles, pagos, orden_servicios, ordenes_trabajo, 
               diagnosticos, citas, vehiculos, servicios, usuarios 
RESTART IDENTITY CASCADE;

-- ============================================================================
-- USUARIOS
-- ============================================================================

-- Password para todos:  admin123
-- Hash bcrypt:  $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm

-- Propietario
INSERT INTO usuarios (nombre, email, password_hash, telefono, direccion, tipo, estado) VALUES
('Carlos Rodríguez', 'admin@taller.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '70000000', 'Av. Principal #123', 'propietario', 'activo');

-- Secretarias
INSERT INTO usuarios (nombre, email, password_hash, telefono, direccion, tipo, estado) VALUES
('María López', 'maria@taller.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '71111111', 'Zona Norte', 'secretaria', 'activo'),
('Ana García', 'ana@taller.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '72222222', 'Zona Sur', 'secretaria', 'activo');

-- Mecánicos
INSERT INTO usuarios (nombre, email, password_hash, telefono, direccion, tipo, estado) VALUES
('José Martínez', 'jose@taller.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '73333333', 'Taller Principal', 'mecanico', 'activo'),
('Luis Pérez', 'luis@taller.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '74444444', 'Taller Principal', 'mecanico', 'activo'),
('Roberto Flores', 'roberto@taller. com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '75555555', 'Taller Principal', 'mecanico', 'activo');

-- Clientes
INSERT INTO usuarios (nombre, email, password_hash, telefono, direccion, tipo, estado) VALUES
('Juan Pérez', 'juan@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '76666666', 'Calle 1 #456', 'cliente', 'activo'),
('Pedro Sánchez', 'pedro@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '77777777', 'Calle 2 #789', 'cliente', 'activo'),
('Laura Gómez', 'laura@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '78888888', 'Av. Libertad #321', 'cliente', 'activo'),
('Carmen Ruiz', 'carmen@example. com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5QE9QpOEOi4Pm', '79999999', 'Zona Este #654', 'cliente', 'activo');

-- ============================================================================
-- VEHÍCULOS
-- ============================================================================

INSERT INTO vehiculos (cliente_id, placa, marca, modelo, anio, color, kilometraje, estado) VALUES
(7, 'SCZ-1234', 'Toyota', 'Corolla', 2020, 'Blanco', 45000, 'activo'),
(7, 'SCZ-5678', 'Honda', 'Civic', 2021, 'Rojo', 30000, 'activo'),
(8, 'LPZ-9012', 'Nissan', 'Sentra', 2019, 'Negro', 60000, 'activo'),
(9, 'CBB-3456', 'Mazda', 'CX-5', 2022, 'Azul', 15000, 'activo'),
(10, 'TJA-7890', 'Hyundai', 'Tucson', 2021, 'Gris', 25000, 'activo');

-- ============================================================================
-- SERVICIOS
-- ============================================================================

INSERT INTO servicios (nombre, descripcion, tipo, precio_base, duracion_estimada, estado) VALUES
-- Diagnósticos
('Diagnóstico General', 'Revisión completa del vehículo', 'diagnostico', 200.00, 60, 'activo'),
('Diagnóstico Electrónico', 'Escaneo computarizado', 'diagnostico', 150.00, 45, 'activo'),

-- Mantenimiento
('Cambio de Aceite', 'Cambio de aceite y filtro', 'mantenimiento', 120.00, 30, 'activo'),
('Alineación y Balanceo', 'Alineación de ruedas', 'mantenimiento', 100.00, 45, 'activo'),
('Rotación de Neumáticos', 'Rotación y revisión de neumáticos', 'mantenimiento', 80.00, 30, 'activo'),
('Lavado Completo', 'Lavado exterior e interior', 'mantenimiento', 50.00, 60, 'activo'),

-- Reparaciones
('Cambio de Frenos', 'Cambio de pastillas y discos', 'reparacion', 350.00, 120, 'activo'),
('Reparación de Motor', 'Reparación general de motor', 'reparacion', 1500.00, 480, 'activo'),
('Cambio de Transmisión', 'Cambio o reparación de transmisión', 'reparacion', 2000.00, 600, 'activo'),
('Reparación de Suspensión', 'Reparación del sistema de suspensión', 'reparacion', 800.00, 240, 'activo');

-- ============================================================================
-- CITAS
-- ============================================================================

INSERT INTO citas (codigo, cliente_id, vehiculo_id, fecha, hora, motivo, estado) VALUES
('CIT-20250115100000', 7, 1, '2025-01-20', '09:00', 'Cambio de aceite y revisión general', 'confirmada'),
('CIT-20250115100100', 8, 3, '2025-01-21', '10:00', 'Ruido extraño en el motor', 'pendiente'),
('CIT-20250115100200', 9, 4, '2025-01-22', '14:00', 'Alineación y balanceo', 'confirmada'),
('CIT-20250110080000', 10, 5, '2025-01-15', '08:00', 'Mantenimiento preventivo 25,000 km', 'completada');

-- ============================================================================
-- DIAGNÓSTICOS
-- ============================================================================

INSERT INTO diagnosticos (codigo, cita_id, mecanico_id, fecha_diagnostico, descripcion_problema, diagnostico, recomendaciones, estado) VALUES
('DIAG-20250115120000', 4, 4, '2025-01-15', 
 'Cliente reporta mantenimiento preventivo programado',
 'Vehículo en buen estado general.  Aceite oscuro, filtros sucios.  Sistema de frenos al 60%.  Neumáticos desgaste normal.',
 'Cambio de aceite y filtros.  Revisar frenos en próximos 5,000 km.  Rotación de neumáticos.',
 'completado');

-- ============================================================================
-- ÓRDENES DE TRABAJO
-- ============================================================================

INSERT INTO ordenes_trabajo (codigo, diagnostico_id, mecanico_id, fecha_inicio, fecha_fin_estimada, costo_mano_obra, costo_repuestos, estado) VALUES
('ORD-20250115130000', 1, 4, '2025-01-15', '2025-01-15', 120.00, 180.00, 'completada');

-- ============================================================================
-- DETALLE DE SERVICIOS EN ORDEN
-- ============================================================================

INSERT INTO orden_servicios (orden_trabajo_id, servicio_id, cantidad, precio_unitario) VALUES
(1, 3, 1, 120.00),  -- Cambio de aceite
(1, 5, 1, 80.00),   -- Rotación de neumáticos
(1, 6, 1, 50.00);   -- Lavado completo

-- ============================================================================
-- PAGOS
-- ============================================================================

INSERT INTO pagos (codigo, orden_trabajo_id, monto_total, monto_pagado, tipo_pago, numero_cuotas, cuotas_pagadas, estado) VALUES
('PAG-20250115140000', 1, 300.00, 300.00, 'contado', 1, 1, 'pagado_total');

-- ============================================================================
-- DETALLE DE PAGOS
-- ============================================================================

INSERT INTO pago_detalles (pago_id, numero_cuota, monto, metodo_pago, numero_comprobante, fecha_pago, hora_pago, recibido_por) VALUES
(1, 1, 300.00, 'efectivo', NULL, '2025-01-15', '14:30', 2);

-- ============================================================================
-- ESTADÍSTICAS
-- ============================================================================

DO $$
DECLARE
    total_usuarios INT;
    total_vehiculos INT;
    total_servicios INT;
    total_citas INT;
BEGIN
    SELECT COUNT(*) INTO total_usuarios FROM usuarios;
    SELECT COUNT(*) INTO total_vehiculos FROM vehiculos;
    SELECT COUNT(*) INTO total_servicios FROM servicios;
    SELECT COUNT(*) INTO total_citas FROM citas;
    
    RAISE NOTICE '';
    RAISE NOTICE '╔════════════════════════════════════════════════╗';
    RAISE NOTICE '║   ✅ DATOS DE PRUEBA CARGADOS EXITOSAMENTE   ║';
    RAISE NOTICE '╚════════════════════════════════════════════════╝';
    RAISE NOTICE '';
    RAISE NOTICE '📊 Resumen de datos insertados:';
    RAISE NOTICE '   👥 Usuarios:     %', total_usuarios;
    RAISE NOTICE '   🚗 Vehículos:   %', total_vehiculos;
    RAISE NOTICE '   🔧 Servicios:   %', total_servicios;
    RAISE NOTICE '   📅 Citas:       %', total_citas;
    RAISE NOTICE '';
    RAISE NOTICE '🔑 Credenciales de prueba: ';
    RAISE NOTICE '   Email:     admin@taller.com';
    RAISE NOTICE '   Password: admin123';
    RAISE NOTICE '';
END $$;