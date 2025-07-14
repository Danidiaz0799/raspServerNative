# Endpoints de Backups – MSAD

---

## 1. Listar todos los backups

**GET** `/api/msad/backups`

Lista todos los backups disponibles (manuales y automáticos).

**Parámetros de filtro:**
- `type`: Permite filtrar por tipo de backup. Valores posibles:
  - `manual`: Solo backups manuales
  - `auto`: Solo backups automáticos
  - `scheduled`: Alias de `auto` (para compatibilidad con frontend)

**Ejemplos de uso:**
```http
GET http://192.168.184.223:5000/api/msad/backups?type=manual      # Solo backups manuales
GET http://192.168.184.223:5000/api/msad/backups?type=auto        # Solo backups automáticos
GET http://192.168.184.223:5000/api/msad/backups?type=scheduled   # Solo backups automáticos (alias)
GET http://192.168.184.223:5000/api/msad/backups                  # Todos los backups
```

**Nota:** El campo `type` en la respuesta será siempre `manual` o `auto` según corresponda.

**Response:**
```json
{
  "success": true,
  "backups": [
    {
      "backup_id": "backup_20250426_050105",
      "filename": "sensor_data_manual_20250426_050105.db",
      "type": "manual",
      "size": 204800,
      "created_at": "2025-04-26T05:01:05",
      "download_url": "/api/msad/backups/download/sensor_data_manual_20250426_050105.db"
    },
    {
      "backup_id": "backup_20250426_060000",
      "filename": "sensor_data_auto_20250426_060000.db",
      "type": "auto",
      "size": 204800,
      "created_at": "2025-04-26T06:00:00",
      "download_url": "http://192.168.184.223:5000/api/msad/backups/download/sensor_data_auto_20250426_060000.db"
    }
  ],
  "total": 2
}
```

---

## 2. Crear un backup manual

**POST http://192.168.184.223:5000/api/msad/backups/create**

Crea un backup inmediato (manual) de la base de datos.

```

**Response:**
```json
{
  "success": true,
  "backup_id": "backup_20250426_060000",
  "filename": "sensor_data_manual_20250426_060000.db",
  "path": "/ruta/a/backups/sensor_data_manual_20250426_060000.db",
  "size": 204800,
  "type": "manual",
  "created_at": "2025-04-26T06:00:00",
  "download_url": "http://192.168.184.223:5000/api/msad/backups/download/sensor_data_manual_20250426_060000.db"
}
```

---

## 3. Descargar un backup específico

**GET** `/api/msad/backups/download/<filename>`

Descarga el archivo de backup especificado por `<filename>`.

**Request:**
```http
GET http://192.168.184.223:5000/api/msad/backups/download/sensor_data_manual_20250426_050105.db
```

**Response:**
- Descarga directa del archivo solicitado (binario).

---

## 4. Eliminar un backup específico

**DELETE** `/api/msad/backups/<filename>`

Elimina el archivo de backup especificado por `<filename>`.

**Request:**
```http
DELETE http://192.168.184.223:5000/api/msad/backups/sensor_data_manual_20250426_060000.db
```

**Response:**
```json
{
  "success": true,
  "message": "Backup sensor_data_manual_20250426_060000.db eliminado correctamente"
}
```

---

## 5. Restaurar la base de datos desde un backup

**POST** `/api/msad/backups/restore/<filename>`

Restaura la base de datos usando el archivo de backup `<filename>`.
Antes de restaurar, crea automáticamente un backup de seguridad.

**Request:**
```http
POST http://192.168.184.223:5000/api/msad/backups/restore/sensor_data_manual_20250426_060000.db
```

**Response:**
```json
{
  "success": true,
  "message": "Backup sensor_data_manual_20250426_060000.db restaurado correctamente",
  "safety_backup": "sensor_data_manual_20250426_061000.db"
}
```

---

## 6. Obtener el estado del programador de backups

**GET** `/api/msad/backups/scheduler`

Devuelve el estado actual del programador automático de backups.

**Request:**
```http
GET http://192.168.184.223:5000/api/msad/backups/scheduler
```

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "interval_hours": 6,
  "backup_count": 3,
  "total_size": 614400,
  "formatted_size": "600.00 KB",
  "last_backup": "2025-04-26T06:00:00",
  "next_backup": "2025-04-26T12:00:00",
  "backup_dir": "/ruta/a/backups"
}
```

---

## 7. Configurar el programador de backups

**POST** `/api/msad/backups/scheduler`

Activa/desactiva el programador automático y/o cambia el intervalo de backups.

**Request:**
```http
POST http://192.168.184.223:5000/api/msad/backups/scheduler
Content-Type: application/json

{
  "enabled": true,
  "interval_hours": 6
}
```

**Response:**
```json
{
  "success": true,
  "message": "Backup scheduler started with interval of 6 hours",
  "status": {
    "success": true,
    "is_running": true,
    "interval_hours": 6,
    "backup_count": 3,
    "total_size": 614400,
    "formatted_size": "600.00 KB",
    "last_backup": "2025-04-26T06:00:00",
    "next_backup": "2025-04-26T12:00:00",
    "backup_dir": "/ruta/a/backups"
  }
}
```

---
