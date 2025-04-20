"""
Exportaciones centrales de configuración para MSAD
"""

# Exportar todas las funciones de configuración
from msad.config.app_settings import (
    IS_WINDOWS,
    HTTP_PORT,
    BACKUP_RETENTION,
    get_base_dir,
    get_msad_dir,
    get_storage_dir,
    get_log_dir,
    get_config_dir,
    get_database_path,
    get_storage_path,
    get_backup_retention,
    ensure_directories
) 