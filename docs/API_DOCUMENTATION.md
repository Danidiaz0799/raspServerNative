# Documentación de la API RESTful - Servidor de Cultivo

Esta API permite interactuar con el servidor Flask para monitorear y controlar el sistema de cultivo distribuido. Todos los endpoints están bajo el prefijo `/api`. La base para las URLs de ejemplo es `http://raspserver.local:5000`.

## Autenticación

Actualmente, la API no implementa un sistema de autenticación explícito.

## Formato de Respuesta

*   **Éxito:** Generalmente `200 OK` o `201 Created` con un cuerpo JSON que contiene los datos solicitados o un mensaje de éxito.
*   **Error del Cliente:** `4xx` (ej. `400 Bad Request`, `404 Not Found`) con un cuerpo JSON describiendo el error: `{ "error": "Mensaje descriptivo" }`.
*   **Error del Servidor:** `500 Internal Server Error` con un cuerpo JSON: `{ "error": "Mensaje de error interno" }`.

---

## Endpoints Principales

### Clientes (`/clients`)

Gestiona los dispositivos cliente (nodos de cultivo) registrados en el sistema.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene una lista de todos los clientes registrados.</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>Ninguno</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[
  {
    "client_id": "...",
    "name": "...",
    "description": "...",
    "status": "online/offline",
    "last_seen": "..."
  },
  ...
]
```
</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/clients</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Registra un nuevo cliente (nodo de cultivo).</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "client_id": "string",
  "name": "string",
  "description": "string (opcional)"
}
```
*Requiere `client_id` y `name`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (201 Created)</strong></td>
<td>

```json
{ "message": "Cliente registrado correctamente" }
```
</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene los detalles de un cliente específico.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "client_id": "...",
  "name": "...",
  "description": "...",
  "status": "...",
  "last_seen": "..."
}
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>PUT /api/clients/{client_id}/status</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Actualiza el estado de conexión de un cliente (online/offline). Actualiza `last_seen` al pasar a 'online'.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{ "status": "online" | "offline" }
```
*Requiere `status`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Estado actualizado correctamente" }
```
</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>PUT /api/clients/{client_id}/info</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Actualiza la información (nombre y descripción) de un cliente existente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "name": "string",
  "description": "string (opcional)"
}
```
*Requiere `name`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Informacion del cliente actualizada correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>DELETE /api/clients/{client_id}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Elimina un cliente y todos sus datos asociados. ¡Usar con precaución!</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Cliente y todos sus datos eliminados correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

### Sensores (`/clients/<client_id>/...`)

Gestiona los datos de los sensores y los parámetros ideales por cliente.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/Sht3xSensor</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene datos históricos del sensor SHT3x para un cliente, con paginación.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `page` (integer, opcional, default=1)<br>• `pageSize` (integer, opcional, default=10)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[
  {
    "id": integer,
    "client_id": "...",
    "timestamp": "...",
    "temperature": float,
    "humidity": float
  },
  ...
]
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/Sht3xSensorManual</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene datos históricos del sensor SHT3x (propósito específico no claro, similar al anterior).</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `page` (integer, opcional, default=1)<br>• `pageSize` (integer, opcional, default=10)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[ { "id": integer, ... }, ... ]
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/IdealParams/{param_type}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene los parámetros ideales (min/max) para un tipo específico (`temperature` o `humidity`) para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `param_type` (string: "temperature" | "humidity")</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "id": integer,
  "client_id": "...",
  "param_type": "...",
  "min_value": float,
  "max_value": float
}
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente o los parámetros no existen.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>PUT /api/clients/{client_id}/IdealParams/{param_type}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Establece o actualiza los parámetros ideales (min/max) para un tipo específico y cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `param_type` (string: "temperature" | "humidity")</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "min_value": float,
  "max_value": float
}
```
*Requiere ambos.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Parametros ideales actualizados exitosamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

### Eventos (`/clients/<client_id>/Event`)

