# Endpoints de Reportes – MSAD

---

**POST** http://192.168.184.223:5000/api/clients/<client_id>/msad/reports

```http
POST /api/clients/mushroom1/msad/reports
Content-Type: application/json
{
  "start_date": "2025-04-01",
  "end_date": "2025-04-10",
  "data_type": "sensors",
  "format": "json"
}
```
Respuesta:
```json
{
  "success": true,
  "filename": "mushroom1_sensors_20250401_to_20250410_20250426_143022.json",
  "records": 128,
  "size": 12345,
  "download_url": "/api/clients/mushroom1/msad/reports/download/mushroom1_sensors_20250401_to_20250410_20250426_143022.json"
}
```
---
**GET** http://192.168.184.223:5000/api/clients/<client_id>/msad/reports

```http
GET /api/clients/mushroom1/msad/reports?format=json&data_type=sensors
```
Respuesta:
```json
{
  "success": true,
  "reports": [
    {
      "filename": "mushroom1_sensors_20250401_to_20250410.json",
      "created_at": "2025-04-26T12:00:00",
      "size": 12345,
      "format": "json",
      "data_type": "sensors",
      "download_url": "/api/clients/mushroom1/msad/reports/download/mushroom1_sensors_20250401_to_20250410.json"
    }
  ],
  "total": 1
}
```
---
**GET** http://192.168.184.223:5000/api/clients/<client_id>/msad/reports/download/<filename>

```http
GET /api/clients/mushroom1/msad/reports/download/mushroom1_sensors_20250401_to_20250410.json
```
Respuesta: descarga directa del archivo (json o csv)
---
**GET** http://192.168.184.223:5000/api/msad/reports/scheduler/status?client_id=<client_id>

```http
GET /api/msad/reports/scheduler/status?client_id=mushroom1
```
Respuesta:
```json
{
  "success": true,
  "is_running": true,
  "config": {
    "interval_hours": 24,
    "client_id": "mushroom1",
    "start_date": "2025-04-01",
    "end_date": "2025-04-10",
    "data_type": "sensors",
    "format": "json"
  },
  "last_run": "2025-04-26T16:00:00",
  "next_run": "2025-04-27T16:00:00"
}
```
---
**POST** http://192.168.184.223:5000/api/msad/reports/scheduler/start

```http
POST /api/msad/reports/scheduler/start
Content-Type: application/json
{
  "interval_hours": 24,
  "client_id": "mushroom1",
  "start_date": "2025-04-01",
  "end_date": "2025-04-10",
  "data_type": "sensors",
  "format": "json"
}
```
Respuesta:
```json
{
  "success": true,
  "message": "Programador de reportes iniciado",
  "config": {
    "interval_hours": 24,
    "client_id": "mushroom1",
    "start_date": "2025-04-01",
    "end_date": "2025-04-10",
    "data_type": "sensors",
    "format": "json"
  }
}
```
---
**POST** http://192.168.184.223:5000/api/msad/reports/scheduler/stop

```http
POST /api/msad/reports/scheduler/stop
Content-Type: application/json
{
  "client_id": "mushroom1"
}
```
Respuesta:
```json
{
  "success": true,
  "message": "Programador de reportes detenido"
}
```

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
