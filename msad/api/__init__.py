"""
API package for MSAD - Flask endpoints organized by functionality
"""

# Import routes from modular route files
from msad.api.system_routes import create_system_blueprint
from msad.api.backup_routes import create_backup_blueprint
from msad.api.report_routes import create_report_blueprint

# Export route creators for app.py integration
__all__ = [
    'create_system_blueprint',
    'create_backup_blueprint',
    'create_report_blueprint'
] 