Gestiona los eventos registrados por el sistema para un cliente.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/Event</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene una lista paginada de eventos del sistema para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `page` (integer, opcional, default=1)<br>• `pageSize` (integer, opcional, default=10)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[
  {
    "id": integer,
    "client_id": "...",
    "timestamp": "...",
    "message": "...",
    "topic": "..."
  },
  ...
]
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/clients/{client_id}/Event</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Guarda un nuevo evento para un cliente (generalmente usado internamente).</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "message": "string",
  "topic": "string"
}
```
*Requiere ambos.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (201 Created)</strong></td>
<td>

```json
{ "message": "Evento guardado correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/Event/FilterByTopic</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene eventos para un cliente filtrados por tópico MQTT, con paginación.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `topic` (string, **requerido**)<br>• `page` (integer, opcional, default=1)<br>• `pageSize` (integer, opcional, default=10)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[ { "id": integer, ... }, ... ]
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error</strong></td>
<td>• 400 Bad Request: Si falta `topic`.<br>• 404 Not Found: Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>DELETE /api/clients/{client_id}/Event/{id}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Elimina un evento específico por su ID numérico para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `id` (integer)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Evento eliminado correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error</strong></td>
<td>• 404 Not Found: Si el cliente no existe.<br>• 500 Internal Server Error: Si el evento no existe o hay otro error.</td>
</tr>
</table>

### Actuadores (`/clients/<client_id>/Actuator`)

Gestiona el estado y control de los actuadores por cliente.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/Actuator</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene el estado actual de todos los actuadores registrados para un cliente específico.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
[
  {
    "id": integer,
    "client_id": "...",
    "name": "...",
    "state": ..., 
    "last_changed": "..."
  },
  ...
]
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/clients/{client_id}/Actuator</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Registra un nuevo actuador para un cliente con su estado inicial.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "name": "string",
  "state": "string | integer | boolean"
}
```
*Requiere ambos.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (201 Created)</strong></td>
<td>

```json
{ "message": "Actuador agregado correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>PUT /api/clients/{client_id}/Actuator/{id}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Actualiza el estado de un actuador específico por su ID numérico para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `id` (integer)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{ "state": "string | integer | boolean" }
```
*Requiere `state`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Estado del actuador actualizado correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/clients/{client_id}/Actuator/toggle_light</code><br>
<code>POST /api/clients/{client_id}/Actuator/toggle_fan</code><br>
<code>POST /api/clients/{client_id}/Actuator/toggle_humidifier</code><br>
<code>POST /api/clients/{client_id}/Actuator/toggle_motor</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Envía un comando para cambiar el estado de un actuador específico (luz, ventilador, etc.) para un cliente. Publica un mensaje MQTT.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{ "state": "on" | "off" | boolean | number }
```
*Requiere `state`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Senal enviada correctamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error</strong></td>
<td>• 404 Not Found: Si el cliente no existe.<br>• 400 Bad Request: Si falta `state`.</td>
</tr>
</table>

### Estado de la Aplicación (`/clients/<client_id>/...State`)

Gestiona el modo de operación (automático/manual) por cliente.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/getState</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene el modo de control actual para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "mode": "manual" | "automatico" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente o su estado no se encuentran.</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>PUT /api/clients/{client_id}/updateState</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Actualiza el modo de control para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{ "mode": "manual" | "automatico" }
```
*Requiere `mode`.*
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "message": "Estado de la aplicacion actualizado exitosamente" }
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error</strong></td>
<td>• 400 Bad Request: Si el modo es inválido.<br>• 404 Not Found: Si el cliente no existe.</td>
</tr>
</table>

### Estadísticas (`/clients/<client_id>/statistics`)

Proporciona estadísticas calculadas sobre los datos.

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/statistics/dashboard</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene estadísticas agregadas (min, max, prom) de T/H para un cliente durante los últimos 'N' días.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>`days` (integer, opcional, default=7)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "sht3x_stats": {
    "client_id": "...",
    "period_days": integer,
    "temperature": { "min": float | null, "max": float | null, "avg": float | null },
    "humidity": { "min": float | null, "max": float | null, "avg": float | null },
    "record_count": integer
  }
}
```
</td>
</tr>
<tr>
<td><strong>Respuesta Error (404 Not Found)</strong></td>
<td>Si el cliente no existe.</td>
</tr>
</table>

---

## Endpoints MSAD (Módulo de Almacenamiento y Datos)

Estos endpoints gestionan los backups y reportes del sistema. (Para detalles de respuesta, ver `MSAD_DETAILS.md`).

### MSAD - Estado (`/msad/status`)

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/msad/status</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Verifica que el módulo MSAD integrado esté activo.</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "success": true,
  "service": "msad",
  "version": "1.1.0", /* Puede variar */
  "status": "running"
}
```
</td>
</tr>
</table>

### MSAD - Backups (`/msad/backups`)

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/msad/backups</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Lista todos los archivos de backup disponibles.</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>`type` (string, opcional: "manual" | "auto")</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con lista de backups (ver `MSAD_DETAILS.md`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/msad/backups/create</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Crea un backup manual inmediato de `sensor_data.db`.</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con detalles del backup creado (ver `MSAD_DETAILS.md`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/msad/backups/download/{filename}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Descarga el archivo de backup (`.db`) especificado.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`filename` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Archivo binario (`Content-Type: application/octet-stream`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>DELETE /api/msad/backups/{filename}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Elimina un archivo de backup específico.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`filename` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{ "success": true, "message": "Backup <filename> eliminado correctamente" }
```
</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/msad/backups/restore/{filename}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Restaura `sensor_data.db` desde un backup. **¡Sobrescribe BD actual!**</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`filename` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "success": true,
  "message": "Backup <filename> restaurado correctamente",
  "safety_backup": "<nombre_backup_seguridad.db>"
}
```
</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/msad/backups/scheduler</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Obtiene el estado del planificador de backups automáticos.</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con estado del scheduler (ver `MSAD_DETAILS.md`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/msad/backups/scheduler</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Configura el planificador de backups automáticos.</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON, opcional)</strong></td>
<td>

```json
{
  "enabled": boolean,
  "interval_hours": integer
}
```
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "success": true,
  "message": "...",
  "status": { ... estado actual ... }
}
```
</td>
</tr>
</table>

