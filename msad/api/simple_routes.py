"""
Rutas simplificadas para MSAD
"""
from flask import Blueprint, jsonify, request, send_file
import os

from msad.core.reports import generate_report, list_reports, get_report_file
from msad.core.backup import (
    init_backup_system, create_backup, list_backups, get_backup_file,
    restore_backup, delete_backup, start_backup_scheduler,
    stop_backup_scheduler, get_backup_status
)

def create_msad_blueprint():
    """
    Crea y devuelve un blueprint minimalista para la integración con Flask
    """
    msad_bp = Blueprint('msad_bp', __name__)
    
    @msad_bp.route('/msad/status', methods=['GET'])
    def get_status():
        """Endpoint para verificar el estado del servicio"""
        return jsonify({
            "success": True,
            "service": "msad",
            "version": "1.0.0-minimal",
            "status": "running"
        })
    
    @msad_bp.route('/msad/backups', methods=['GET'])
    def get_backups():
        """Endpoint para listar backups disponibles"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Obtener parámetros de filtrado opcionales
            backup_type = request.args.get('type')  # 'manual' o 'auto'
            
            # Listar backups
            result = list_backups(backup_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error al listar backups: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/create', methods=['POST'])
    def backup_db():
        """Endpoint para crear un backup manual"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Crear backup manual
            result = create_backup(manual=True)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error al crear backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/download/<filename>', methods=['GET'])
    def download_backup(filename):
        """Endpoint para descargar un backup"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Obtener la ruta del archivo
            file_path = get_backup_file(filename)
            
            if not file_path:
                return jsonify({
                    "success": False,
                    "error": "Archivo de backup no encontrado"
                }), 404
                
            # Enviar el archivo
            return send_file(
                file_path,
                mimetype="application/octet-stream",
                as_attachment=True,
                download_name=filename
            )
                
        except Exception as e:
            logger.error(f"Error al descargar backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/<filename>', methods=['DELETE'])
    def remove_backup(filename):
        """Endpoint para eliminar un backup"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Eliminar backup
            result = delete_backup(filename)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 404
                
        except Exception as e:
            logger.error(f"Error al eliminar backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/restore/<filename>', methods=['POST'])
    def restore_db(filename):
        """Endpoint para restaurar un backup"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Restaurar backup
            result = restore_backup(filename)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error al restaurar backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/scheduler', methods=['GET'])
    def get_scheduler_status():
        """Endpoint para obtener el estado del programador de backups"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Obtener estado
            result = get_backup_status()
            
            return jsonify(result)
                
        except Exception as e:
            logger.error(f"Error al obtener estado del programador: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @msad_bp.route('/msad/backups/scheduler', methods=['POST'])
    def configure_scheduler():
        """Endpoint para configurar el programador de backups"""
        try:
            # Inicializar sistema de backups si es necesario
            init_backup_system()
            
            # Obtener parámetros
            data = request.json or {}
            enabled = data.get('enabled', True)
            interval_hours = int(data.get('interval_hours', 24))
            
            # Configurar programador
            if enabled:
                result = start_backup_scheduler(interval_hours)
                message = f"Programador de backups iniciado con intervalo de {interval_hours} horas"
            else:
                result = stop_backup_scheduler()
                message = "Programador de backups detenido"
            
            if result:
                return jsonify({
                    "success": True,
                    "message": message,
                    "status": get_backup_status()
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Error al configurar programador de backups"
                }), 400
                
        except Exception as e:
            logger.error(f"Error al configurar programador: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    return msad_bp

def create_export_blueprint():
    """
    Crea y devuelve un blueprint para gestión de reportes
    """
    reports_bp = Blueprint('reports_bp', __name__)
    
    # 1. Endpoint para crear un reporte
    @reports_bp.route('/clients/<client_id>/msad/reports', methods=['POST'])
    def create_report(client_id):
        """Endpoint para crear un reporte de datos"""
        try:
            # Obtener parámetros de la solicitud
            data = request.json
            if not data:
                return jsonify({
                    "success": False,
                    "error": "Se requiere un cuerpo JSON en la solicitud"
                }), 400
                
            # Extraer parámetros
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            data_type = data.get('data_type', 'sensors')
            format = data.get('format', 'json')
            
            # Validar parámetros obligatorios
            if not start_date or not end_date:
                return jsonify({
                    "success": False,
                    "error": "Se requiere start_date y end_date"
                }), 400
                
            # Generar reporte
            result = generate_report(client_id, start_date, end_date, data_type, format)
            
            # Determinar el código de respuesta
            if result.get('success', False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error al crear reporte: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    # 2. Endpoint para listar reportes
    @reports_bp.route('/clients/<client_id>/msad/reports', methods=['GET'])
    def get_client_reports(client_id):
        """Endpoint para listar reportes de un cliente"""
        try:
            # Obtener parámetros de filtrado opcionales
            format = request.args.get('format')
            data_type = request.args.get('data_type')
            
            # Listar reportes
            result = list_reports(client_id, format, data_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error al listar reportes: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    # 3. Endpoint para listar todos los reportes
    @reports_bp.route('/msad/reports', methods=['GET'])
    def get_all_reports():
        """Endpoint para listar todos los reportes"""
        try:
            # Obtener parámetros de filtrado opcionales
            format = request.args.get('format')
            data_type = request.args.get('data_type')
            
            # Listar reportes
            result = list_reports(None, format, data_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error al listar reportes: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    # 4. Endpoint para descargar un reporte
    @reports_bp.route('/clients/<client_id>/msad/reports/download/<filename>', methods=['GET'])
    def download_report(client_id, filename):
        """Endpoint para descargar un reporte"""
        try:
            # Obtener la ruta del archivo
            file_path = get_report_file(client_id, filename)
            
            if not file_path:
                return jsonify({
                    "success": False,
                    "error": "Archivo no encontrado"
                }), 404
                
            # Determinar tipo MIME según la extensión
            mime_type = "application/octet-stream"  # Valor por defecto
            
            if filename.endswith('.json'):
                mime_type = "application/json"
            elif filename.endswith('.csv'):
                mime_type = "text/csv"
                
            # Enviar el archivo
            return send_file(
                file_path,
                mimetype=mime_type,
                as_attachment=True,
                download_name=filename
            )
                
        except Exception as e:
            logger.error(f"Error al descargar reporte: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    return reports_bp 