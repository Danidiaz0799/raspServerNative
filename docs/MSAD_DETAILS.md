# 📊 MSAD - Detalles del Módulo de Almacenamiento y Datos

<div align="center">

![Versión](https://img.shields.io/badge/Versión-1.0.0--minimal-blue)
![Integración](https://img.shields.io/badge/Integración-RaspServer-green)
![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)

</div>

## 📋 Índice

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Integración con RaspServer](#-integración-con-raspserver)
- [Esquema de Almacenamiento](#-esquema-de-almacenamiento)
- [Flujo de Trabajo](#-flujo-de-trabajo)
- [Instalación y Configuración Específica](#-instalación-y-configuración-específica)
- [Solución de Problemas](#-solución-de-problemas)

## 📝 Descripción

MSAD es un **módulo integrado y optimizado** dentro del servidor principal, enfocado en la generación y gestión de backups y reportes. Permite extraer, filtrar y exportar datos críticos del cultivo (sensores, eventos, actuadores) para facilitar análisis detallados, toma de decisiones y asegurar la persistencia de los datos.

### ✨ Características Clave

| Característica              | Descripción                                                    |
| :-------------------------- | :------------------------------------------------------------- |
| 🚀 **Alta Performance**     | Consultas optimizadas, bajo impacto en recursos.               |
| 🔄 **Formatos Múltiples**   | Exportación de reportes en JSON y CSV.                         |
| 💾 **Backups Robustos**     | Backups automáticos/manuales, restauración segura.             |
| ⏰ **Programación**         | Intervalo configurable para backups automáticos (`schedule`).   |
| 🔍 **Filtrado Avanzado**    | Selección por cliente, fechas, tipo de datos en reportes.      |
| 📂 **Gestión de Archivos**  | Almacenamiento organizado y API para listar/descargar/eliminar. |
| 🔗 **Integración Simple**   | API RESTful integrada en el servidor principal.                |

---

## 🏗 Arquitectura

MSAD opera como un módulo dentro de la aplicación Flask principal, interactuando con la base de datos común y exponiendo su funcionalidad a través de blueprints API específicos.

```
                    ┌───────────────────┐
                    │   Flask Server    │
                    │     (app.py)      │  <-- Inicializa MSAD
                    │                   │      Registra Blueprints MSAD
                    └─────────┬─────────┘
                              │ (Llamadas API /api/msad/*, /api/clients/.../msad/*)
                              ▼
┌─────────────────────────────────────────────────────┐
│                 MSAD Módulo Integrado               │
│                                                     │
│  ┌───────────────┐         ┌────────────────────┐  │
│  │  API Layer    │ ◄────► │     Core Layer     │  │
│  │ (Blueprints)  │         │ (backup.py,       │  │
│  │ api/*.py      │         │  reports.py,       │  │
│  │               │         │  system.py)        │  │
│  └───────────────┘         └─────────┬──────────┘  │
│                                      │ (Acceso DB)   │
└──────────────────────────────────────┼──────────────┘
                                       ▼
                             ┌──────────────────┐
                             │  Base de Datos   │
                             │   (SQLite -      │
                             │ sensor_data.db)  │
                             └──────────────────┘
```

*   **Capa API (`msad/api/`)**: Define los endpoints RESTful (usando Flask Blueprints) para interactuar con las funciones de MSAD.
*   **Capa Core (`msad/core/`)**: Contiene la lógica principal para backups, reportes y utilidades del sistema (manejo de rutas, logs).
*   **Base de Datos**: Accede directamente a `sensor_data.db`.

---

## 🎯 Funcionalidades Detalladas

### 📊 Gestión de Reportes

| Funcionalidad         | Descripción                                                                                                |
| :-------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Generación**        | Crea reportes históricos bajo demanda vía API (`POST /api/clients/{client_id}/msad/reports`).                |
| **Filtrado**          | Permite filtrar por `client_id`, `start_date`, `end_date`, `data_type` (`sensors`, `events`, `actuators`).   |
| **Formatos**          | Exporta a `JSON` o `CSV`.                                                                                  |
| **Consulta Datos**    | Accede a las tablas relevantes (`sht3x_data`, `events`, `actuator_log`) de `sensor_data.db`.                |
| **Gestión Archivos** | API para listar (`GET /api/.../reports`), descargar (`GET /api/.../download/...`) y eliminar (`DELETE /api/.../reports/...`) reportes. |

### 💾 Gestión de Backups

| Funcionalidad            | Descripción                                                                                                |
| :----------------------- | :--------------------------------------------------------------------------------------------------------- |
| **Backups Automáticos**  | Ejecución periódica configurable (`schedule`) de backups completos de `sensor_data.db`.                      |
| **Backups Manuales**     | Creación inmediata vía API (`POST /api/msad/backups/create`).                                               |
| **Listado y Descarga**   | API para listar (`GET /api/msad/backups`) y descargar (`GET /api/msad/backups/download/...`) archivos `.db`. |
| **Eliminación**          | API para eliminar backups específicos (`DELETE /api/msad/backups/...`).                                      |
| **Restauración Segura**  | Proceso API (`POST /api/msad/backups/restore/...`) que crea backup de seguridad antes de sobrescribir la BD. |
| **Gestión Planificador** | API para consultar estado (`GET`) y configurar (`POST`) el scheduler de backups automáticos (`/api/msad/backups/scheduler`). |

---

## 🔌 Integración con RaspServer

La integración se realiza en `app.py`:

1.  **Importación:** Se importan las funciones `init_msad`, `shutdown_msad` y los `create_*_blueprint` desde el paquete `msad`.
2.  **Registro de Blueprints:** Se crean y registran los blueprints de MSAD (`system_bp`, `backup_bp`, `report_bp`) en la aplicación Flask bajo el prefijo `/api`.
3.  **Inicialización:** Se llama a `init_msad()` al iniciar `app.py`, opcionalmente activando `auto_backup`.
4.  **Apagado Limpio:** Se registra `shutdown_msad()` con `atexit` para detener limpiamente el scheduler de backups al cerrar la aplicación.

```python
# Ejemplo simplificado en app.py
from msad import (
    init_msad, shutdown_msad,
    create_system_blueprint, create_backup_blueprint, create_report_blueprint
)
import atexit

# ... app = Flask(...) ...

# Registrar Blueprints
system_bp = create_system_blueprint()
backup_bp = create_backup_blueprint()
report_bp = create_report_blueprint()
app.register_blueprint(system_bp, url_prefix='/api')
app.register_blueprint(backup_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')

# Inicializar MSAD
msad_status = init_msad(auto_backup=True, backup_interval_hours=24)

# Registrar apagado
atexit.register(shutdown_msad) # Asumiendo que shutdown_msad detiene el scheduler

# ... app.run(...) ...
```

---

## 📂 Esquema de Almacenamiento

MSAD organiza sus archivos en una estructura configurable. La ruta base por defecto o recomendada es:

*   **Producción (Linux):** `/mnt/storage/msad/` (o similar, configurable)
*   **Desarrollo (Windows):** `storage/msad/` (relativa al proyecto)

```
<RUTA_BASE>/msad/
├── backups/
│   ├── sensor_data_auto_YYYYMMDD_HHMMSS.db
│   └── sensor_data_manual_YYYYMMDD_HHMMSS.db
├── reports/
│   ├── <client_id_1>/
│   │   ├── <client_id_1>_sensors_...<timestamp>.json
│   │   └── <client_id_1>_events_...<timestamp>.csv
│   └── <client_id_2>/
│       └── ...
└── logs/
    └── msad.log
```

**Importante:** Asegurar que la `<RUTA_BASE>/msad` y sus subdirectorios (`backups`, `reports`, `logs`) existan y tengan permisos de escritura para el usuario que ejecuta la aplicación Flask.

---

## 🔄 Flujo de Trabajo

A continuación se describen los flujos principales para las operaciones de reportes y backups.

### 📊 Generación y Consulta de Reportes

1.  **Creación de Reporte:**
    1.  El cliente (frontend/usuario) envía una petición `POST` a `/api/clients/{client_id}/msad/reports` incluyendo en el cuerpo JSON los filtros requeridos (`start_date`, `end_date`) y opcionales (`data_type`, `format`).
    2.  La capa API (`msad/api/report_routes.py`) recibe la solicitud y llama a la función correspondiente en la capa Core (`msad/core/reports.py`).
    3.  La capa Core consulta la base de datos `sensor_data.db` aplicando los filtros especificados.
    4.  Si se encuentran datos, se genera el archivo de reporte en el formato solicitado (JSON o CSV).
    5.  El archivo generado se almacena en la ruta configurada: `<RUTA_BASE>/msad/reports/{client_id}/`.
    6.  La API devuelve una respuesta JSON al cliente indicando el éxito y proporcionando metadatos del reporte generado (nombre de archivo, URL de descarga, número de registros, etc.).

2.  **Listado de Reportes:**
    1.  El cliente envía una petición `GET` a `/api/clients/{client_id}/msad/reports` (para un cliente) o `/api/msad/reports` (para todos), opcionalmente con parámetros query (`format`, `data_type`) para filtrar.
    2.  La capa API llama a la función de listado en la capa Core.
    3.  La capa Core examina el directorio de reportes (`<RUTA_BASE>/msad/reports/`), aplica los filtros si existen, y recopila los metadatos de los reportes encontrados.
    4.  La API devuelve una respuesta JSON con la lista de los reportes que coinciden con los criterios.

3.  **Descarga de Reporte:**
    1.  El cliente envía una petición `GET` a `/api/clients/{client_id}/msad/reports/download/{filename}`.
    2.  La capa API llama a la función correspondiente en la capa Core.
    3.  La capa Core localiza el archivo especificado dentro del directorio del cliente en `<RUTA_BASE>/msad/reports/`.
    4.  Si el archivo existe, el servidor lo envía como una descarga binaria con el `Content-Type` apropiado (JSON o CSV).

4.  **Eliminación de Reporte:**
    1.  El cliente envía una petición `DELETE` a `/api/clients/{client_id}/msad/reports/{report_id}`.
    2.  La capa API llama a la función de eliminación en la capa Core.
    3.  La capa Core busca el archivo asociado al `report_id` y lo elimina del sistema de archivos.
    4.  La API devuelve una respuesta JSON confirmando la eliminación.

### 💾 Proceso de Backup y Restauración

*   **Backups Automáticos:**
    1.  El planificador (`schedule`), configurado al iniciar `app.py` o vía API, ejecuta periódicamente (cada X horas) la tarea definida en `msad/core/backup.py`.
    2.  La tarea llama a la función `create_backup(manual=False)`.
    3.  Esta función realiza una copia del archivo `sensor_data.db`.
    4.  La copia se almacena en `<RUTA_BASE>/msad/backups/` con un nombre que indica la fecha, hora y tipo "auto".

*   **Operaciones Manuales vía API:**
    1.  **Crear Backup:** `POST /api/msad/backups/create` desencadena la llamada a `create_backup(manual=True)`, que guarda una copia en `backups/` con tipo "manual" y devuelve detalles en JSON.
    2.  **Listar Backups:** `GET /api/msad/backups` llama a `list_backups()`, que lee el contenido del directorio `backups/` y devuelve una lista JSON con los detalles.
    3.  **Restaurar Backup:** `POST /api/msad/backups/restore/{filename}` llama a `restore_backup()`:
        *   Primero, crea un backup de seguridad del `sensor_data.db` *actual*.
        *   Luego, lee el archivo `{filename}` desde `backups/`.
        *   Finalmente, reemplaza el `sensor_data.db` actual con el contenido del backup leído.
        *   Devuelve una respuesta JSON confirmando la operación y el nombre del backup de seguridad.
    4.  **Descargar Backup:** `GET /api/msad/backups/download/{filename}` llama a `get_backup_file()`, localiza el archivo en `backups/` y lo envía como descarga binaria.
    5.  **Eliminar Backup:** `DELETE /api/msad/backups/{filename}` llama a `delete_backup()`, que elimina el archivo especificado de `backups/` y devuelve confirmación.
    6.  **Consultar/Configurar Scheduler:** `GET` o `POST` a `/api/msad/backups/scheduler` interactúan con las funciones `get_backup_status()`, `start_backup_scheduler()` o `stop_backup_scheduler()` en `backup.py` para gestionar el estado del planificador `schedule`.

---

## ⚙️ Instalación y Configuración Específica

| Requisito/Paso               | Descripción                                                                                                | Acción / Verificación                                                                                                  |
| :--------------------------- | :--------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Dependencias**             | Asegurar que `schedule` esté en `requirements.txt` para backups automáticos.                               | Verificar `requirements.txt`; Ejecutar `pip install -r requirements.txt`.                                              |
| **Activación Backups Auto.** | Habilitar/configurar intervalo al iniciar `app.py` o vía API.                                                | Modificar `init_msad(auto_backup=True, ...)` en `app.py` O usar `POST /api/msad/backups/scheduler`.                    |
| **Permisos Directorios**     | El directorio base de MSAD y sus subdirectorios (`backups`, `reports`, `logs`) deben existir y ser escribibles. | Crear directorios (`mkdir -p ...`); Asignar permisos (`sudo chown -R user:group ...`, `sudo chmod -R u+rw ...`). |
| **Configuración Rutas**      | (Opcional) Cambiar la ruta base de almacenamiento si es necesario.                                           | Buscar y modificar `STORAGE_PATH` en `msad/config/` o `msad/core/`. Recordar ajustar permisos.                          |

---

## ❓ Solución de Problemas

| Problema                                      | Causa Probable                                                                 | Solución                                                                                                                                |
| :-------------------------------------------- | :----------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| Error al generar reporte: "No hay datos"      | Rango de fechas/cliente incorrecto; No hay datos en BD.                          | Verificar parámetros API; Usar `POST /api/msad/test-data` (si existe y está accesible); Consultar BD.                                       |
| Error al generar reporte: "Error BD" / 500    | Problema acceso `sensor_data.db`; BD bloqueada; Ruta BD incorrecta.              | Verificar permisos `sensor_data.db`; Verificar ruta BD en MSAD; Revisar logs (`msad.log`, Flask).                                      |
| Error al descargar/listar/eliminar: 404       | Nombre archivo/ID incorrecto; Archivo no existe; Ruta almacenamiento errónea.  | Verificar nombre/ID; Listar de nuevo; Verificar `STORAGE_PATH` y permisos.                                                              |
| Error al crear backup: "Permission denied"    | Directorio `backups/` no existe o sin permisos de escritura.                   | Crear directorio `backups/` en `STORAGE_PATH`; Asignar permisos de escritura al usuario de Flask.                                       |
| Error al restaurar backup: "DB locked" / 500 | `sensor_data.db` en uso por otro proceso.                                      | Intentar detener servidor Flask antes de restaurar (si posible); Reintentar en baja actividad.                                           |
| Backups automáticos no se ejecutan          | `schedule` no instalado; Planificador deshabilitado; Error tarea; Proceso no corre. | Verificar `requirements.txt`; Habilitar scheduler (API/`init_msad`); Revisar `msad.log`; Asegurar que `app.py` corra persistentemente. |

*   **Logs:** Consultar `msad.log` (en `<RUTA_BASE>/msad/logs/`) para detalles específicos.

---

<div align="center">
    **MSAD** - Documentación Detallada v1.0.0 - Integrado en el Servidor
</div> 