# Endpoints de Reportes – MSAD

---

## 1. Crear un reporte de datos

**POST** `/api/clients/<client_id>/msad/reports`

Crea un reporte de datos para un cliente, en formato JSON o CSV, para un rango de fechas y tipo de datos.

**Request:**
```http
POST /api/clients/greenhouse-1/msad/reports
Content-Type: application/json

{
  "start_date": "2025-04-01",
  "end_date": "2025-04-10",
  "data_type": "sensors",   // Opcional: 'sensors', 'events', 'actuators'
  "format": "json"           // Opcional: 'json' (por defecto) o 'csv'
}
```

**Response:**
```json
{
  "success": true,
  "report_id": "report_20250401_20250410_sensors.json",
  "filename": "report_20250401_20250410_sensors.json",
  "path": "/ruta/a/reports/report_20250401_20250410_sensors.json",
  "format": "json",
  "created_at": "2025-04-10T12:00:00",
  "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_20250401_20250410_sensors.json"
}
```

---

## 2. Listar reportes de un cliente

**GET** `/api/clients/<client_id>/msad/reports`

Lista todos los reportes generados para un cliente.
- Parámetros opcionales: `format`, `data_type`

**Request:**
```http
GET /api/clients/greenhouse-1/msad/reports?format=json&data_type=sensors
```

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "report_id": "report_20250401_20250410_sensors.json",
      "filename": "report_20250401_20250410_sensors.json",
      "format": "json",
      "created_at": "2025-04-10T12:00:00",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_20250401_20250410_sensors.json"
    }
  ]
}
```

---

## 3. Listar todos los reportes del sistema

**GET** `/api/msad/reports`

Lista todos los reportes generados en el sistema (de todos los clientes).
- Parámetros opcionales: `format`, `data_type`

**Request:**
```http
GET /api/msad/reports?format=json&data_type=sensors
```

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "report_id": "report_20250401_20250410_sensors.json",
      "filename": "report_20250401_20250410_sensors.json",
      "format": "json",
      "created_at": "2025-04-10T12:00:00",
      "download_url": "/api/clients/greenhouse-1/msad/reports/download/report_20250401_20250410_sensors.json"
    }
  ]
}
```

---

## 4. Descargar un reporte específico

**GET** `/api/clients/<client_id>/msad/reports/download/<filename>`

Descarga el archivo de reporte especificado por `<filename>` para el cliente.

**Request:**
```http
GET /api/clients/greenhouse-1/msad/reports/download/report_20250401_20250410_sensors.json
```

**Response:**
- Descarga directa del archivo solicitado (binario, JSON o CSV).

---

## 5. Eliminar un reporte específico

**DELETE** `/api/clients/<client_id>/msad/reports/<report_id>`

Elimina el archivo de reporte especificado por `<report_id>` para el cliente.

**Request:**
```http
DELETE /api/clients/greenhouse-1/msad/reports/report_20250401_20250410_sensors.json
```

**Response:**
```json
{
  "success": true,
  "message": "Reporte eliminado correctamente",
  "report_id": "report_20250401_20250410_sensors.json",
  "filename": "report_20250401_20250410_sensors.json",
  "client_id": "greenhouse-1"
}
```

---
