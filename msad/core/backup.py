"""
Funciones para gestionar backups de la base de datos
"""
import os
import sys
import time
import shutil
import sqlite3
import datetime
import threading
import schedule
from pathlib import Path

from msad.core.system import logger, get_database_path, STORAGE_PATH

# Configuración global
BACKUP_DIR = os.path.join(STORAGE_PATH, "backups")
MAX_BACKUPS = 10  # Máximo número de backups a mantener
backup_thread = None
is_running = False

def init_backup_system():
    """
    Inicializa el sistema de backups
    """
    try:
        # Crear directorio de backups si no existe
        os.makedirs(BACKUP_DIR, exist_ok=True)
        logger.info(f"Sistema de backups inicializado en {BACKUP_DIR}")
        return True
    except Exception as e:
        logger.error(f"Error al inicializar sistema de backups: {str(e)}")
        return False

def create_backup(manual=False):
    """
    Crea un backup de la base de datos actual
    
    Args:
        manual: Si es True, el backup se considera manual
    
    Returns:
        dict: Información del backup creado
    """
    try:
        # Obtener ruta de la base de datos
        db_path = get_database_path()
        if not os.path.exists(db_path):
            logger.error(f"Base de datos no encontrada en {db_path}")
            return {
                "success": False,
                "error": f"Base de datos no encontrada en {db_path}"
            }
        
        # Generar nombre para el backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_type = "manual" if manual else "auto"
        backup_filename = f"sensor_data_{backup_type}_{timestamp}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Asegurar que el directorio existe
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Verificar integridad de la base de datos antes de hacer backup
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        integrity_check = cursor.fetchone()[0]
        conn.close()
        
        if integrity_check != "ok":
            logger.error(f"La base de datos falló la verificación de integridad: {integrity_check}")
            return {
                "success": False,
                "error": "La base de datos está corrupta y no se puede realizar el backup"
            }
        
        # Crear backup (copia del archivo)
        shutil.copy2(db_path, backup_path)
        
        # Verificar que el backup se creó correctamente
        if not os.path.exists(backup_path):
            logger.error("El archivo de backup no se creó correctamente")
            return {
                "success": False,
                "error": "Error al crear archivo de backup"
            }
        
        # Obtener tamaño del backup
        backup_size = os.path.getsize(backup_path)
        
        # Rotar backups si se supera el máximo
        rotate_backups()
        
        logger.info(f"Backup creado en {backup_path} ({backup_size} bytes)")
        
        return {
            "success": True,
            "backup_id": f"backup_{timestamp}",
            "filename": backup_filename,
            "path": backup_path,
            "size": backup_size,
            "type": backup_type,
            "created_at": datetime.datetime.now().isoformat(),
            "download_url": f"/api/msad/backups/download/{backup_filename}"
        }
        
    except Exception as e:
        logger.error(f"Error al crear backup: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def rotate_backups():
    """
    Elimina backups antiguos si se supera el número máximo
    """
    try:
        # Listar todos los backups
        backups = list_backups()
        
        # Si hay más backups de los permitidos, eliminar los más antiguos
        if len(backups["backups"]) > MAX_BACKUPS:
            # Ordenar por fecha (los más antiguos primero)
            backups_to_delete = sorted(
                backups["backups"], 
                key=lambda x: x["created_at"]
            )[:len(backups["backups"]) - MAX_BACKUPS]
            
            for backup in backups_to_delete:
                delete_backup(backup["filename"])
                logger.info(f"Backup rotado: {backup['filename']}")
                
        return True
    except Exception as e:
        logger.error(f"Error al rotar backups: {str(e)}")
        return False

def list_backups(backup_type=None):
    """
    Lista todos los backups disponibles
    
    Args:
        backup_type: Filtrar por tipo ("manual" o "auto")
    
    Returns:
        dict: Lista de backups
    """
    try:
        backups = []
        
        # Verificar que el directorio existe
        if not os.path.exists(BACKUP_DIR):
            return {"success": True, "backups": [], "total": 0}
        
        # Listar archivos de backup
        for filename in os.listdir(BACKUP_DIR):
            if not filename.startswith("sensor_data_") or not filename.endswith(".db"):
                continue
                
            # Extraer tipo de backup
            parts = filename.split("_")
            if len(parts) < 3:
                continue
                
            file_backup_type = parts[1]
            
            # Filtrar por tipo si se especificó
            if backup_type and file_backup_type != backup_type:
                continue
            
            # Obtener información del archivo
            file_path = os.path.join(BACKUP_DIR, filename)
            stat = os.stat(file_path)
            
            # Extraer timestamp del nombre
            timestamp_parts = filename.replace("sensor_data_", "").replace(".db", "").split("_")
            if len(timestamp_parts) < 2:
                timestamp = stat.st_ctime
            else:
                timestamp_str = "_".join(timestamp_parts[1:])
                try:
                    timestamp = datetime.datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S").timestamp()
                except ValueError:
                    timestamp = stat.st_ctime
            
            created_at = datetime.datetime.fromtimestamp(timestamp).isoformat()
            
            backup = {
                "backup_id": f"backup_{timestamp_parts[-1]}",
                "filename": filename,
                "type": file_backup_type,
                "size": stat.st_size,
                "created_at": created_at,
                "download_url": f"/api/msad/backups/download/{filename}"
            }
            
            backups.append(backup)
        
        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "success": True,
            "backups": backups,
            "total": len(backups)
        }
        
    except Exception as e:
        logger.error(f"Error al listar backups: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def delete_backup(filename):
    """
    Elimina un backup específico
    
    Args:
        filename: Nombre del archivo de backup
    
    Returns:
        dict: Resultado de la operación
    """
    try:
        if not filename.startswith("sensor_data_") or not filename.endswith(".db"):
            return {
                "success": False,
                "error": "Nombre de archivo inválido"
            }
            
        backup_path = os.path.join(BACKUP_DIR, filename)
        
        if not os.path.exists(backup_path):
            return {
                "success": False,
                "error": "Archivo de backup no encontrado"
            }
            
        os.remove(backup_path)
        
        logger.info(f"Backup eliminado: {backup_path}")
        
        return {
            "success": True,
            "message": f"Backup {filename} eliminado correctamente"
        }
        
    except Exception as e:
        logger.error(f"Error al eliminar backup: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def get_backup_file(filename):
    """
    Obtiene la ruta de un archivo de backup
    
    Args:
        filename: Nombre del archivo de backup
    
    Returns:
        str: Ruta al archivo o None si no existe
    """
    try:
        if not filename.startswith("sensor_data_") or not filename.endswith(".db"):
            return None
            
        backup_path = os.path.join(BACKUP_DIR, filename)
        
        if os.path.exists(backup_path) and os.path.isfile(backup_path):
            return backup_path
        
        return None
        
    except Exception as e:
        logger.error(f"Error al obtener archivo de backup: {str(e)}")
        return None

def restore_backup(filename):
    """
    Restaura un backup a la base de datos actual
    
    Args:
        filename: Nombre del archivo de backup
    
    Returns:
        dict: Resultado de la operación
    """
    try:
        # Validar nombre de archivo
        if not filename.startswith("sensor_data_") or not filename.endswith(".db"):
            return {
                "success": False,
                "error": "Nombre de archivo inválido"
            }
            
        # Verificar que el backup existe
        backup_path = os.path.join(BACKUP_DIR, filename)
        if not os.path.exists(backup_path):
            return {
                "success": False,
                "error": "Archivo de backup no encontrado"
            }
            
        # Obtener ruta de la base de datos
        db_path = get_database_path()
        
        # Crear backup de seguridad antes de restaurar
        safety_result = create_backup(manual=True)
        if not safety_result["success"]:
            logger.warning("No se pudo crear backup de seguridad antes de restaurar")
        
        # Restaurar (copiar el backup sobre la base de datos actual)
        shutil.copy2(backup_path, db_path)
        
        logger.info(f"Backup {filename} restaurado correctamente")
        
        return {
            "success": True,
            "message": f"Backup {filename} restaurado correctamente",
            "safety_backup": safety_result.get("filename") if safety_result.get("success") else None
        }
        
    except Exception as e:
        logger.error(f"Error al restaurar backup: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def start_backup_scheduler(interval_hours=24):
    """
    Inicia el programador de backups automáticos
    
    Args:
        interval_hours: Intervalo en horas entre backups
        
    Returns:
        bool: True si se inició correctamente, False en caso contrario
    """
    global backup_thread, is_running
    
    try:
        if is_running:
            logger.warning("El programador de backups ya está en ejecución")
            return True
            
        # Configurar programación
        schedule.clear()
        
        # Programar backup cada X horas
        if interval_hours <= 0:
            interval_hours = 24  # Valor por defecto
            
        schedule.every(interval_hours).hours.do(lambda: create_backup(manual=False))
        logger.info(f"Backups automáticos programados cada {interval_hours} horas")
        
        # Función para ejecutar el programador en un hilo separado
        def run_scheduler():
            global is_running
            is_running = True
            
            logger.info("Iniciando programador de backups")
            while is_running:
                schedule.run_pending()
                time.sleep(60)  # Verificar cada minuto
                
            logger.info("Programador de backups detenido")
        
        # Iniciar hilo
        backup_thread = threading.Thread(target=run_scheduler, daemon=True)
        backup_thread.start()
        
        return True
        
    except Exception as e:
        logger.error(f"Error al iniciar programador de backups: {str(e)}")
        is_running = False
        return False

def stop_backup_scheduler():
    """
    Detiene el programador de backups automáticos
    
    Returns:
        bool: True si se detuvo correctamente, False en caso contrario
    """
    global is_running
    
    try:
        if not is_running:
            logger.warning("El programador de backups no está en ejecución")
            return True
            
        # Detener programador
        is_running = False
        schedule.clear()
        
        # Esperar a que el hilo termine (con timeout)
        if backup_thread and backup_thread.is_alive():
            backup_thread.join(timeout=5)
            
        logger.info("Programador de backups detenido")
        return True
        
    except Exception as e:
        logger.error(f"Error al detener programador de backups: {str(e)}")
        return False

def get_backup_status():
    """
    Obtiene el estado actual del sistema de backups
    
    Returns:
        dict: Estado del sistema de backups
    """
    try:
        # Contar backups
        backup_count = len(list_backups()["backups"])
        
        # Espacio ocupado
        total_size = sum(os.path.getsize(os.path.join(BACKUP_DIR, f)) 
                         for f in os.listdir(BACKUP_DIR) 
                         if os.path.isfile(os.path.join(BACKUP_DIR, f)))
        
        # Formatear tamaño
        if total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.2f} KB"
        else:
            size_str = f"{total_size / (1024 * 1024):.2f} MB"
        
        last_backup = None
        next_backup = None
        
        # Obtener último backup
        backups = list_backups()
        if backups["total"] > 0:
            last_backup = backups["backups"][0]["created_at"]
        
        # Obtener próximo backup programado
        if is_running:
            for job in schedule.get_jobs():
                next_run = job.next_run
                if next_run:
                    next_backup = next_run.isoformat()
                break
                
        return {
            "success": True,
            "is_running": is_running,
            "backup_count": backup_count,
            "total_size": total_size,
            "formatted_size": size_str,
            "last_backup": last_backup,
            "next_backup": next_backup,
            "backup_dir": BACKUP_DIR
        }
        
    except Exception as e:
        logger.error(f"Error al obtener estado de backups: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        } 