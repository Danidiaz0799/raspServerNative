"""
Funciones para generar y gestionar reportes
"""
import os
import json
import csv
import datetime
from msad.core.system import logger, STORAGE_PATH, execute_query
import threading
import schedule

# --- Configuración global para el programador de reportes ---
REPORT_SCHEDULER_THREAD = None
REPORT_SCHEDULER_RUNNING = False
REPORT_SCHEDULER_CONFIG = {
    'interval_hours': 24,
    'client_id': None,
    'start_date': None,
    'end_date': None,
    'data_type': 'sensors',
    'format': 'json',
}
REPORT_SCHEDULER_LAST_RUN = None
REPORT_SCHEDULER_NEXT_RUN = None

def generate_report(client_id, start_date, end_date, data_type="sensors", format="json"):
    """
    Genera un reporte de datos para un cliente en un rango de fechas.
    Valida todos los parámetros y asegura robustez ante errores y datos faltantes.
    """
    try:
        # Validación robusta de parámetros
        if not client_id or not isinstance(client_id, str):
            return {"success": False, "error": "client_id es requerido y debe ser string"}
        if not start_date or not isinstance(start_date, str):
            return {"success": False, "error": "start_date es requerido y debe ser string (YYYY-MM-DD)"}
        if not end_date or not isinstance(end_date, str):
            return {"success": False, "error": "end_date es requerido y debe ser string (YYYY-MM-DD)"}

        # Validar tipo de datos
        valid_types = ["sensors", "events", "actuators"]
        if data_type not in valid_types:
            return {"success": False, "error": f"Tipo de datos no válido. Opciones: {', '.join(valid_types)}"}

        # Validar formato
        valid_formats = ["json", "csv"]
        if format not in valid_formats:
            return {"success": False, "error": f"Formato no válido. Opciones: {', '.join(valid_formats)}"}

        # Validar fechas
        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        except Exception:
            return {"success": False, "error": "Formato de fecha incorrecto. Use YYYY-MM-DD"}
        if start_dt > end_dt:
            return {"success": False, "error": "La fecha inicial no puede ser posterior a la fecha final"}

        # Mapear tipo de datos a tabla de base de datos
        tables = {
            "sensors": "sht3x_data",
            "events": "events",
            "actuators": "actuator_actions"
        }
        table = tables[data_type]

        # Verificar existencia de datos para el cliente
        check_query = f"SELECT COUNT(*) as count FROM {table} WHERE client_id = ?"
        try:
            check_result = execute_query(check_query, (client_id,))
        except Exception as e:
            logger.error(f"Error al consultar la base de datos: {e}")
            return {"success": False, "error": "Error al consultar la base de datos"}
        if not check_result or check_result[0]['count'] == 0:
            logger.warning(f"No se encontraron datos para el cliente {client_id} en la tabla {table}")
            return {"success": False, "error": f"No hay datos registrados para el cliente {client_id}"}
        logger.info(f"Se encontraron {check_result[0]['count']} registros en total para el cliente {client_id}")

        # Consultar datos para el rango
        start_timestamp = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_timestamp = end_dt.strftime("%Y-%m-%d %H:%M:%S")
        query = f"SELECT * FROM {table} WHERE client_id = ? AND timestamp >= ? AND timestamp <= ? ORDER BY timestamp DESC"
        try:
            data = execute_query(query, (client_id, start_timestamp, end_timestamp))
        except Exception as e:
            logger.error(f"Error al consultar datos: {e}")
            return {"success": False, "error": "Error al consultar la base de datos"}
        if data is None:
            return {"success": False, "error": "Error al consultar la base de datos"}
        if not data:
            logger.info(f"No se encontraron datos para el cliente {client_id} en el rango especificado")
            return {"success": False, "error": "No se encontraron datos para el rango especificado"}

        # Generar nombre de archivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        period = f"{start_date}_to_{end_date}"
        filename = f"{client_id}_{data_type}_{period}_{timestamp}.{format}"
        client_dir = os.path.join(STORAGE_PATH, "reports", client_id)
        try:
            os.makedirs(client_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"No se pudo crear el directorio de reportes: {e}")
            return {"success": False, "error": "No se pudo crear el directorio para reportes"}
        file_path = os.path.join(client_dir, filename)

        # Guardar archivo según formato
        try:
            if format == "json":
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            elif format == "csv":
                if data:
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
        except Exception as e:
            logger.error(f"No se pudo guardar el archivo de reporte: {e}")
            return {"success": False, "error": "No se pudo guardar el archivo de reporte"}

        # Devolver información del reporte
        try:
            file_size = os.path.getsize(file_path)
        except Exception:
            file_size = None
        logger.info(f"Reporte generado: {file_path} ({file_size} bytes, {len(data)} registros)")
        return {
            "success": True,
            "report_id": f"report_{timestamp}",
            "client_id": client_id,
            "data_type": data_type,
            "filename": filename,
            "format": format,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "records": len(data),
            "size": file_size,
            "created_at": datetime.datetime.now().isoformat(),
            "download_url": f"/api/clients/{client_id}/msad/reports/download/{filename}"
        }
    except Exception as e:
        logger.error(f"Error inesperado al generar reporte: {str(e)}")
        return {"success": False, "error": str(e)}

