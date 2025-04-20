"""
Funciones para generar y gestionar reportes
"""
import os
import json
import csv
import datetime
from msad.core.system import logger, STORAGE_PATH, execute_query

def generate_report(client_id, start_date, end_date, data_type="sensors", format="json"):
    """
    Generar un reporte de datos para un cliente en un rango de fechas
    
    Args:
        client_id: ID del cliente
        start_date: Fecha inicial (YYYY-MM-DD)
        end_date: Fecha final (YYYY-MM-DD)
        data_type: Tipo de datos (sensors, events, actuators)
        format: Formato de salida (json, csv)
    
    Returns:
        dict: Información del reporte generado
    """
    try:
        # Validar parámetros
        if not client_id or not start_date or not end_date:
            return {"success": False, "error": "Faltan parámetros requeridos"}
            
        # Validar tipo de datos
        valid_types = ["sensors", "events", "actuators"]
        if data_type not in valid_types:
            return {"success": False, "error": f"Tipo de datos no válido. Opciones: {', '.join(valid_types)}"}
            
        # Validar formato
        valid_formats = ["json", "csv"]
        if format not in valid_formats:
            return {"success": False, "error": f"Formato no válido. Opciones: {', '.join(valid_formats)}"}
        
        # Convertir fechas
        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        except ValueError:
            return {"success": False, "error": "Formato de fecha incorrecto. Use YYYY-MM-DD"}
            
        # Verificar orden de fechas
        if start_dt > end_dt:
            return {"success": False, "error": "La fecha inicial no puede ser posterior a la fecha final"}
            
        # Mapear tipo de datos a tabla de base de datos
        tables = {
            "sensors": "sht3x_data",
            "events": "events",
            "actuators": "actuator_actions"
        }
        table = tables[data_type]
        
        # Consultar datos
        start_timestamp = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_timestamp = end_dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Primero verificar si hay datos para este cliente en general
        check_query = f"SELECT COUNT(*) as count FROM {table} WHERE client_id = ?"
        check_result = execute_query(check_query, (client_id,))
        
        if check_result and check_result[0]['count'] == 0:
            logger.warning(f"No se encontraron datos para el cliente {client_id} en la tabla {table}")
            return {"success": False, "error": f"No hay datos registrados para el cliente {client_id}"}
        else:
            logger.info(f"Se encontraron {check_result[0]['count']} registros en total para el cliente {client_id}")
        
        query = f"""
        SELECT * FROM {table}
        WHERE client_id = ? AND timestamp >= ? AND timestamp <= ?
        ORDER BY timestamp DESC
        """
        
        logger.info(f"Consultando datos para el cliente {client_id} en el rango {start_date} a {end_date}")
        data = execute_query(query, (client_id, start_timestamp, end_timestamp))
        
        if data is None:
            logger.error(f"Error al ejecutar la consulta en la tabla {table}")
            return {"success": False, "error": "Error al consultar la base de datos"}
            
        if not data:
            logger.info(f"No se encontraron datos para el cliente {client_id} en el rango especificado")
            return {"success": False, "error": "No se encontraron datos para el rango especificado"}
        
        # Generar nombre de archivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        period = f"{start_date}_to_{end_date}"
        filename = f"{client_id}_{data_type}_{period}_{timestamp}.{format}"
        
        # Asegurar que existe el directorio de reportes para el cliente
        client_dir = os.path.join(STORAGE_PATH, "reports", client_id)
        os.makedirs(client_dir, exist_ok=True)
        
        file_path = os.path.join(client_dir, filename)
        
        # Convertir timestamps a fechas legibles en los datos
        for row in data:
            if 'timestamp' in row:
                # El timestamp ahora es un string, no necesitamos fromtimestamp
                # Simplemente lo dejamos como está, ya está en formato legible
                # row['timestamp'] = datetime.datetime.fromtimestamp(row['timestamp']).isoformat()
                pass  # Mantenemos el timestamp como está (ya es un string con formato)
        
        # Guardar archivo según formato
        if format == "json":
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format == "csv":
            if data:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        
        # Devolver información del reporte
        file_size = os.path.getsize(file_path)
        
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
        logger.error(f"Error al generar reporte: {str(e)}")
        return {"success": False, "error": str(e)}

