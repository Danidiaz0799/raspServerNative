"""
MSAD - Microservicio de Almacenamiento Distribuido (Versión Modular)
"""

__version__ = '1.1.0'

# Solo exportamos las funciones que necesitamos para la integración con app.py
from msad.api.system_routes import create_system_blueprint
from msad.api.backup_routes import create_backup_blueprint
from msad.api.report_routes import create_report_blueprint
from msad.core.system import init_msad, shutdown_msad
from msad.core.backup import init_backup_system, start_backup_scheduler, stop_backup_scheduler

# Función para crear un único blueprint que incluya todas las rutas MSAD
def create_msad_blueprint():
    """Wrapper function to maintain backward compatibility"""
    return create_system_blueprint()

# Función para crear un único blueprint para los endpoints de reportes
def create_export_blueprint():
    """Wrapper function to maintain backward compatibility"""
    return create_report_blueprint()

# Estos son usados directamente por app.py
__all__ = [
    'create_msad_blueprint',
    'create_export_blueprint',
    'create_system_blueprint',
    'create_backup_blueprint',
    'create_report_blueprint',
    'init_msad',
    'shutdown_msad',
    'init_backup_system',
    'start_backup_scheduler',
    'stop_backup_scheduler'
] 