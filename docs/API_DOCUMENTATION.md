# Documentación de la API RESTful - Servidor de Cultivo

Esta API permite interactuar con el servidor Flask para monitorear y controlar el sistema de cultivo. Todos los endpoints están bajo el prefijo `/api`.

## Autenticación

Actualmente, la API no implementa un sistema de autenticación explícito.

## Formato de Respuesta

*   **Éxito:** Generalmente `200 OK` con un cuerpo JSON que contiene los datos solicitados o un mensaje de éxito.
*   **Error del Cliente:** `4xx` (ej. `400 Bad Request`, `404 Not Found`) con un cuerpo JSON describiendo el error: `{ "success": false, "error": "Mensaje descriptivo" }`.
*   **Error del Servidor:** `500 Internal Server Error` con un cuerpo JSON: `{ "success": false, "error": "Mensaje de error interno" }`.

---

## Endpoints Principales

### Clientes (`/clients`)

Gestiona los dispositivos cliente MQTT conectados al sistema.

*   **`GET /clients`**
    *   Descripción: Obtiene una lista de todos los clientes registrados.
    *   Respuesta Éxito (`200 OK`): `[ { "client_id": "...", "device_type": "...", "location": "...", "status": "online/offline", "enabled": true/false, "last_seen": "..." }, ... ]`

*   **`POST /clients`**
    *   Descripción: Registra un nuevo cliente (típicamente llamado por el propio cliente vía MQTT, pero expuesto en API).
    *   Body (JSON): `{ "client_id": "string", "device_type": "string", "location": "string" }`
    *   Respuesta Éxito (`201 Created` o `200 OK` si ya existe): `{ "success": true, "message": "Cliente registrado/actualizado", "client_id": "..." }`

*   **`GET /clients/<client_id>`**
    *   Descripción: Obtiene los detalles de un cliente específico.
    *   Path Params: `client_id` (string)
    *   Respuesta Éxito (`200 OK`): `{ "client_id": "...", ... }`
    *   Respuesta Error (`404 Not Found`): Si el cliente no existe.

*   **`PUT /clients/<client_id>/status`**
    *   Descripción: Actualiza el estado de conexión de un cliente (online/offline). Usado internamente por el sistema MQTT.
    *   Path Params: `client_id` (string)
    *   Body (JSON): `{ "status": "online" | "offline" }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Estado actualizado" }`

*   **`PUT /clients/<client_id>/enable`**
    *   Descripción: Habilita o deshabilita un cliente (afecta si se procesan sus datos o se controla).
    *   Path Params: `client_id` (string)
    *   Body (JSON): `{ "enabled": true | false }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Cliente habilitado/deshabilitado" }`

*   **`PUT /clients/<client_id>`**
    *   Descripción: Actualiza la información general de un cliente.
    *   Path Params: `client_id` (string)
    *   Body (JSON): `{ "device_type": "string", "location": "string" }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Información actualizada" }`

*   **`DELETE /clients/<client_id>`**
    *   Descripción: Elimina un cliente y todos sus datos asociados (sensores, eventos, etc.). ¡Usar con precaución!
    *   Path Params: `client_id` (string)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Cliente eliminado" }`

### Sensores (`/sensors`)

Gestiona los datos de los sensores y los parámetros ideales.

*   **`GET /sensors/sht3x`**
    *   Descripción: Obtiene datos históricos del sensor SHT3x.
    *   Query Params (opcionales):
        *   `client_id` (string): Filtra por cliente.
        *   `start_time` (string, ISO 8601): Fecha/hora de inicio.
        *   `end_time` (string, ISO 8601): Fecha/hora de fin.
        *   `limit` (integer): Número máximo de registros.
    *   Respuesta Éxito (`200 OK`): `[ { "timestamp": "...", "client_id": "...", "temperature": float, "humidity": float }, ... ]`

*   **`GET /sensors/ideal_params/<client_id>`**
    *   Descripción: Obtiene los parámetros ideales de temperatura y humedad para el control automático de un cliente.
    *   Path Params: `client_id` (string)
    *   Respuesta Éxito (`200 OK`): `{ "client_id": "...", "ideal_temp_min": float, "ideal_temp_max": float, "ideal_humidity_min": float, "ideal_humidity_max": float }`

*   **`POST /sensors/ideal_params/<client_id>`**
    *   Descripción: Establece o actualiza los parámetros ideales para un cliente.
    *   Path Params: `client_id` (string)
    *   Body (JSON): `{ "ideal_temp_min": float, "ideal_temp_max": float, "ideal_humidity_min": float, "ideal_humidity_max": float }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Parámetros ideales actualizados" }`

### Eventos (`/events`)

Gestiona los eventos registrados por el sistema.

