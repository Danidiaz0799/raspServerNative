"""
Configuración centralizada para el módulo MSAD
"""
import os
import platform

# Detectar sistema operativo
IS_WINDOWS = platform.system() == "Windows"

# Paths base
def get_base_dir():
    """Obtener directorio base"""
    if IS_WINDOWS:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    else:
        return "/home/stevpi/Desktop/raspServer"

def get_msad_dir():
    """Obtener directorio de MSAD"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_storage_dir():
    """Obtener directorio de almacenamiento"""
    if IS_WINDOWS:
        return os.path.join(get_base_dir(), "storage", "msad")
    else:
        return "/mnt/storage/msad"

def get_log_dir():
    """Obtener directorio de logs"""
    return os.path.join(get_msad_dir(), "logs")

def get_config_dir():
    """Obtener directorio de configuración"""
    return os.path.join(get_msad_dir(), "config")

def get_database_path():
    """Obtener ruta de la base de datos"""
    if IS_WINDOWS:
        return os.path.join(get_base_dir(), "sensor_data.db")
    else:
        return os.path.join(get_base_dir(), "sensor_data.db")

def get_storage_path(path=None):
    """Obtener una ruta dentro del almacenamiento"""
    if path:
        return os.path.join(get_storage_dir(), path)
    return get_storage_dir()

# Configuración del servidor HTTP
HTTP_PORT = 8080

# Configuración de respaldos
BACKUP_RETENTION = {
    "daily": 7,    # Número de respaldos diarios a mantener
    "weekly": 4,   # Número de respaldos semanales a mantener
    "monthly": 6   # Número de respaldos mensuales a mantener
}

def get_backup_retention(backup_type=None):
    """Obtener configuración de retención de respaldos"""
    if backup_type:
        return BACKUP_RETENTION.get(backup_type, 7)
    return BACKUP_RETENTION

def ensure_directories():
    """Crear directorios necesarios si no existen"""
    # Directorios principales
    os.makedirs(get_storage_dir(), exist_ok=True)
    os.makedirs(get_log_dir(), exist_ok=True)
    os.makedirs(get_config_dir(), exist_ok=True)
    
    # Estructura de almacenamiento
    os.makedirs(os.path.join(get_storage_dir(), "backups", "daily"), exist_ok=True)
    os.makedirs(os.path.join(get_storage_dir(), "backups", "weekly"), exist_ok=True)
    os.makedirs(os.path.join(get_storage_dir(), "backups", "monthly"), exist_ok=True)
    
    # Estructura para datos de clientes
    os.makedirs(os.path.join(get_storage_dir(), "data", "clients"), exist_ok=True)
    
    # Directorio base para exportaciones (nueva estructura)
    exports_dir = os.path.join(get_storage_dir(), "exports")
    os.makedirs(exports_dir, exist_ok=True)
    
    # Nota: Ya no creamos subdirectorios fijos para exportaciones
    # Los directorios específicos por cliente se crearán dinámicamente 