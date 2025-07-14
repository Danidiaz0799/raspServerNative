# API RESTful RaspServer - Sistema de Cultivo Distribuido

## Información General

- **Base URL:** `http://raspserver.local:5000/api`
- **Formato de respuesta:** JSON
- **Autenticación:** No requerida (En desarrollo para futuras versiones)

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado correctamente |
| 400 | Bad Request - Error en los parámetros de la solicitud |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error en el servidor |

## Índice de Endpoints

1. [Clientes](#1-clientes)
2. [Sensores](#2-sensores)
3. [Parámetros Ideales](#3-parámetros-ideales)
4. [Eventos](#4-eventos)
5. [Actuadores](#5-actuadores)
6. [Estado de la Aplicación](#6-estado-de-la-aplicación)
7. [Estadísticas](#7-estadísticas)
8. [MSAD - Módulo de Almacenamiento y Datos](#8-msad---módulo-de-almacenamiento-y-datos)
   - [Estado](#81-estado)
   - [Backups](#82-backups)
   - [Reportes](#83-reportes)

---

## 1. Clientes

Gestión de nodos de cultivo registrados en el sistema.

### Listar todos los clientes

```
GET http://raspserver.local:5000/api/clients
```

**Respuesta exitosa (200 OK):**
```json
[
  {
    "client_id": "greenhouse-1",
    "name": "Invernadero Principal",
    "description": "Zona de cultivo #1",
    "status": "online",
    "last_seen": "2023-10-15T14:30:22Z"
  },
  {
    "client_id": "greenhouse-2",
    "name": "Invernadero Secundario",
    "description": "Zona de cultivo #2",
    "status": "offline",
    "last_seen": "2023-10-14T18:45:10Z"
  }
]
```

### Obtener un cliente específico

```
GET http://raspserver.local:5000/api/clients/{client_id}
```

**Respuesta exitosa (200 OK):**
```json
{
  "client_id": "greenhouse-1",
  "name": "Invernadero Principal",
  "description": "Zona de cultivo #1",
  "status": "online",
  "last_seen": "2023-10-15T14:30:22Z"
}
```

### Registrar un nuevo cliente

```
POST http://raspserver.local:5000/api/clients
```

**Cuerpo de la solicitud:**
```json
{
  "client_id": "greenhouse-3",
  "name": "Invernadero Experimental",
  "description": "Zona de cultivo experimental"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "message": "Cliente registrado correctamente"
}
```

### Actualizar estado de un cliente

```
PUT http://raspserver.local:5000/api/clients/{client_id}/status
```

**Cuerpo de la solicitud:**
```json
{
  "status": "online"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Estado actualizado correctamente"
}
```

### Actualizar información de un cliente

```
PUT http://raspserver.local:5000/api/clients/{client_id}/info
```

**Cuerpo de la solicitud:**
```json
{
  "name": "Nuevo nombre",
  "description": "Nueva descripción"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Información del cliente actualizada correctamente"
}
```

### Eliminar un cliente

```
DELETE http://raspserver.local:5000/api/clients/{client_id}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Cliente y todos sus datos eliminados correctamente"
}
```

---

## 2. Sensores

Obtención y gestión de lecturas de sensores.

### Obtener lecturas del sensor SHT3x (automático)

```
GET http://raspserver.local:5000/api/clients/{client_id}/Sht3xSensor?page=1&pageSize=10
```

**Parámetros de consulta opcionales:**
- `page`: Número de página (por defecto: 1)
- `pageSize`: Cantidad de registros por página (por defecto: 10)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 123,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T14:30:22Z",
    "temperature": 22.5,
    "humidity": 55.2
  },
  {
    "id": 124,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T14:45:22Z",
    "temperature": 22.7,
    "humidity": 54.8
  }
]
```

### Obtener lecturas del sensor SHT3x (manual)

```
GET http://raspserver.local:5000/api/clients/{client_id}/Sht3xSensorManual?page=1&pageSize=10
```

**Parámetros de consulta opcionales:**
- `page`: Número de página (por defecto: 1)
- `pageSize`: Cantidad de registros por página (por defecto: 10)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 123,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T14:30:22Z",
    "temperature": 22.5,
    "humidity": 55.2
  }
]
```

---

## 3. Parámetros Ideales

Gestión de rangos óptimos para temperatura y humedad.

### Obtener parámetros ideales

```
GET http://raspserver.local:5000/api/clients/{client_id}/IdealParams/{param_type}
```

**Valores para `param_type`:**
- `temperature`: Parámetros de temperatura
- `humidity`: Parámetros de humedad

**Respuesta exitosa (200 OK):**
```json
{
  "client_id": "greenhouse-1",
  "param_type": "temperature",
  "min_value": 20.0,
  "max_value": 25.0
}
```

### Actualizar parámetros ideales

```
PUT http://raspserver.local:5000/api/clients/{client_id}/IdealParams/{param_type}
```

**Valores para `param_type`:**
- `temperature`: Parámetros de temperatura
- `humidity`: Parámetros de humedad

**Cuerpo de la solicitud:**
```json
{
  "min_value": 20.0,
  "max_value": 25.0
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Parametros ideales actualizados exitosamente"
}
```

---

## 4. Eventos

Gestión de eventos y alertas del sistema.

### Listar eventos

```
GET http://raspserver.local:5000/api/clients/{client_id}/Event?page=1&pageSize=10
```

**Parámetros de consulta opcionales:**
- `page`: Número de página (por defecto: 1)
- `pageSize`: Cantidad de registros por página (por defecto: 10)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 45,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T14:30:22Z",
    "type": "ALERT",
    "message": "Humedad baja",
    "topic": "humidity"
  },
  {
    "id": 46,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T15:45:10Z",
    "type": "INFO",
    "message": "Ventilación activada",
    "topic": "fan"
  }
]
```

### Registrar un evento

```
POST http://raspserver.local:5000/api/clients/{client_id}/Event
```

**Cuerpo de la solicitud:**
```json
{
  "message": "Temperatura alta detectada",
  "topic": "temperature"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "message": "Evento guardado correctamente"
}
```

### Filtrar eventos por tema

```
GET http://raspserver.local:5000/api/clients/{client_id}/Event/FilterByTopic?topic=temperature&page=1&pageSize=10
```

**Parámetros de consulta:**
- `topic`: Tema del evento a filtrar (requerido)
- `page`: Número de página (por defecto: 1)
- `pageSize`: Cantidad de registros por página (por defecto: 10)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 47,
    "client_id": "greenhouse-1",
    "timestamp": "2023-10-15T16:30:22Z",
    "type": "ALERT",
    "message": "Temperatura alta detectada",
    "topic": "temperature"
  }
]
```

### Eliminar un evento

```
DELETE http://raspserver.local:5000/api/clients/{client_id}/Event/{id}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Evento eliminado correctamente"
}
```

---

## 5. Actuadores

Gestión de actuadores para el control del ambiente.

### Listar todos los actuadores

```
GET http://raspserver.local:5000/api/clients/{client_id}/Actuator
```

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "client_id": "greenhouse-1",
    "name": "Iluminacion",
    "state": "off",
    "last_updated": "2023-10-15T14:30:22Z"
  },
  {
    "id": 2,
    "client_id": "greenhouse-1",
    "name": "Ventilacion",
    "state": "on",
    "last_updated": "2023-10-15T15:45:10Z"
  },
  {
    "id": 3,
    "client_id": "greenhouse-1",
    "name": "Humidificador",
    "state": "off",
    "last_updated": "2023-10-15T14:30:22Z"
  },
  {
    "id": 4,
    "client_id": "greenhouse-1",
    "name": "Motor",
    "state": "off",
    "last_updated": "2023-10-15T14:30:22Z"
  }
]
```

### Encender/Apagar la luz

```
POST http://raspserver.local:5000/api/clients/{client_id}/Actuator/toggle_light
```

**Cuerpo de la solicitud:**
```json
{
  "state": "on"
}
```

**Valores para `state`:**
- `on`: Encender
- `off`: Apagar

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Senal enviada correctamente"
}
```

### Encender/Apagar el ventilador

```
POST http://raspserver.local:5000/api/clients/{client_id}/Actuator/toggle_fan
```

**Cuerpo de la solicitud:**
```json
{
  "state": "on"
}
```

**Valores para `state`:**
- `on`: Encender
- `off`: Apagar

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Senal enviada correctamente"
}
```

### Encender/Apagar el humidificador

```
POST http://raspserver.local:5000/api/clients/{client_id}/Actuator/toggle_humidifier
```

**Cuerpo de la solicitud:**
```json
{
  "state": "on"
}
```

**Valores para `state`:**
- `on`: Encender
- `off`: Apagar

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Senal enviada correctamente"
}
```

### Encender/Apagar el motor

```
POST http://raspserver.local:5000/api/clients/{client_id}/Actuator/toggle_motor
```

**Cuerpo de la solicitud:**
```json
{
  "state": "on"
}
```

**Valores para `state`:**
- `on`: Encender
- `off`: Apagar

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Senal enviada correctamente"
}
```

### Agregar un nuevo actuador

```
POST http://raspserver.local:5000/api/clients/{client_id}/Actuator
```

**Cuerpo de la solicitud:**
```json
{
  "name": "NuevoActuador",
  "state": "off"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "message": "Actuador agregado correctamente"
}
```

### Actualizar estado de un actuador

```
PUT http://raspserver.local:5000/api/clients/{client_id}/Actuator/{id}
```

**Cuerpo de la solicitud:**
```json
{
  "state": "on"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Estado del actuador actualizado correctamente"
}
```

---

## 6. Estado de la Aplicación

Gestión del modo de operación (manual/automático).

### Obtener estado actual

```
GET http://raspserver.local:5000/api/clients/{client_id}/getState
```

**Respuesta exitosa (200 OK):**
```json
{
  "mode": "automatico"
}
```

### Actualizar estado

```
PUT http://raspserver.local:5000/api/clients/{client_id}/updateState
```

**Cuerpo de la solicitud:**
```json
{
  "mode": "manual"
}
```

**Valores para `mode`:**
- `manual`: Modo manual
- `automatico`: Modo automático

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Estado de la aplicacion actualizado exitosamente"
}
```

---

## 7. MSAD - Módulo de Almacenamiento y Datos

### 7.1 Estado

#### Verificar estado del servicio MSAD

```
GET http://raspserver.local:5000/api/msad/status
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "service": "msad",
  "version": "1.1.0",
  "status": "running"
### 7.2 Backups

#### Listar todos los backups

```
GET http://raspserver.local:5000/api/msad/backups
```

**Parámetros de consulta opcionales:**
- `type`: Filtrar por tipo de backup (`manual`, `auto`, `scheduled`)

**Nota:** El campo `type` en la respuesta será siempre `manual` o `auto`. El parámetro `scheduled` es un alias de `auto` para compatibilidad con el frontend.

**Ejemplos de uso:**
```
GET /api/msad/backups?type=manual      # Solo backups manuales
GET /api/msad/backups?type=auto        # Solo backups automáticos
GET /api/msad/backups?type=scheduled   # Solo backups automáticos (alias)
GET /api/msad/backups                  # Todos los backups
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "backups": [
    {
      "filename": "backup_20231015_143022.zip",
      "size": 1024567,
      "date": "2023-10-15T14:30:22Z",
      "type": "manual"
    },
    {
      "filename": "backup_20231014_000000.zip",
      "size": 952348,
      "date": "2023-10-14T00:00:00Z",
      "type": "auto"
    }
  ]
}
```

#### Crear backup manual

```
POST http://raspserver.local:5000/api/msad/backups/create
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Backup creado correctamente",
  "filename": "backup_20231015_143022.zip",
  "size": 1024567
}
```

#### Descargar un backup

```
GET http://raspserver.local:5000/api/msad/backups/download/{filename}
```

**Respuesta exitosa:** Archivo binario (descarga)

#### Eliminar un backup

```
DELETE http://raspserver.local:5000/api/msad/backups/{filename}
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Backup eliminado correctamente",
  "filename": "backup_20231015_143022.zip"
}
```

#### Restaurar un backup

```
POST http://raspserver.local:5000/api/msad/backups/restore/{filename}
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Backup restaurado correctamente",
  "filename": "backup_20231015_143022.zip"
}
```

#### Obtener estado del programador de backups

```
GET http://raspserver.local:5000/api/msad/backups/scheduler
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "is_running": true,
  "interval_hours": 3,
  "backup_count": 2,
  "total_size": 204800,
  "formatted_size": "200.00 KB",
  "last_backup": "2025-04-26T05:01:05",
  "next_backup": "2025-04-26T08:01:05",
  "backup_dir": "/ruta/a/backups"
}
```

#### Configurar programador de backups

```
POST http://raspserver.local:5000/api/msad/backups/scheduler
```

**Cuerpo de la solicitud:**
```json
{
  "enabled": true,
  "interval_hours": 3
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Backup scheduler started with interval of 3 hours",
  "status": {
    "success": true,
    "is_running": true,
    "interval_hours": 3,
    "backup_count": 2,
    "total_size": 204800,
    "formatted_size": "200.00 KB",
    "last_backup": "2025-04-26T05:01:05",
    "next_backup": "2025-04-26T08:01:05",
    "backup_dir": "/ruta/a/backups"
  }
}
```

### 7.3 Reportes

#### Generar un reporte

```
POST http://raspserver.local:5000/api/clients/{client_id}/msad/reports
```

**Cuerpo de la solicitud:**
```json
{
  "start_date": "2023-10-01",
  "end_date": "2023-10-15",
  "data_type": "sensors",
  "format": "csv"
}
```

**Valores para `data_type`:**
- `sensors`: Datos de sensores
- `events`: Datos de eventos
- `all`: Todos los datos

**Valores para `format`:**
- `csv`: Formato CSV
- `json`: Formato JSON

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Reporte generado correctamente",
  "file_id": "report_greenhouse1_sensors_20231015_1430.csv",
  "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_greenhouse1_sensors_20231015_1430.csv"
}
```