def list_reports(client_id=None, format=None, data_type=None):
    """
    Lista los reportes disponibles, robusto ante errores y directorios faltantes.
    """
    try:
        reports = []
        reports_base = os.path.join(STORAGE_PATH, "reports")
        
        # Si no existe el directorio, devolver lista vacía
        if not os.path.exists(reports_base):
            return {"success": True, "reports": [], "total": 0}
        
        # Filtrar por cliente
        if client_id:
            client_dirs = [client_id]
            if not os.path.exists(os.path.join(reports_base, client_id)):
                return {"success": True, "reports": [], "total": 0}
        else:
            try:
                client_dirs = [d for d in os.listdir(reports_base)
                               if os.path.isdir(os.path.join(reports_base, d))]
            except Exception as e:
                logger.error(f"No se pudo listar clientes en reports: {e}")
                return {"success": False, "error": "No se pudo acceder al directorio de reportes"}
        reports = []
        for client in client_dirs:
            client_dir = os.path.join(reports_base, client)
            try:
                filenames = os.listdir(client_dir)
            except Exception:
                continue
            for filename in filenames:
                file_path = os.path.join(client_dir, filename)
                if not os.path.isfile(file_path):
                    continue
                parts = filename.split('_')
                if len(parts) < 5:
                    continue
                file_extension = filename.split('.')[-1]
                if format and file_extension != format:
                    continue
                file_data_type = parts[1] if len(parts) > 1 else None
                if data_type and file_data_type != data_type:
                    continue
                try:
                    stat = os.stat(file_path)
                    created = datetime.datetime.fromtimestamp(stat.st_ctime)
                except Exception:
                    continue
                timestamp_part = parts[-1].split('.')[0]
                report = {
                    "report_id": f"report_{timestamp_part}",
                    "client_id": client,
                    "data_type": file_data_type,
                    "filename": filename,
                    "format": file_extension,
                    "size": stat.st_size,
                    "created_at": created.isoformat(),
                    "download_url": f"/api/clients/{client}/msad/reports/download/{filename}"
                }
                reports.append(report)
        reports.sort(key=lambda x: x["created_at"], reverse=True)
        return {
            "success": True,
            "reports": reports,
            "total": len(reports)
        }
    except Exception as e:
        logger.error(f"Error al listar reportes: {str(e)}")
        return {"success": False, "error": str(e)}