def list_reports(client_id=None, format=None, data_type=None):
    """
    Listar los reportes disponibles
    
    Args:
        client_id: Opcional, filtrar por cliente específico
        format: Opcional, filtrar por formato (json, csv)
        data_type: Opcional, filtrar por tipo de datos (sensors, events, actuators)
    
    Returns:
        dict: Lista de reportes
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
            # Verificar que existe el directorio para ese cliente
            if not os.path.exists(os.path.join(reports_base, client_id)):
                return {"success": True, "reports": [], "total": 0}
        else:
            # Listar todos los clientes
            client_dirs = [d for d in os.listdir(reports_base) 
                          if os.path.isdir(os.path.join(reports_base, d))]
        
        # Recorrer directorios de clientes
        for client in client_dirs:
            client_dir = os.path.join(reports_base, client)
            
            for filename in os.listdir(client_dir):
                # Solo procesar archivos, no directorios
                file_path = os.path.join(client_dir, filename)
                if not os.path.isfile(file_path):
                    continue
                
                # Extraer información del nombre del archivo
                # Formato esperado: client_datatype_startdate_to_enddate_timestamp.format
                parts = filename.split('_')
                if len(parts) < 5:  # Verificar formato mínimo
                    continue
                    
                file_extension = filename.split('.')[-1]
                
                # Filtrar por formato si se especificó
                if format and file_extension != format:
                    continue
                
                # Extraer tipo de datos del nombre
                file_data_type = parts[1] if len(parts) > 1 else None
                
                # Filtrar por tipo de datos si se especificó
                if data_type and file_data_type != data_type:
                    continue
                
                # Obtener información del archivo
                stat = os.stat(file_path)
                created = datetime.datetime.fromtimestamp(stat.st_ctime)
                
                # Extraer timestamp del nombre (asumiendo que está al final antes de la extensión)
                timestamp_part = parts[-1].split('.')[0]
                
                # Crear objeto de reporte
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
        
        # Ordenar por fecha de creación (más reciente primero)
        reports.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "success": True,
            "reports": reports,
            "total": len(reports)
        }
        
    except Exception as e:
        logger.error(f"Error al listar reportes: {str(e)}")
        return {"success": False, "error": str(e)}

def get_report_file(client_id, filename_or_id):
    """
    Obtener la ruta de un archivo de reporte
    
    Args:
        client_id: ID del cliente
        filename_or_id: Nombre del archivo o report_id
    
    Returns:
        str: Ruta al archivo o None si no existe
    """
    try:
        # Comprobar si es un filename completo o un report_id
        if filename_or_id.startswith('report_'):
            # Es un report_id, buscar por timestamp
            report_timestamp = filename_or_id.replace('report_', '')
            
            client_dir = os.path.join(STORAGE_PATH, "reports", client_id)
            if not os.path.exists(client_dir):
                logger.warning(f"Directorio del cliente no encontrado: {client_dir}")
                return None
                
            # Buscar todos los archivos que contienen ese timestamp
            for filename in os.listdir(client_dir):
                if os.path.isfile(os.path.join(client_dir, filename)):
                    # Verificar si el timestamp está en el nombre del archivo
                    parts = filename.split('_')
                    if len(parts) >= 5:
                        # El timestamp suele ser la última parte antes de la extensión
                        file_timestamp = parts[-1].split('.')[0]
                        if file_timestamp == report_timestamp:
                            logger.info(f"Archivo encontrado por report_id {filename_or_id}: {filename}")
                            return os.path.join(client_dir, filename)
            
            logger.warning(f"No se encontró archivo con report_id {filename_or_id}")
            return None
        else:
            # Es un nombre de archivo completo
            file_path = os.path.join(STORAGE_PATH, "reports", client_id, filename_or_id)
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
            
            logger.warning(f"Archivo no encontrado: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error al obtener archivo de reporte: {str(e)}")
        return None 