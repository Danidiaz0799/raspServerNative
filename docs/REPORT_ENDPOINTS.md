# Endpoints de Reportes – MSAD

---

## Resumen

Esta API permite la generación, consulta, descarga, eliminación y programación automática de reportes de datos para clientes, alineada con la estructura real de la base de datos y el sistema de archivos. Todos los endpoints implementan validaciones estrictas y manejo robusto de errores. Las respuestas son informativas y claras ante cualquier situación.

---

## 1. Crear un reporte de datos

**POST** `/api/clients/<client_id>/msad/reports`

Crea un reporte de datos para un cliente, en formato JSON o CSV, para un rango de fechas y tipo de datos.

### Parámetros requeridos y validaciones
- `client_id` (en la URL): string, obligatorio. Debe existir en la base de datos.
- `start_date`: string, obligatorio. Formato `YYYY-MM-DD`.
- `end_date`: string, obligatorio. Formato `YYYY-MM-DD`.
- `data_type`: string, opcional. Uno de: `sensors`, `events`, `actuators` (por defecto: `sensors`).
- `format`: string, opcional. Uno de: `json`, `csv` (por defecto: `json`).

### Validaciones y errores comunes
- Si falta algún parámetro requerido, la respuesta será:
```json
{
  "success": false,
  "error": "<mensaje explicativo>"
}
```
- Si el formato de fecha es incorrecto:
```json
{
  "success": false,
  "error": "Formato de fecha incorrecto. Use YYYY-MM-DD"
}
```
- Si no hay datos para el cliente o el rango:
```json
{
  "success": false,
  "error": "No se encontraron datos para el rango especificado"
}
```
- Si ocurre un error de sistema (por ejemplo, al escribir el archivo):
```json
{
  "success": false,
  "error": "No se pudo guardar el archivo de reporte"
}
```

### Ejemplo de Request:
```http
POST /api/clients/greenhouse-1/msad/reports
Content-Type: application/json
{
  "start_date": "2025-04-01",
  "end_date": "2025-04-10",
  "data_type": "sensors",
  "format": "json"
}
```

### Ejemplo de Response exitosa:
```json
{
  "success": true,
  "report_id": "report_20250401_20250410_sensors_20250426_120000",
  "client_id": "greenhouse-1",
  "data_type": "sensors",
  "filename": "greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json",
  "format": "json",
  "period": {
    "start": "2025-04-01",
    "end": "2025-04-10"
  },
  "records": 128,
  "size": 12345,
  "created_at": "2025-04-26T12:00:00",
  "download_url": "/api/clients/greenhouse-1/msad/reports/download/greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json"
}
```

### Notas importantes
- El nombre del archivo generado incluye el rango de fechas, tipo de datos y un timestamp único.
- Todos los errores son registrados en logs para facilitar la trazabilidad.
- Si el directorio de reportes no existe, se crea automáticamente.
- El endpoint es robusto ante fallos de base de datos o sistema de archivos.

---

## 2. Listar reportes de un cliente

**GET** `/api/clients/<client_id>/msad/reports`

Lista todos los reportes generados para un cliente específico. Permite filtrar por formato y tipo de datos.

### Parámetros opcionales
- `format`: `json` o `csv`. Solo muestra reportes de ese formato.
- `data_type`: `sensors`, `events` o `actuators`. Solo muestra reportes de ese tipo.

### Validaciones y manejo de errores
- Si el cliente no tiene reportes, la lista será vacía:
```json
{
  "success": true,
  "reports": [],
  "total": 0
}
```
- Si ocurre un error de sistema, por ejemplo, al acceder al directorio:
```json
{
  "success": false,
  "error": "No se pudo acceder al directorio de reportes"
}
```

### Ejemplo de Request:
```http
GET /api/clients/greenhouse-1/msad/reports?format=json&data_type=sensors
```

### Ejemplo de Response exitosa:
```json
{
  "success": true,
  "reports": [
    {
      "report_id": "report_20250401_20250410_sensors_20250426_120000",
      "client_id": "greenhouse-1",
      "data_type": "sensors",
      "filename": "greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json",
      "format": "json",
      "size": 12345,
      "created_at": "2025-04-26T12:00:00",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json"
    }
  ],
  "total": 1
}
```

### Notas
- Los reportes siempre se devuelven ordenados por fecha de creación, más recientes primero.
- Si el directorio del cliente no existe, la respuesta será una lista vacía.

---

## 3. Listar todos los reportes del sistema

**GET** `/api/msad/reports`

Lista todos los reportes generados en el sistema, de todos los clientes. Permite filtrar por formato y tipo de datos.

### Parámetros opcionales
- `format`: `json` o `csv`.
- `data_type`: `sensors`, `events` o `actuators`.

### Validaciones y manejo de errores
- Si no existen reportes, la lista será vacía.
- Si ocurre un error al acceder a los directorios de reportes, se devuelve un mensaje de error.

### Ejemplo de Request:
```http
GET /api/msad/reports?format=json&data_type=sensors
```

### Ejemplo de Response exitosa:
```json
{
  "success": true,
  "reports": [
    {
      "report_id": "report_20250401_20250410_sensors_20250426_120000",
      "client_id": "greenhouse-1",
      "data_type": "sensors",
      "filename": "greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json",
      "format": "json",
      "size": 12345,
      "created_at": "2025-04-26T12:00:00",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json"
    }
  ],
  "total": 1
}
```

---

## 4. Descargar un reporte específico