#### Listar reportes de un cliente

```
GET http://raspserver.local:5000/api/clients/{client_id}/msad/reports
```

**Parámetros de consulta opcionales:**
- `format`: Filtrar por formato (`csv` o `json`)
- `data_type`: Filtrar por tipo de datos (`sensors`, `events`, `all`)

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "reports": [
    {
      "file_id": "report_greenhouse1_sensors_20231015_1430.csv",
      "size": 25678,
      "date": "2023-10-15T14:30:22Z",
      "client_id": "greenhouse-1",
      "data_type": "sensors",
      "format": "csv",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_greenhouse1_sensors_20231015_1430.csv"
    }
  ]
}
```

#### Listar todos los reportes

```
GET http://raspserver.local:5000/api/msad/reports
```

**Parámetros de consulta opcionales:**
- `format`: Filtrar por formato (`csv` o `json`)
- `data_type`: Filtrar por tipo de datos (`sensors`, `events`, `all`)

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "reports": [
    {
      "file_id": "report_greenhouse1_sensors_20231015_1430.csv",
      "size": 25678,
      "date": "2023-10-15T14:30:22Z",
      "client_id": "greenhouse-1",
      "data_type": "sensors",
      "format": "csv",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_greenhouse1_sensors_20231015_1430.csv"
    },
    {
      "file_id": "report_greenhouse2_events_20231014_1030.json",
      "size": 15342,
      "date": "2023-10-14T10:30:15Z",
      "client_id": "greenhouse-2",
      "data_type": "events",
      "format": "json",
      "download_url": "/api/clients/greenhouse-2/msad/reports/download/report_greenhouse2_events_20231014_1030.json"
    }
  ]
}
```

#### Descargar un reporte

```
GET http://raspserver.local:5000/api/clients/{client_id}/msad/reports/download/{filename}
```

**Respuesta exitosa:** Archivo CSV o JSON (descarga)

#### Eliminar un reporte

```
DELETE http://raspserver.local:5000/api/clients/{client_id}/msad/reports/{report_id}
```

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Reporte eliminado correctamente",
  "report_id": "report_greenhouse1_sensors_20231015_1430.csv",
  "client_id": "greenhouse-1"
}
```