*   **`GET /events`**
    *   Descripción: Obtiene una lista de eventos del sistema.
    *   Query Params (opcionales):
        *   `client_id` (string)
        *   `event_type` (string)
        *   `start_time` (string, ISO 8601)
        *   `end_time` (string, ISO 8601)
        *   `limit` (integer)
    *   Respuesta Éxito (`200 OK`): `[ { "id": integer, "timestamp": "...", "client_id": "...", "event_type": "...", "message": "...", "details": "..." }, ... ]`

*   **`POST /events`**
    *   Descripción: Guarda un nuevo evento (generalmente usado internamente).
    *   Body (JSON): `{ "client_id": "string", "event_type": "string", "message": "string", "details": "json_string_o_null" }`
    *   Respuesta Éxito (`201 Created`): `{ "success": true, "message": "Evento guardado", "event_id": integer }`

*   **`GET /events/topic/<topic>`**
    *   Descripción: Obtiene eventos filtrados por un tópico MQTT específico (puede ser menos útil que el GET general).
    *   Path Params: `topic` (string)
    *   Respuesta Éxito (`200 OK`): `[ { ...evento... }, ... ]`

*   **`PUT /events/<event_id>`**
    *   Descripción: Actualiza un evento existente (uso limitado).
    *   Path Params: `event_id` (integer)
    *   Body (JSON): `{ "message": "string", "details": "json_string_o_null" }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Evento actualizado" }`

*   **`DELETE /events/<event_id>`**
    *   Descripción: Elimina un evento específico.
    *   Path Params: `event_id` (integer)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Evento eliminado" }`

### Actuadores (`/actuators`)

Gestiona el estado y control de los actuadores (luces, ventiladores, etc.).

*   **`GET /actuators`**
    *   Descripción: Obtiene el estado actual de todos los actuadores, opcionalmente filtrado por cliente.
    *   Query Params (opcional): `client_id` (string)
    *   Respuesta Éxito (`200 OK`): `[ { "client_id": "...", "name": "...", "type": "...", "state": ..., "last_changed": "..." }, ... ]`

*   **`POST /actuators`**
    *   Descripción: Guarda el estado inicial de un actuador (usado internamente).
    *   Body (JSON): `{ "client_id": "string", "name": "string", "type": "string", "state": "string/int/bool" }`
    *   Respuesta Éxito (`201 Created`): `{ "success": true, "message": "Estado inicial guardado" }`

*   **`GET /actuators/<name>`**
    *   Descripción: Obtiene el estado de un actuador específico para un cliente dado.
    *   Path Params: `name` (string, ej. "light1")
    *   Query Params: `client_id` (string, **requerido**)
    *   Respuesta Éxito (`200 OK`): `{ "client_id": "...", "name": "...", ... }`

*   **`PUT /actuators/<name>`**
    *   Descripción: Actualiza el estado de un actuador (usado internamente al recibir confirmación MQTT).
    *   Path Params: `name` (string)
    *   Body (JSON): `{ "client_id": "string", "state": ..., "last_changed": "ISO 8601 string" }`
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Estado actualizado" }`

*   **`POST /actuators/<name>/<action>`**
    *   Descripción: Envía un comando manual a un actuador (ej. encender/apagar). Publica un mensaje MQTT.
    *   Path Params:
        *   `name` (string): Nombre del actuador (ej. "light1", "fan").
        *   `action` (string): Acción a realizar (ej. "on", "off", "toggle").
    *   Body (JSON): `{ "client_id": "string" }` (El ID del cliente al que pertenece el actuador)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Comando enviado a MQTT", "topic": "...", "payload": "..." }`
    *   Respuesta Error (`400 Bad Request`): Si el cliente o actuador no se encuentra, o la acción no es válida.

### Estado de la Aplicación (`/state`)

Gestiona configuraciones específicas por cliente, como el modo de control.

*   **`GET /state/<client_id>`**
    *   Descripción: Obtiene el estado de la aplicación para un cliente (ej. modo 'auto' o 'manual').
    *   Path Params: `client_id` (string)
    *   Respuesta Éxito (`200 OK`): `{ "control_mode": "auto" | "manual", ...otros estados... }` (Devuelve un objeto con todos los pares clave-valor de estado para ese cliente)

*   **`POST /state/<client_id>`**
    *   Descripción: Actualiza un valor de estado específico para un cliente.
    *   Path Params: `client_id` (string)
    *   Body (JSON): `{ "state_key": "string", "state_value": "any" }` (ej. `{ "state_key": "control_mode", "state_value": "manual" }`)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Estado actualizado" }`

### Estadísticas (`/statistics`)

Proporciona estadísticas calculadas sobre los datos.