### MSAD - Reportes (`/clients/<client_id>/msad/reports`, `/msad/reports`)

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>POST /api/clients/{client_id}/msad/reports</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Genera un reporte de datos históricos para un cliente.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Cuerpo (JSON)</strong></td>
<td>

```json
{
  "start_date": "YYYY-MM-DD", /* Requerido */
  "end_date": "YYYY-MM-DD",   /* Requerido */
  "data_type": "sensors" | "events" | "actuators", /* Opcional */
  "format": "json" | "csv"  /* Opcional */
}
```
</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con metadatos del reporte (ver `MSAD_DETAILS.md`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/msad/reports</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Lista los reportes generados para un cliente específico.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>`client_id` (string)</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `format` (string, opcional)<br>• `data_type` (string, opcional)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con lista de reportes (ver `MSAD_DETAILS.md`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/msad/reports</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Lista todos los reportes generados para todos los clientes.</td>
</tr>
<tr>
<td><strong>Parámetros Query</strong></td>
<td>• `format` (string, opcional)<br>• `data_type` (string, opcional)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Objeto JSON con lista de reportes (igual estructura que el anterior).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>GET /api/clients/{client_id}/msad/reports/download/{filename}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Descarga un archivo de reporte generado específico.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `filename` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>Archivo JSON o CSV (`Content-Type: application/json` o `text/csv`).</td>
</tr>
</table>

<table>
<tr>
<td><strong>Endpoint</strong></td>
<td><code>DELETE /api/clients/{client_id}/msad/reports/{report_id}</code></td>
</tr>
<tr>
<td><strong>Descripción</strong></td>
<td>Elimina un archivo de reporte específico usando el `report_id`.</td>
</tr>
<tr>
<td><strong>Parámetros Path</strong></td>
<td>• `client_id` (string)<br>• `report_id` (string)</td>
</tr>
<tr>
<td><strong>Respuesta Éxito (200 OK)</strong></td>
<td>

```json
{
  "success": true,
  "message": "Reporte eliminado",
  "report_id": "...",
  "filename": "...",
  "client_id": "..."
}
```
</td>
</tr>
</table> 