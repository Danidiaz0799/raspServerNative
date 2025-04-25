# MSAD - Módulo de Almacenamiento y Análisis de Datos

<div align="center">

![Versión](https://img.shields.io/badge/Versión-1.1.0-blue)
![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)
![Integración](https://img.shields.io/badge/Integración-RaspServer-green)

</div>

## 📋 Índice

- [Resumen](#-resumen)
- [Arquitectura](#-arquitectura)
- [Funcionalidades](#-funcionalidades)
  - [Sistema de Backups](#-sistema-de-backups)
  - [Sistema de Reportes](#-sistema-de-reportes)
- [Endpoints API](#-endpoints-api)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Resolución de Problemas](#-resolución-de-problemas)

## 📝 Resumen

MSAD es un módulo integrado en RaspServer que proporciona capacidades de almacenamiento, respaldo y generación de reportes para los datos del sistema de cultivo. Sus principales características son:

- **Backups automáticos y manuales** de la base de datos principal
- **Generación de reportes** en formatos JSON y CSV
- **API RESTful** para interactuar con todas las funcionalidades
- **Alta eficiencia** en el manejo de datos con mínimo impacto en recursos

## 🏗 Arquitectura

El módulo MSAD está diseñado como un componente integrado en la aplicación Flask principal, expuesto a través de blueprints API específicos.

```
┌─────────────────────────┐
│    Aplicación Flask     │◄───┐ Registra blueprints
│      (app.py)           │    │ e inicializa MSAD
└───────────┬─────────────┘    │
            │                  │
            ▼                  │
┌─────────────────────────────────────────────┐
│                 MSAD                        │
│                                             │
│  ┌─────────────┐       ┌─────────────────┐  │
│  │  API Layer  │◄────► │    Core Layer   │  │
│  │ (endpoints) │       │  (lógica de     │  │
│  └─────────────┘       │   negocio)      │  │
│                        └────────┬────────┘  │
│                                 │           │
└─────────────────────────────────┼───────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   Base de Datos    │
                       │  (sensor_data.db)  │
                       └────────────────────┘
```

### Componentes Principales

1. **API Layer**: Implementa endpoints RESTful para acceder a las funcionalidades
   - Ubicación: `msad/api/`
   - Archivos: `backup_routes.py`, `report_routes.py`, `system_routes.py`

2. **Core Layer**: Contiene la lógica de negocio e interacción con la base de datos
   - Ubicación: `msad/core/`
   - Archivos: `backup.py`, `reports.py`, `system.py`

3. **Almacenamiento**: Gestiona archivos de backups y reportes generados
   - Estructura: `<STORAGE_PATH>/msad/{backups,reports}`

## 🔧 Funcionalidades

### 💾 Sistema de Backups

#### Características

- **Backups automáticos**: Programados a intervalos configurables
- **Backups manuales**: Bajo demanda a través de la API
- **Rotación**: Conserva un número máximo de backups, eliminando los más antiguos
- **Verificación de integridad**: Comprueba que la base de datos no esté corrupta
- **Restauración segura**: Crea un backup de seguridad antes de restaurar

#### Flujo de Creación de Backup

1. Verifica existencia y estado de la base de datos
2. Genera nombre único con timestamp y tipo (manual/auto)
3. Verifica integridad de la base de datos
4. Crea copia de seguridad en `<STORAGE_PATH>/msad/backups/`
5. Rota backups antiguos si es necesario

#### Flujo de Restauración

1. Crea backup de seguridad de la base de datos actual
2. Copia el archivo de backup seleccionado como la base de datos principal
3. Verifica integridad después de la restauración

### 📊 Sistema de Reportes

#### Características

- **Generación flexible**: Filtrado por cliente, fechas y tipo de datos
- **Múltiples formatos**: JSON y CSV
- **Estructura organizada**: Reportes guardados por cliente
- **Metadatos completos**: Información detallada sobre cada reporte

#### Tipos de Reportes

| Tipo        | Descripción                            | Tabla BD           |
|-------------|----------------------------------------|--------------------|
| `sensors`   | Datos de sensores (temp/humedad)       | `sht3x_data`       |
| `events`    | Eventos del sistema                    | `events`           |
| `actuators` | Acciones de los actuadores             | `actuator_actions` |

#### Flujo de Generación de Reportes

1. Valida parámetros de entrada (cliente, fechas, tipo, formato)
2. Consulta datos en la base de datos según criterios
3. Formatea los datos al formato solicitado (JSON/CSV)
4. Guarda el archivo en `<STORAGE_PATH>/msad/reports/<client_id>/`
5. Retorna metadatos del reporte generado

## 🌐 Endpoints API

### Estado del Sistema

```
GET /api/msad/status
```

**Respuesta:**
```json
{
  "success": true,
  "service": "msad",
  "version": "1.1.0",
  "status": "running"
}
```

### Gestión de Backups

#### Listar backups

```
GET /api/msad/backups
```

**Parámetros opcionales:**
- `type`: Filtrar por tipo (`manual` o `auto`)

**Respuesta:**
```json
{
  "success": true,
  "backups": [
    {
      "backup_id": "backup_20231015_143022",
      "filename": "sensor_data_manual_20231015_143022.db",
      "type": "manual",
      "size": 1024567,
      "created_at": "2023-10-15T14:30:22",
      "download_url": "/api/msad/backups/download/sensor_data_manual_20231015_143022.db"
    }
  ]
}
```

#### Crear backup manual

```
POST /api/msad/backups/create
```

**Respuesta:**
```json
{
  "success": true,
  "filename": "sensor_data_manual_20231015_143022.db",
  "size": 1024567,
  "download_url": "/api/msad/backups/download/sensor_data_manual_20231015_143022.db"
}
```

#### Descargar backup

```
GET /api/msad/backups/download/{filename}
```

**Respuesta:** Archivo binario

#### Eliminar backup

```
DELETE /api/msad/backups/{filename}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Backup eliminado correctamente"
}
```

#### Restaurar backup

```
POST /api/msad/backups/restore/{filename}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Backup restaurado correctamente",
  "safety_backup": "sensor_data_auto_20231015_150022.db"
}
```

#### Consultar estado del scheduler

```
GET /api/msad/backups/scheduler
```

**Respuesta:**
```json
{
  "success": true,
  "enabled": true,
  "interval_hours": 24,
  "next_backup": "2023-10-16T00:00:00",
  "last_backup": "2023-10-15T00:00:00"
}
```

#### Configurar scheduler

```
POST /api/msad/backups/scheduler
```

**Cuerpo:**
```json
{
  "enabled": true,
  "interval_hours": 12
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Scheduler configurado correctamente",
  "status": {
    "enabled": true,
    "interval_hours": 12,
    "next_backup": "2023-10-15T12:00:00"
  }
}
```

### Gestión de Reportes

#### Generar reporte

```
POST /api/clients/{client_id}/msad/reports
```

**Cuerpo:**
```json
{
  "start_date": "2023-10-01",
  "end_date": "2023-10-15",
  "data_type": "sensors",
  "format": "csv"
}
```

**Parámetros:**
- `start_date`: Fecha inicial (YYYY-MM-DD)
- `end_date`: Fecha final (YYYY-MM-DD)
- `data_type`: Tipo de datos (`sensors`, `events`, `actuators`)
- `format`: Formato de salida (`json`, `csv`)

**Respuesta:**
```json
{
  "success": true,
  "filename": "greenhouse1_sensors_20231001_to_20231015_20231015_143022.csv",
  "records": 350,
  "size": 25678,
  "download_url": "/api/clients/greenhouse-1/msad/reports/download/greenhouse1_sensors_20231001_to_20231015_20231015_143022.csv"
}
```

#### Listar reportes de un cliente

```
GET /api/clients/{client_id}/msad/reports
```

**Parámetros opcionales:**
- `format`: Filtrar por formato (`json`, `csv`)
- `data_type`: Filtrar por tipo de datos (`sensors`, `events`, `actuators`)

**Respuesta:**
```json
{
  "success": true,
  "reports": [
    {
      "filename": "greenhouse1_sensors_20231001_to_20231015_20231015_143022.csv",
      "client_id": "greenhouse-1",
      "data_type": "sensors",
      "format": "csv",
      "created_at": "2023-10-15T14:30:22",
      "size": 25678,
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/greenhouse1_sensors_20231001_to_20231015_20231015_143022.csv"
    }
  ]
}
```

#### Listar todos los reportes

```
GET /api/msad/reports
```

**Parámetros opcionales:** Igual que el endpoint anterior

#### Descargar reporte

```
GET /api/clients/{client_id}/msad/reports/download/{filename}
```

**Respuesta:** Archivo CSV o JSON

#### Eliminar reporte

```
DELETE /api/clients/{client_id}/msad/reports/{filename}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Reporte eliminado correctamente"
}
```

## ⚙️ Instalación y Configuración

### Requisitos Previos

- Python 3.7 o superior
- Dependencia `schedule` para los backups automáticos
- Permisos de escritura en el directorio de almacenamiento

### Configuración del Directorio de Almacenamiento

El módulo MSAD usa por defecto estas rutas:

- **Linux**: `/mnt/storage/msad/`
- **Windows (Desarrollo)**: `storage/msad/` (relativo al proyecto)

Estructura de directorios:

```
<STORAGE_PATH>/msad/
├── backups/           # Archivos de respaldo de la BD
├── reports/           # Reportes generados por cliente
│   ├── client_1/
│   └── client_2/
└── logs/              # Archivos de registro
```

### Integración con RaspServer

El módulo MSAD se inicializa y registra en `app.py`:

```python
from msad import (
    init_msad, shutdown_msad,
    create_system_blueprint, create_backup_blueprint, create_report_blueprint
)
import atexit

# Crear y registrar blueprints
system_bp = create_system_blueprint()
backup_bp = create_backup_blueprint()
report_bp = create_report_blueprint()

app.register_blueprint(system_bp, url_prefix='/api')
app.register_blueprint(backup_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')

# Inicializar con backups automáticos cada 24 horas
init_msad(auto_backup=True, backup_interval_hours=24)

# Registrar función de apagado limpio
atexit.register(shutdown_msad)
```

### Parámetros de Configuración

| Parámetro                | Descripción                                     | Valor por defecto |
|--------------------------|--------------------------------------------------|-------------------|
| `auto_backup`            | Habilitar backups automáticos                   | `False`           |
| `backup_interval_hours`  | Intervalo en horas entre backups automáticos    | `24`              |
| `MAX_BACKUPS`            | Número máximo de backups a conservar            | `10`              |
| `STORAGE_PATH`           | Ruta base para almacenamiento                   | Ver arriba        |

## 🛠 Resolución de Problemas

### Problemas Comunes

| Problema                              | Posible Causa                                     | Solución                                                       |
|---------------------------------------|---------------------------------------------------|----------------------------------------------------------------|
| Error "Permission denied"             | Permisos insuficientes en directorio              | `sudo chmod -R 755 <STORAGE_PATH>`                             |
| No se crean backups automáticos       | Schedule no funciona o app reiniciada             | Verificar logs, reiniciar servidor                             |
| Error al restaurar backup             | BD en uso o corrupta                              | Detener servidor antes de restaurar                            |
| "No hay datos" al generar reporte     | Rango de fechas incorrecto o cliente sin datos    | Verificar que existan datos para el cliente y rango            |
| Archivo de reporte no se descarga     | Nombre incorrecto o falta MIME type               | Verificar ruta exacta y formato en la URL                      |

### Consulta de Logs

Los logs de MSAD se almacenan en:

```
<STORAGE_PATH>/msad/logs/msad.log
```

Ejemplo para consultar los últimos 100 registros:

```bash
tail -n 100 /mnt/storage/msad/logs/msad.log
```

### Verificación del Sistema

Para comprobar el estado de MSAD:

```bash
curl http://raspserver.local:5000/api/msad/status
``` 