*   **`GET /statistics/<client_id>`**
    *   Descripción: Obtiene estadísticas agregadas (mín, máx, prom) de temperatura y humedad para un cliente durante un período.
    *   Path Params: `client_id` (string)
    *   Query Params (opcional): `period` (string, ej. "last_24h", "last_7d", "all_time", default="last_24h")
    *   Respuesta Éxito (`200 OK`): `{ "client_id": "...", "period": "...", "temperature": { "min": float, "max": float, "avg": float }, "humidity": { "min": float, "max": float, "avg": float }, "record_count": integer }`

---

## Endpoints MSAD (Microservicio de Almacenamiento y Datos)

Estos endpoints gestionan los backups, reportes y datos de prueba del sistema.

### MSAD - Estado (`/msad/status`)

*   **`GET /api/msad/status`**
    *   Descripción: Verifica que el módulo MSAD integrado esté activo.
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "service": "msad", "version": "1.0.0-minimal", "status": "running" }`

### MSAD - Datos de Prueba (`/msad/test-data`)

*   **`POST /api/msad/test-data`**
    *   Descripción: Inserta datos de sensores SHT3x aleatorios en la base de datos para facilitar las pruebas de reportes.
    *   Body (JSON):
        *   `client_id` (string, opcional, default="mushroom1"): ID del cliente para el que se generan los datos.
        *   `count` (integer, opcional, default=10): Número de registros de prueba a insertar.
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Se insertaron <count> registros de prueba para el cliente <client_id>", "count": <count> }`

### MSAD - Backups (`/msad/backups`)

*   **`GET /api/msad/backups`**
    *   Descripción: Lista todos los archivos de backup disponibles.
    *   Query Params (opcional): `type` (string, "manual" | "auto") para filtrar por tipo de backup.
    *   Respuesta Éxito (`200 OK`):
        ```json
        {
          "success": true,
          "backups": [
            {
              "backup_id": "backup_YYYYMMDD_HHMMSS",
              "filename": "sensor_data_type_YYYYMMDD_HHMMSS.db",
              "type": "manual" | "auto",
              "size": integer, // en bytes
              "created_at": "ISO 8601 timestamp",
              "download_url": "/api/msad/backups/download/<filename>"
            }
            // ... más backups
          ],
          "total": integer // número total de backups listados
        }
        ```

*   **`POST /api/msad/backups/create`**
    *   Descripción: Dispara la creación de un backup manual inmediato de la base de datos principal (`sensor_data.db`).
    *   Respuesta Éxito (`200 OK`):
        ```json
        {
          "success": true,
          "backup_id": "backup_YYYYMMDD_HHMMSS",
          "filename": "sensor_data_manual_YYYYMMDD_HHMMSS.db",
          "path": "/ruta/completa/al/backup/....db", // Ruta en el servidor
          "size": integer, // en bytes
          "type": "manual",
          "created_at": "ISO 8601 timestamp",
          "download_url": "/api/msad/backups/download/<filename>"
        }
        ```
    *   Respuesta Error (`400 Bad Request`, `500 Internal Server Error`): Si falla la creación.

*   **`GET /api/msad/backups/download/<filename>`**
    *   Descripción: Descarga el archivo de backup (`.db`) especificado.
    *   Path Params: `filename` (string)
    *   Respuesta Éxito (`200 OK`): El archivo binario de la base de datos como descarga (`Content-Type: application/octet-stream`).
    *   Respuesta Error (`404 Not Found`): `{ "success": false, "error": "Archivo de backup no encontrado" }`

*   **`DELETE /api/msad/backups/<filename>`**
    *   Descripción: Elimina un archivo de backup específico.
    *   Path Params: `filename` (string)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Backup <filename> eliminado correctamente" }`
    *   Respuesta Error (`404 Not Found`): Si el archivo no existe.

*   **`POST /api/msad/backups/restore/<filename>`**
    *   Descripción: Restaura la base de datos principal (`sensor_data.db`) usando el archivo de backup especificado. **¡Sobrescribe la BD actual!** Puede requerir reinicio del servidor.
    *   Path Params: `filename` (string)
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Backup <filename> restaurado correctamente", "safety_backup": "<nombre_backup_seguridad.db>" }` (Se crea un backup de seguridad de la BD actual antes de restaurar).
    *   Respuesta Error (`404 Not Found`, `400 Bad Request`, `500 Internal Server Error`): Si el archivo no existe o falla la restauración.

*   **`GET /api/msad/backups/scheduler`**
    *   Descripción: Obtiene el estado actual del planificador de backups automáticos.
    *   Respuesta Éxito (`200 OK`):
        ```json
        {
          "success": true,
          "is_running": true | false,
          "backup_count": integer, // backups existentes
          "total_size": integer, // tamaño total en bytes
          "formatted_size": "string", // ej. "2.44 MB"
          "last_backup": "ISO 8601 timestamp" | null,
          "next_backup": "ISO 8601 timestamp" | null,
          "backup_dir": "/ruta/al/directorio/de/backups"
        }
        ```