**GET** `/api/clients/<client_id>/msad/reports/download/<filename>`

Descarga el archivo de reporte especificado por `<filename>` para el cliente.

### Validaciones y manejo de errores
- Si el archivo no existe o el nombre es incorrecto, se devuelve:
```json
{
  "success": false,
  "error": "File not found"
}
```
- Si ocurre un error del sistema:
```json
{
  "success": false,
  "error": "<mensaje de error>"
}
```

**Request:**
```http
GET /api/clients/greenhouse-1/msad/reports/download/greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json
```

**Response:**
- Descarga directa del archivo solicitado (binario, JSON o CSV).

### Notas
- El endpoint determina automáticamente el tipo MIME según la extensión del archivo.
- Se puede usar tanto el nombre completo del archivo como el `report_id` para descargarlo (ver lógica interna).

---

## 5. Eliminar un reporte específico

**DELETE** `/api/clients/<client_id>/msad/reports/<report_id>`

Elimina el archivo de reporte especificado por `<report_id>` para el cliente.

### Validaciones y manejo de errores
- Si el archivo no existe:
```json
{
  "success": false,
  "error": "Reporte no encontrado",
  "report_id": "<report_id>",
  "client_id": "<client_id>"
}
```
- Si ocurre un error al eliminar el archivo:
```json
{
  "success": false,
  "error": "<mensaje de error>",
  "report_id": "<report_id>",
  "client_id": "<client_id>"
}
```

**Request:**
```http
DELETE /api/clients/greenhouse-1/msad/reports/report_20250401_20250410_sensors_20250426_120000
```

**Response exitosa:**
```json
{
  "success": true,
  "message": "Reporte eliminado correctamente",
  "report_id": "report_20250401_20250410_sensors_20250426_120000",
  "filename": "greenhouse-1_sensors_2025-04-01_to_2025-04-10_20250426_120000.json",
  "client_id": "greenhouse-1"
}
```

### Notas
- Se puede eliminar tanto por nombre de archivo como por `report_id`.
- El sistema valida siempre la existencia y permisos antes de eliminar.

---

## 6. Programador automático de reportes (Scheduler)

Permite automatizar la generación periódica de reportes para un cliente, rango de fechas, tipo de datos y formato. El sistema es robusto ante errores y valida todos los parámetros antes de iniciar la programación.

### Parámetros requeridos y validaciones
- `interval_hours`: entero, obligatorio. Mayor que 0.
- `client_id`, `start_date`, `end_date`, `data_type`, `format`: igual que en la generación manual de reportes.

### Ejemplo de inicio/reinicio del scheduler
**POST** `/api/msad/reports/scheduler/start`

**Request:**
```http
POST /api/msad/reports/scheduler/start
Content-Type: application/json
{
  "interval_hours": 24,
  "client_id": "greenhouse-1",
  "start_date": "2025-04-01",
  "end_date": "2025-04-10",
  "data_type": "sensors",
  "format": "json"
}
```

**Response exitosa:**
```json
{
  "success": true,
  "message": "Programador de reportes iniciado",
  "config": {
    "interval_hours": 24,
    "client_id": "greenhouse-1",
    "start_date": "2025-04-01",
    "end_date": "2025-04-10",
    "data_type": "sensors",
    "format": "json"
  }
}
```

### Errores comunes
- Si falta algún parámetro o es inválido:
```json
{
  "success": false,
  "error": "<mensaje explicativo>"
}
```

### Detener el programador
**POST** `/api/msad/reports/scheduler/stop`

**Response:**
```json
{
  "success": true,
  "message": "Programador de reportes detenido"
}
```

### Consultar el estado del programador
**GET** `/api/msad/reports/scheduler/status`

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "config": {
    "interval_hours": 24,
    "client_id": "greenhouse-1",
    "start_date": "2025-04-01",
    "end_date": "2025-04-10",
    "data_type": "sensors",
    "format": "json"
  },
  "last_run": "2025-04-26T16:00:00",
  "next_run": "2025-04-27T16:00:00"
}
```

### Notas y mejores prácticas
- Puedes cambiar la configuración enviando un nuevo POST a `/scheduler/start` con diferentes parámetros.
- El programador ejecutará la generación de reportes automáticamente en el intervalo definido.
- El estado muestra la última y próxima ejecución programada.
- Todos los errores y eventos importantes quedan registrados en logs para auditoría.
- Si ocurre un error durante la ejecución automática, el sistema lo reporta en logs y continúa funcionando para futuros ciclos.

### Detener el programador de reportes

**POST** `/api/msad/reports/scheduler/stop`

**Request:**
```http
POST /api/msad/reports/scheduler/stop
```

**Response:**
```json
{
  "success": true,
  "message": "Programador de reportes detenido"
}
```

### Consultar el estado del programador de reportes

**GET** `/api/msad/reports/scheduler/status`

**Request:**
```http
GET /api/msad/reports/scheduler/status
```

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "config": {
    "interval_hours": 24,
    "client_id": "greenhouse-1",
    "start_date": "2025-04-01",
    "end_date": "2025-04-10",
    "data_type": "sensors",
    "format": "json"
  },
  "last_run": "2025-04-26T16:00:00",
  "next_run": "2025-04-27T16:00:00"
}
```

**Notas:**
- Puedes cambiar la configuración enviando un nuevo POST a `/scheduler/start` con diferentes parámetros.
- El programador ejecutará la generación de reportes automáticamente en el intervalo definido.
- El estado muestra la última y próxima ejecución programada.

---
