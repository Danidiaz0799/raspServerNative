"""
Funciones básicas del sistema MSAD
"""
import os
import logging
import datetime
import sqlite3

# Configuración básica
STORAGE_PATH = "/mnt/storage/msad"
if os.name == 'nt':  # Windows (para desarrollo)
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "storage", "msad")

# Configurar logging
def setup_logging():
    """Configurar sistema de logs básico"""
    log_dir = os.path.join(STORAGE_PATH, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        filename=os.path.join(log_dir, "msad.log"),
        level=logging.INFO,
        format='%(asctime)s - MSAD - %(levelname)s - %(message)s'
    )
    return logging.getLogger("msad")

logger = setup_logging()

def get_database_path():
    """Obtener ruta a la base de datos principal"""
    if os.name == 'nt':  # Windows
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sensor_data.db")
    else:  # Linux
        return "/home/stevpi/Desktop/raspServer/sensor_data.db"

def ensure_directories():
    """Crear estructura de directorios necesaria"""
    # Directorio base
    os.makedirs(STORAGE_PATH, exist_ok=True)
    
    # Directorios para reportes
    os.makedirs(os.path.join(STORAGE_PATH, "reports"), exist_ok=True)
    
    # Directorio para logs
    os.makedirs(os.path.join(STORAGE_PATH, "logs"), exist_ok=True)
    
    logger.info(f"Estructura de directorios creada en {STORAGE_PATH}")

def init_msad(auto_backup=False, backup_interval_hours=24):
    """
    Inicializar MSAD de forma muy simple
    """
    logger.info("Iniciando MSAD versión minimalista")
    
    try:
        # Crear estructura de directorios
        ensure_directories()
        
        # Verificar base de datos
        db_path = get_database_path()
        if not os.path.exists(db_path):
            logger.warning(f"Base de datos no encontrada en {db_path}")
            return {
                "success": False,
                "message": f"Base de datos no encontrada en {db_path}"
            }
        
        # Inicializar sistema de backups si está habilitado
        if auto_backup:
            # Importamos aquí para evitar dependencia circular
            from msad.core.backup import init_backup_system, start_backup_scheduler
            
            # Inicializar sistema de backups
            init_backup_system()
            
            # Iniciar programador de backups
            backup_result = start_backup_scheduler(backup_interval_hours)
            if backup_result:
                logger.info(f"Sistema de backups automáticos iniciado (intervalo: {backup_interval_hours} horas)")
            else:
                logger.warning("No se pudo iniciar el sistema de backups automáticos")
        
        logger.info("MSAD iniciado correctamente")
        return {
            "success": True,
            "message": "MSAD iniciado correctamente"
        }
    except Exception as e:
        logger.error(f"Error al iniciar MSAD: {str(e)}")
        return {
            "success": False,
            "message": f"Error al iniciar MSAD: {str(e)}"
        }

def shutdown_msad():
    """
    Detener MSAD de forma muy simple
    """
    logger.info("Deteniendo MSAD")
    
    try:
        # Detener programador de backups si está en ejecución
        try:
            from msad.core.backup import stop_backup_scheduler
            stop_backup_scheduler()
        except ImportError:
            pass  # El módulo puede no estar disponible
        except Exception as e:
            logger.error(f"Error al detener programador de backups: {str(e)}")
            
        return {
            "success": True,
            "message": "MSAD detenido correctamente"
        }
    except Exception as e:
        logger.error(f"Error al detener MSAD: {str(e)}")
        return {
            "success": False,
            "message": f"Error al detener MSAD: {str(e)}"
        }

def execute_query(query, params=(), fetchall=True):
    """
    Ejecutar consulta en la base de datos
    """
    try:
        db_path = get_database_path()
        logger.info(f"Conectando a base de datos: {db_path}")
        logger.info(f"Ejecutando consulta: {query}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            
            if fetchall:
                results = cursor.fetchall()
                processed_results = [dict(row) for row in results]
                logger.info(f"Consulta exitosa, {len(processed_results)} resultados obtenidos")
                conn.close()
                return processed_results
            else:
                conn.commit()
                logger.info("Consulta de escritura exitosa")
                conn.close()
                return True
        except sqlite3.Error as sql_error:
            logger.error(f"Error SQL específico: {str(sql_error)}, Consulta: {query}, Parámetros: {params}")
            conn.close()
            return None
            
    except Exception as e:
        logger.error(f"Error en consulta SQL: {str(e)}, Consulta: {query}, Parámetros: {params}")
        return None