*   **`POST /api/msad/backups/scheduler`**
    *   Descripción: Configura (habilita/deshabilita o cambia intervalo) el planificador de backups automáticos.
    *   Body (JSON, opcional):
        *   `enabled` (boolean, opcional, default=true): Activa/desactiva el planificador.
        *   `interval_hours` (integer, opcional, default=24): Intervalo entre backups automáticos.
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Planificador actualizado/iniciado/detenido", "status": { ... estado actual del scheduler ... } }` (El objeto status es igual al de GET /scheduler).

### MSAD - Reportes (`/clients/<client_id>/msad/reports`, `/msad/reports`)

*   **`POST /api/clients/<client_id>/msad/reports`**
    *   Descripción: Genera un reporte de datos históricos para un cliente específico.
    *   Path Params: `client_id` (string)
    *   Body (JSON):
        *   `start_date` (string, "YYYY-MM-DD"): Fecha de inicio (requerida).
        *   `end_date` (string, "YYYY-MM-DD"): Fecha de fin (requerida).
        *   `data_type` (string, opcional, default="sensors"): Tipo de datos ("sensors", "events", "actuators"). Ver tabla en [MSAD_DETAILS.md](MSAD_DETAILS.md).
        *   `format` (string, opcional, default="json"): Formato del reporte ("json" | "csv"). Ver tabla en [MSAD_DETAILS.md](MSAD_DETAILS.md).
    *   Respuesta Éxito (`200 OK`):
        ```json
        {
          "success": true,
          "client_id": "<client_id>",
          "report_id": "report_YYYYMMDD_HHMMSS",
          "filename": "<client_id>_<data_type>_<start>_to_<end>_<timestamp>.<format>",
          "format": "json" | "csv",
          "data_type": "sensors" | "events" | "actuators",
          "period": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
          "size": integer, // tamaño en bytes
          "records": integer, // número de registros en el reporte
          "created_at": "ISO 8601 timestamp",
          "download_url": "/api/clients/<client_id>/msad/reports/download/<filename>"
        }
        ```
    *   Respuesta Error (`400 Bad Request`): `{ "success": false, "error": "Parámetros inválidos o no se encontraron datos" }`

*   **`GET /api/clients/<client_id>/msad/reports`**
    *   Descripción: Lista los reportes generados disponibles para un cliente específico.
    *   Path Params: `client_id` (string)
    *   Query Params (opcionales): `format` (string), `data_type` (string) para filtrar.
    *   Respuesta Éxito (`200 OK`):
        ```json
        {
          "success": true,
          "reports": [
            {
              "report_id": "report_YYYYMMDD_HHMMSS",
              "client_id": "<client_id>",
              "filename": "...",
              "format": "...",
              "data_type": "...",
              "size": integer,
              "created_at": "ISO 8601 timestamp",
              "download_url": "/api/clients/<client_id>/msad/reports/download/<filename>"
            }
            // ... más reportes
          ],
          "total": integer
        }
        ```

*   **`GET /api/msad/reports`**
    *   Descripción: Lista todos los reportes generados para **todos** los clientes.
    *   Query Params (opcionales): `format` (string), `data_type` (string) para filtrar.
    *   Respuesta Éxito (`200 OK`): Igual estructura que el endpoint anterior, pero con reportes de múltiples `client_id`.

*   **`GET /api/clients/<client_id>/msad/reports/download/<filename>`**
    *   Descripción: Descarga un archivo de reporte generado específico.
    *   Path Params: `client_id` (string), `filename` (string)
    *   Respuesta Éxito (`200 OK`): El archivo de reporte (JSON o CSV) como descarga (`Content-Type: application/json` o `text/csv`).
    *   Respuesta Error (`404 Not Found`): `{ "success": false, "error": "Archivo no encontrado" }`

*   **`DELETE /api/clients/<client_id>/msad/reports/<report_id>`**
    *   Descripción: Elimina un archivo de reporte específico. **Nota:** Usa el `report_id` devuelto al crear/listar el reporte (ej. `report_YYYYMMDD_HHMMSS`). Internamente busca el archivo asociado a ese ID.
    *   Path Params: `client_id` (string), `report_id` (string).
    *   Respuesta Éxito (`200 OK`): `{ "success": true, "message": "Reporte eliminado", "report_id": "...", "filename": "...", "client_id": "..." }`
    *   Respuesta Error (`404 Not Found`): Si el reporte/archivo no existe. 