# --- Scheduler Functions ---
def start_report_scheduler(config=None):
    """
    Inicia o reinicia el programador de reportes automáticos con la configuración dada.
    config: dict con las llaves 'interval_hours', 'client_id', 'start_date', 'end_date', 'data_type', 'format'
    """
    global REPORT_SCHEDULER_THREAD, REPORT_SCHEDULER_RUNNING, REPORT_SCHEDULER_CONFIG, REPORT_SCHEDULER_LAST_RUN, REPORT_SCHEDULER_NEXT_RUN
    import datetime
    import time
    stop_report_scheduler()  # Detener cualquier scheduler previo
    schedule.clear('report')
    if config:
        REPORT_SCHEDULER_CONFIG.update(config)
    interval = REPORT_SCHEDULER_CONFIG.get('interval_hours', 24)
    if not interval or interval <= 0:
        interval = 24
        REPORT_SCHEDULER_CONFIG['interval_hours'] = 24
    def report_job():
        global REPORT_SCHEDULER_LAST_RUN
        logger.info(f"[Scheduler] Generando reporte automático con configuración: {REPORT_SCHEDULER_CONFIG}")
        try:
            res = generate_report(
                REPORT_SCHEDULER_CONFIG['client_id'],
                REPORT_SCHEDULER_CONFIG['start_date'],
                REPORT_SCHEDULER_CONFIG['end_date'],
                REPORT_SCHEDULER_CONFIG['data_type'],
                REPORT_SCHEDULER_CONFIG['format']
            )
            if res.get('success'):
                logger.info(f"[Scheduler] Reporte generado correctamente: {res.get('filename')}")
            else:
                logger.warning(f"[Scheduler] Error al generar reporte: {res.get('error')}")
        except Exception as e:
            logger.error(f"[Scheduler] Excepción al generar reporte: {str(e)}")
        REPORT_SCHEDULER_LAST_RUN = datetime.datetime.now().isoformat()
        # Calcular próxima ejecución
        global REPORT_SCHEDULER_NEXT_RUN
        REPORT_SCHEDULER_NEXT_RUN = (datetime.datetime.now() + datetime.timedelta(hours=interval)).isoformat()
    schedule.every(interval).hours.do(report_job).tag('report')
    REPORT_SCHEDULER_NEXT_RUN = (datetime.datetime.now() + datetime.timedelta(hours=interval)).isoformat()
    def run_scheduler():
        global REPORT_SCHEDULER_RUNNING
        REPORT_SCHEDULER_RUNNING = True
        logger.info("[Scheduler] Iniciando programador de reportes")
        # La librería schedule estándar no soporta tags en run_pending; solo ejecuta todos los jobs pendientes.
        while REPORT_SCHEDULER_RUNNING:
            schedule.run_pending()
            time.sleep(60)
        logger.info("[Scheduler] Programador de reportes detenido")
    REPORT_SCHEDULER_THREAD = threading.Thread(target=run_scheduler, daemon=True)
    REPORT_SCHEDULER_THREAD.start()
    return True

def stop_report_scheduler():
    """Detiene el programador de reportes automáticos"""
    global REPORT_SCHEDULER_RUNNING, REPORT_SCHEDULER_THREAD
    if not REPORT_SCHEDULER_RUNNING:
        logger.warning("[Scheduler] El programador de reportes no está en ejecución")
        return True
    REPORT_SCHEDULER_RUNNING = False
    schedule.clear('report')
    if REPORT_SCHEDULER_THREAD and REPORT_SCHEDULER_THREAD.is_alive():
        REPORT_SCHEDULER_THREAD.join(timeout=5)
    logger.info("[Scheduler] Programador de reportes detenido")
    return True

def get_report_scheduler_status():
    """Obtiene el estado actual del programador de reportes"""
    global REPORT_SCHEDULER_RUNNING, REPORT_SCHEDULER_CONFIG, REPORT_SCHEDULER_LAST_RUN, REPORT_SCHEDULER_NEXT_RUN
    return {
        'success': True,
        'is_running': REPORT_SCHEDULER_RUNNING,
        'config': REPORT_SCHEDULER_CONFIG.copy(),
        'last_run': REPORT_SCHEDULER_LAST_RUN,
        'next_run': REPORT_SCHEDULER_NEXT_RUN,
    }

def get_report_file(client_id, filename_or_id):
    """
    Obtiene la ruta de un archivo de reporte por nombre o report_id. Robustez ante errores y casos no encontrados.
    """
    try:
        if not client_id or not filename_or_id:
            logger.error("client_id y filename_or_id son requeridos")
            return None
        client_dir = os.path.join(STORAGE_PATH, "reports", client_id)
        if not os.path.exists(client_dir):
            logger.warning(f"Directorio del cliente no encontrado: {client_dir}")
            return None
        # Buscar por report_id (timestamp) o filename
        if filename_or_id.startswith('report_'):
            report_timestamp = filename_or_id.replace('report_', '')
            for filename in os.listdir(client_dir):
                if os.path.isfile(os.path.join(client_dir, filename)):
                    parts = filename.split('_')
                    if len(parts) >= 5:
                        file_timestamp = parts[-1].split('.')[0]
                        if file_timestamp == report_timestamp:
                            logger.info(f"Archivo encontrado por report_id {filename_or_id}: {filename}")
                            return os.path.join(client_dir, filename)
            logger.warning(f"No se encontró archivo con report_id {filename_or_id}")
            return None
        else:
            file_path = os.path.join(client_dir, filename_or_id)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
            logger.warning(f"Archivo no encontrado: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error al obtener archivo de reporte: {str(e)}")
        return None