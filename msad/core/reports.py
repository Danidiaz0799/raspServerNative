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

# --- Configuración global para el programador de reportes por cliente ---
REPORT_SCHEDULERS = {}
# Estructura de cada entrada:
# {
#   'thread': threading.Thread,
#   'running': bool,
#   'config': dict,
#   'last_run': str,
#   'next_run': str
# }

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
import time
import datetime

def start_report_scheduler_for_client(client_id, config):
    """
    Inicia o reinicia el programador de reportes automáticos para un cliente específico.
    config: dict con las llaves 'interval_hours', 'start_date', 'end_date', 'data_type', 'format'
    """
    global REPORT_SCHEDULERS
    stop_report_scheduler_for_client(client_id)  # Detener cualquier scheduler previo para este cliente
    interval = config.get('interval_hours', 24)
    if not interval or interval <= 0:
        interval = 24
        config['interval_hours'] = 24
    def report_job():
        logger.info(f"[Scheduler:{client_id}] Generando reporte automático con configuración: {config}")
        try:
            res = generate_report(
                client_id,
                config['start_date'],
                config['end_date'],
                config.get('data_type', 'sensors'),
                config.get('format', 'json')
            )
            if res.get('success'):
                logger.info(f"[Scheduler:{client_id}] Reporte generado correctamente: {res.get('filename')}")
            else:
                logger.warning(f"[Scheduler:{client_id}] Error al generar reporte: {res.get('error')}")
        except Exception as e:
            logger.error(f"[Scheduler:{client_id}] Excepción al generar reporte: {str(e)}")
        REPORT_SCHEDULERS[client_id]['last_run'] = datetime.datetime.now().isoformat()
        REPORT_SCHEDULERS[client_id]['next_run'] = (datetime.datetime.now() + datetime.timedelta(hours=interval)).isoformat()
    # Programar el job
    job = schedule.every(interval).hours.do(report_job).tag(f'report_{client_id}')
    next_run = (datetime.datetime.now() + datetime.timedelta(hours=interval)).isoformat()
    def run_scheduler():
        REPORT_SCHEDULERS[client_id]['running'] = True
        logger.info(f"[Scheduler:{client_id}] Iniciando programador de reportes")
        while True:
            # Verifica que el scheduler siga registrado y activo
            if client_id not in REPORT_SCHEDULERS or not REPORT_SCHEDULERS[client_id]['running']:
                logger.info(f"[Scheduler:{client_id}] Scheduler eliminado o detenido, saliendo del hilo")
                break
            schedule.run_pending()
            time.sleep(60)
        logger.info(f"[Scheduler:{client_id}] Programador de reportes detenido")
    thread = threading.Thread(target=run_scheduler, daemon=True)
    REPORT_SCHEDULERS[client_id] = {
        'thread': thread,
        'running': True,
        'config': config.copy(),
        'last_run': None,
        'next_run': next_run
    }
    thread.start()
    return True

def stop_report_scheduler_for_client(client_id):
    """
    Detiene el programador de reportes automáticos para un cliente específico
    """
    global REPORT_SCHEDULERS
    if client_id not in REPORT_SCHEDULERS or not REPORT_SCHEDULERS[client_id]['running']:
        logger.warning(f"[Scheduler:{client_id}] El programador de reportes no está en ejecución")
        return True
    REPORT_SCHEDULERS[client_id]['running'] = False
    schedule.clear(f'report_{client_id}')
    thread = REPORT_SCHEDULERS[client_id]['thread']
    if thread and thread.is_alive():
        thread.join(timeout=5)
    logger.info(f"[Scheduler:{client_id}] Programador de reportes detenido")
    del REPORT_SCHEDULERS[client_id]
    return True

def get_report_scheduler_status_for_client(client_id):
    """
    Obtiene el estado actual del programador de reportes para un cliente específico
    """
    global REPORT_SCHEDULERS
    if client_id not in REPORT_SCHEDULERS:
        return {'success': False, 'error': 'No hay scheduler activo para este cliente'}
    sched = REPORT_SCHEDULERS[client_id]
    return {
        'success': True,
        'is_running': sched['running'],
        'config': sched['config'].copy(),
        'last_run': sched['last_run'],
        'next_run': sched['next_run'],
    }

def get_all_report_schedulers_status():
    """
    Devuelve el estado de todos los schedulers activos
    """
    global REPORT_SCHEDULERS
    status = {}
    for client_id, sched in REPORT_SCHEDULERS.items():
        status[client_id] = {
            'is_running': sched['running'],
            'config': sched['config'].copy(),
            'last_run': sched['last_run'],
            'next_run': sched['next_run'],
        }
    return {'success': True, 'schedulers': status}

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