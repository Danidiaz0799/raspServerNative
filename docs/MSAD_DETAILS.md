# 📊 MSAD - Detalles del Microservicio de Almacenamiento y Datos

<div align="center">

![Versión](https://img.shields.io/badge/Versión-1.0.0--minimal-blue)
![Integración](https://img.shields.io/badge/Integración-RaspServer-green)
![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)

</div>

## 📋 Índice

- [Descripción](#-descripción)
- [Arquitectura](#-arquitectura)
- [Funcionalidades](#-funcionalidades)
- [Integración con RaspServer](#-integración-con-raspserver)
- [Esquema de Almacenamiento](#-esquema-de-almacenamiento)
- [Flujo de Trabajo](#-flujo-de-trabajo)
- [Instalación y Configuración Específica](#-instalación-y-configuración-específica)
- [Solución de Problemas](#-solución-de-problemas)
- [Desarrollo Futuro](#-desarrollo-futuro)

## 📝 Descripción

MSAD es un **módulo integrado y optimizado** dentro de RaspServer, enfocado en la generación y gestión de backups y reportes. Permite extraer, filtrar y exportar datos críticos del cultivo de hongos (sensores, eventos, actuadores) para facilitar análisis detallados, toma de decisiones y asegurar la persistencia de los datos.

### ✨ Características Clave

| Característica | Descripción | Módulo Principal |
|----------------|-------------|------------------|
| 🚀 **Alta Performance** | Consultas optimizadas y bajo impacto en recursos del servidor | Core |
| 🔄 **Formatos Múltiples** | Exportación de reportes en JSON y CSV | Core (Reports) |
| 💾 **Backups Robustos** | Backups automáticos/manuales, restauración segura | Core (Backup) |
| ⏰ **Programación** | Configuración de intervalo para backups automáticos | Core (Backup) / `schedule` |
| 🔍 **Filtrado Avanzado** | Selección por cliente, fechas, tipo de datos en reportes | Core (Reports) |
| 📂 **Gestión de Archivos** | Almacenamiento organizado y endpoints para listar/descargar/eliminar | API / Core |
| 🔗 **Integración Simple** | API RESTful integrada en RaspServer | API |

## 🏗 Arquitectura

MSAD sigue una arquitectura modular dentro de la aplicación Flask principal:

```
                    ┌───────────────────┐
                    │                   │
                    │   Flask Server    │
                    │   (app.py)        │  <-- Inicializa MSAD
                    │                   │      Registra Blueprints MSAD
                    └─────────┬─────────┘
                              │ (Llamadas API)
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
│                                      │(Acceso DB)   │
└──────────────────────────────────────┼──────────────┘
                                       ▼
                             ┌──────────────────┐
                             │  Base de Datos   │
                             │   (SQLite -      │
                             │ sensor_data.db)  │
                             └──────────────────┘
```

*   **`app.py`**: Actúa como orquestador, inicializando MSAD (`msad/__init__.py`) y registrando sus blueprints API.
*   **`msad/api/`**: Contiene los blueprints de Flask que definen los endpoints RESTful para interactuar con las funcionalidades de MSAD (backups, reportes, estado).
*   **`msad/core/`**: Implementa la lógica de negocio principal:
    *   `backup.py`: Funciones para crear, listar, restaurar, eliminar backups y gestionar el planificador (`schedule`).
    *   `reports.py`: Funciones para consultar la base de datos, filtrar datos y generar archivos de reporte (JSON/CSV).
    *   `system.py`: Funciones de utilidad, configuración de logging, gestión de rutas de almacenamiento.
*   **Base de Datos**: MSAD accede directamente al archivo `sensor_data.db` utilizado por el resto de RaspServer.

### 📁 Estructura de Código

```
msad/
├── __init__.py           # Inicialización del módulo, registro de blueprints
├── api/
│   ├── __init__.py
│   ├── backup_routes.py  # Endpoints para backups
│   ├── report_routes.py  # Endpoints para reportes
│   └── system_routes.py  # Endpoint de estado
├── config/               # Configuración (ej. rutas base, logging)
│   ├── __init__.py
│   ├── app_settings.py
│   └── config_exports.py
└── core/
    ├── __init__.py
    ├── backup.py         # Lógica de backups y scheduling
    ├── core_exports.py   # (Podría ser obsoleto o para simplificar imports)
    ├── reports.py        # Lógica de generación de reportes
    └── system.py         # Lógica de sistema (paths, logging, DB access helpers)
```

## 🎯 Funcionalidades Detalladas

### 📊 Gestión de Reportes

*   **Generación bajo demanda**: Crea reportes históricos a través de la API.
*   **Filtrado Múltiple**: Combina filtros por `client_id`, `start_date`, `end_date`, `data_type` (`sensors`, `events`, `actuators`).
*   **Formatos Flexibles**: Exporta a `JSON` (ideal para integración con otras aplicaciones o visualizaciones) o `CSV` (para análisis en hojas de cálculo).
*   **Consulta de Datos**: Accede a las tablas `sht3x_data`, `events`, `actuator_log` (o las tablas relevantes existentes) de `sensor_data.db`.
*   **Gestión de Archivos**: Lista reportes existentes (globalmente o por cliente) y permite descargarlos o eliminarlos vía API.

### 💾 Gestión de Backups

*   **Backups Automáticos Programados**: Utiliza la librería `schedule` para ejecutar backups completos de `sensor_data.db` a intervalos regulares (configurables vía API o al inicio de `app.py`).
*   **Backups Manuales**: Permite disparar un backup inmediato a través de la API (`POST /api/msad/backups/create`).
*   **Listado y Descarga**: Ofrece endpoints API para listar todos los backups disponibles (con metadatos como fecha, tamaño, tipo) y descargar archivos `.db` individuales.
*   **Eliminación**: Permite eliminar archivos de backup específicos vía API para gestionar el espacio de almacenamiento.
*   **Restauración Segura**: Implementa un proceso de restauración (`POST /api/msad/backups/restore/<filename>`) que:
    1.  Crea un backup de seguridad de la base de datos *actual* antes de sobrescribirla.
    2.  Reemplaza `sensor_data.db` con el contenido del archivo de backup seleccionado.
    3.  **Nota:** Puede ser necesario reiniciar el servidor Flask (`app.py`) después de una restauración para que todos los componentes reconozcan la base de datos restaurada.
*   **Gestión del Planificador**: Permite consultar el estado del planificador de backups automáticos (si está activo, cuándo es la próxima ejecución) y configurarlo (activar/desactivar, cambiar intervalo) mediante la API (`GET` y `POST` a `/api/msad/backups/scheduler`).

## 🔌 Integración con RaspServer

La integración se realiza principalmente en `app.py`:

```python
# En app.py

# 1. Importar funciones de inicialización y blueprints de MSAD
from msad import (
    init_msad, shutdown_msad,
    create_system_blueprint, create_backup_blueprint, create_report_blueprint
)

# ... (Creación de la app Flask)

# 2. Registrar los Blueprints de MSAD
system_bp = create_system_blueprint()
backup_bp = create_backup_blueprint()
report_bp = create_report_blueprint()

app.register_blueprint(system_bp, url_prefix='/api')
app.register_blueprint(backup_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')

# 3. Inicializar MSAD al arrancar la aplicación
#    (Opcional: habilitar backups automáticos y definir intervalo)
msad_status = init_msad(auto_backup=True, backup_interval_hours=24)
print(f"Estado inicial de MSAD: {msad_status['message']}")

# 4. Registrar la función de apagado de MSAD para que se ejecute al salir
import atexit
# ... (dentro de la función on_exit registrada con atexit)
# shutdown_msad()

```

El acceso a la base de datos se centraliza a través de funciones helper (posiblemente en `msad/core/system.py` o directamente usando `aiosqlite` o `sqlite3`) que apuntan al archivo `sensor_data.db` principal.

## 📂 Esquema de Almacenamiento

MSAD organiza los archivos generados (reportes y backups) y sus logs en una estructura de directorios configurable. La configuración por defecto o recomendada es:

**En producción (Linux/Raspberry Pi):**

```
/mnt/storage/msad/  (o una ruta configurable, ej. dentro del dir del proyecto)
├── backups/
│   ├── sensor_data_auto_YYYYMMDD_HHMMSS.db
│   ├── sensor_data_manual_YYYYMMDD_HHMMSS.db
│   └── ...
├── reports/
│   ├── <client_id_1>/
│   │   ├── <client_id_1>_sensors_<start>_to_<end>_<timestamp>.json
│   │   └── <client_id_1>_events_<start>_to_<end>_<timestamp>.csv
│   ├── <client_id_2>/
│   │   └── ...
│   └── ...
└── logs/
    └── msad.log
```
*   **`/mnt/storage/msad/`**: Es un ejemplo de ruta base. Podría estar en otro lugar, como `/var/lib/raspserver/msad` o incluso dentro del directorio del proyecto si el volumen de datos no es muy grande. **Es crucial asegurarse de que esta ruta exista y tenga permisos de escritura para el usuario que ejecuta `app.py`.** La ruta se configura probablemente en `msad/config/app_settings.py`.
*   `backups/`: Almacena todos los archivos `.db` de backup.
*   `reports/`: Contiene subdirectorios por `client_id`, donde se guardan los reportes generados para cada cliente.
*   `logs/`: Guarda el archivo de log específico de MSAD.

**En desarrollo (Windows):** Puede usar una ruta relativa dentro del proyecto, como `storage/msad/...`.

## 🔄 Flujo de Trabajo

### 📊 Generación y Consulta de Reportes

```mermaid
graph LR
    A[Cliente API] --> B(POST /api/clients/.../reports \n {filtros});
    B --> C{MSAD Core: \n reports.py};
    C --> D[Consulta sensor_data.db];
    D --> C;
    C --> E{Genera Archivo \n (JSON/CSV)};
    E --> F[Almacena en /reports/...];
    F --> C;
    C --> B;
    B --> A[Respuesta JSON: \n {success: true, filename: ..., download_url: ...}];

    A2[Cliente API] --> G(GET /api/.../reports);
    G --> H{MSAD Core: \n reports.py};
    H --> I[Lee dir /reports/...];
    I --> H;
    H --> G;
    G --> A2[Respuesta JSON: \n Lista de reportes];

    A3[Cliente API] --> J(GET /api/.../download/filename.ext);
    J --> K{MSAD Core: \n reports.py};
    K --> L[Busca archivo en /reports/...];
    L --> K;
    K --> J;
    J --> A3[Respuesta: \n Archivo binario];
```

### 💾 Proceso de Backup y Restauración

```mermaid
graph LR
    subgraph Configuración y Backups Automáticos
        P[Planificador (schedule)] -- cada X horas --> BA(MSAD Core: backup.py \n create_backup(manual=False));
        BA --> DB[(sensor_data.db)];
        BA --> FS[Almacena en /backups/...];
    end

    subgraph Operaciones Manuales API
        A[Cliente API] --> B(POST /api/msad/backups/create);
        B --> C(MSAD Core: backup.py \n create_backup(manual=True));
        C --> DB;
        C --> FS;
        C --> B;
        B --> A[Respuesta JSON: {success: true, filename: ...}];

        A2[Cliente API] --> D(GET /api/msad/backups);
        D --> E(MSAD Core: backup.py \n list_backups);
        E --> FS;
        E --> D;
        D --> A2[Respuesta JSON: Lista de backups];

        A3[Cliente API] --> F(POST /api/msad/backups/restore/file.db);
        F --> G(MSAD Core: backup.py \n restore_backup);
        G -- 1. Backup Seguridad --> FS;
        G -- 2. Lee Backup a Restaurar --> FS;
        G -- 3. Sobrescribe --> DB;
        G --> F;
        F --> A3[Respuesta JSON: {success: true, safety_backup: ...}];
    end
```

## ⚙️ Instalación y Configuración Específica

MSAD está integrado en RaspServer, por lo que su instalación principal se realiza junto con las dependencias generales del proyecto. Sin embargo, hay puntos específicos a considerar:

### Dependencias
*   Asegúrate de que `schedule` esté incluido en tu `requirements.txt` si planeas usar los backups automáticos.
    ```
    # requirements.txt debe incluir:
    flask>=2.0.0
    aiosqlite>=0.17.0
    paho-mqtt>=1.5.0
    schedule>=1.1.0
    numpy>=1.20.0
    # ... otras dependencias de Flask/RaspServer
    ```
*   Instala con `pip install -r requirements.txt`. 

### Activación de Backups Automáticos
*   Puedes habilitar los backups automáticos al iniciar la aplicación Flask modificando la llamada a `init_msad` en `app.py`:
    ```python
    # En app.py, al inicializar MSAD:
    msad_status = init_msad(auto_backup=True, backup_interval_hours=24)
    ```
*   Alternativamente, puedes gestionar la activación y el intervalo a través de la API (`POST /api/msad/backups/scheduler`).

### Permisos de Directorios
*   El paso más crítico es asegurarse de que el **directorio de almacenamiento de MSAD** (donde irán las carpetas `backups/`, `reports/`, `logs/`) **exista y tenga permisos de escritura** para el usuario que ejecuta el proceso de Flask (`app.py`).
*   Verifica la ruta configurada (probablemente en `msad/config/app_settings.py` o `msad/core/system.py`). Si la ruta es, por ejemplo, `/mnt/storage/msad`:
    ```bash
    # En sistemas Linux/Raspberry Pi (ejecutar como root o con sudo)
    sudo mkdir -p /mnt/storage/msad/backups
    sudo mkdir -p /mnt/storage/msad/reports
    sudo mkdir -p /mnt/storage/msad/logs
    # Cambia [usuario] por el nombre de usuario que ejecuta Flask (ej. 'pi')
    sudo chown -R [usuario]:[usuario] /mnt/storage/msad 
    sudo chmod -R u+rw /mnt/storage/msad
    ```

### Configuración de Rutas (Opcional)
*   Si necesitas cambiar la ruta base de almacenamiento de MSAD (por defecto `/mnt/storage/msad` o similar), busca la definición de `STORAGE_PATH` o similar en `msad/config/app_settings.py` o `msad/core/system.py` y ajústala según tus necesidades. Recuerda crear el directorio y asignar permisos después de cambiar la ruta.

## ❓ Solución de Problemas

Errores específicos de MSAD pueden surgir por varias razones:

<table>
<tr>
<th>Problema</th>
<th>Causa Probable</th>
<th>Solución</th>
</tr>
<tr>
<td>Error al generar reporte: "No se encontraron datos..."</td>
<td>- Rango de fechas incorrecto.<br>- `client_id` incorrecto.<br>- No hay datos para ese tipo/periodo en la BD.</td>
<td>- Verifica parámetros API (fechas, cliente, tipo).<br>- Usa `POST /api/msad/test-data` para generar datos de prueba.<br>- Consulta la BD directamente para verificar existencia de datos.</td>
</tr>
<tr>
<td>Error al generar reporte: "Error al consultar la base de datos" / Error 500</td>
<td>- Problema de acceso a `sensor_data.db`.<br>- Base de datos bloqueada.<br>- Ruta a la BD incorrecta en la config de MSAD.</td>
<td>- Verifica permisos de `sensor_data.db`.<br>- Asegúrate que la ruta a la BD configurada en MSAD (`get_database_path()` en `system.py`) sea correcta.<br>- Revisa logs (`msad.log` y logs de Flask) para detalles del error SQL.</td>
</tr>
<tr>
<td>Error al descargar/listar/eliminar reportes/backups: "Archivo no encontrado" / Error 404</td>
<td>- Nombre de archivo o `report_id` incorrecto.<br>- Archivo eliminado previamente.<br>- Ruta de almacenamiento (`STORAGE_PATH`) incorrecta o inaccesible.</td>
<td>- Verifica el `filename` o `report_id` exacto (sensible a mayúsculas/minúsculas).<br>- Lista los archivos de nuevo para confirmar existencia.<br>- Verifica que `STORAGE_PATH` exista y tenga permisos de lectura/escritura.</td>
</tr>
<tr>
<td>Error al crear backup: "Permission denied" / Error 500</td>
<td>- El directorio de backups no existe.<br>- Permisos de escritura insuficientes en el directorio de backups.</td>
<td>- Crea el directorio `backups/` dentro de `STORAGE_PATH`.<br>- Asegúrate de que el usuario que ejecuta Flask tenga permisos de escritura en ese directorio (ver sección de Instalación).</td>
</tr>
<tr>
<td>Error al restaurar backup: "Database is locked" / Error 500</td>
<td>- La base de datos `sensor_data.db` está siendo utilizada activamente por otro proceso (Flask, MQTT client, etc.).</td>
<td>- Intenta detener el servidor Flask (`app.py`) antes de ejecutar la restauración vía API (si es posible).<br>- Si no es posible detenerlo, el error puede ser intermitente; reintentar puede funcionar. Considera hacer restauraciones en momentos de baja actividad.</td>
</tr>
<tr>
<td>Backups automáticos no se ejecutan</td>
<td>- `schedule` no instalado.<br>- Planificador no habilitado (`auto_backup=False` en `init_msad` o deshabilitado vía API).<br>- Error en la ejecución de la tarea programada (ver `msad.log`).<br>- El proceso principal de Flask (`app.py`) no se mantiene corriendo.</td>
<td>- Verifica `requirements.txt` y reinstala si es necesario.<br>- Habilita el scheduler vía API o en `init_msad`.<br>- Revisa `msad.log` por errores durante la ejecución del backup programado.<br>- Asegúrate que `app.py` corra de forma persistente (ej. con `systemd`).</td>
</tr>
</table>

*   **Logs:** Revisa el archivo `msad.log` (ubicado en `STORAGE_PATH/logs/`) para mensajes de error detallados específicos de MSAD.

## 🔮 Desarrollo Futuro

### Posibles Mejoras Futuras

- **Exportación a más formatos**: Añadir soporte para PDF o XLSX en reportes.
- **Análisis estadístico incorporado**: Calcular y añadir estadísticas básicas (min, max, avg) directamente en los reportes generados.
- **Reportes programados**: Permitir configurar la generación automática y periódica de ciertos reportes.
- **Notificaciones**: Implementar notificaciones (ej. email, webhook) al completarse la generación de reportes extensos o al fallar un backup.
- **Compresión**: Añadir opción para comprimir (.zip, .gz) los archivos de reporte o backup generados, especialmente los grandes.
- **Visualizaciones**: Integrar la generación de gráficos básicos (ej. usando Matplotlib o Plotly) como imágenes o HTML junto con los reportes de datos.
- **Interfaz de Usuario**: Crear vistas en el frontend Angular para interactuar con las funcionalidades de MSAD (listar/descargar/generar reportes, gestionar backups).

### Extensión de Código Ejemplo

Para añadir un nuevo tipo de reporte (ej. estadísticas):

1.  **En `msad/core/reports.py`:**
    ```python
    import numpy as np # Necesitarás numpy
    # ... otras importaciones

    def generate_statistics_report(client_id, start_date, end_date, format="json"):
        """Genera un reporte de estadísticas (min, max, avg) para sensores."""
        conn = None
        try:
            db_path = get_database_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = """
                SELECT temperature, humidity FROM sht3x_data
                WHERE client_id = ? AND timestamp >= ? AND timestamp <= ?
            """
            # Ajustar las fechas para incluir el día final completo
            end_date_inclusive = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() + datetime.timedelta(days=1)
            end_date_str = end_date_inclusive.strftime('%Y-%m-%d')

            cursor.execute(query, (client_id, start_date, end_date_str))
            rows = cursor.fetchall()

            if not rows:
                return None # No data found

            temps = [row[0] for row in rows if row[0] is not None]
            humids = [row[1] for row in rows if row[1] is not None]

            stats = {
                'client_id': client_id,
                'period': {'start': start_date, 'end': end_date},
                'record_count': len(rows),
                'temperature': {
                    'min': round(float(np.min(temps)), 2) if temps else None,
                    'max': round(float(np.max(temps)), 2) if temps else None,
                    'avg': round(float(np.mean(temps)), 2) if temps else None,
                },
                'humidity': {
                    'min': round(float(np.min(humids)), 2) if humids else None,
                    'max': round(float(np.max(humids)), 2) if humids else None,
                    'avg': round(float(np.mean(humids)), 2) if humids else None,
                }
            }

            # Aquí generarías el archivo JSON/CSV basado en 'stats'
            # ... (lógica de escritura de archivo similar a otros reportes)
            # Retornar metadatos del archivo generado
            # return report_metadata
            return stats # Por ahora devolvemos los datos para el ejemplo

        except Exception as e:
            logger.error(f"Error generating statistics report: {e}")
            raise # Re-lanzar para manejo en la API
        finally:
            if conn:
                conn.close()
    ```

2.  **En `msad/api/report_routes.py` (o un nuevo `statistics_routes.py`):**
    ```python
    # ... importaciones ...
    from msad.core.reports import generate_statistics_report

    # Asumiendo que lo añades a report_bp
    @report_bp.route('/clients/<client_id>/msad/statistics', methods=['POST'])
    def create_statistics_report_endpoint(client_id):
        """Endpoint para generar un reporte de estadísticas."""
        data = request.json
        if not data or 'start_date' not in data or 'end_date' not in data:
            return jsonify({"success": False, "error": "start_date y end_date son requeridos"}), 400

        start_date = data['start_date']
        end_date = data['end_date']
        # format = data.get('format', 'json') # Si generas archivo

        try:
            # Aquí llamarías a la función que genera y guarda el archivo
            # report_metadata = generate_and_save_statistics_report(client_id, start_date, end_date, format)
            # Por ahora, solo obtenemos los datos:
            stats_data = generate_statistics_report(client_id, start_date, end_date)

            if stats_data:
                # Devolverías los metadatos del archivo si lo hubieras guardado
                # return jsonify({"success": True, **report_metadata})
                return jsonify({"success": True, "statistics": stats_data})
            else:
                return jsonify({"success": False, "error": "No se encontraron datos para estadísticas"}), 404

        except Exception as e:
            logger.error(f"Error en endpoint de estadísticas: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    ```

---

<div align="center">
    **MSAD** - Documentación Detallada v1.0.0 - Integrado en RaspServer
</div> 