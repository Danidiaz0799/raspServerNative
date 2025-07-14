"""
Report routes module for MSAD - Data reporting and export endpoints
"""
from flask import Blueprint, jsonify, request, send_file
from msad.core.system import logger
from msad.core.reports import (
    generate_report,
    list_reports,
    get_report_file,
    start_report_scheduler_for_client,
    stop_report_scheduler_for_client,
    get_report_scheduler_status_for_client,
    get_all_report_schedulers_status
)

import os

def create_report_blueprint():
    """
    Creates and returns a blueprint for report-related endpoints
    """
    report_bp = Blueprint('msad_report_bp', __name__)
    
    @report_bp.route('/clients/<client_id>/msad/reports', methods=['POST'])
    def create_report(client_id):
        """Endpoint to create a data report"""
        try:
            # Get request parameters
            data = request.json
            if not data:
                return jsonify({
                    "success": False,
                    "error": "JSON body required in the request"
                }), 400
                
            # Extract parameters
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            data_type = data.get('data_type', 'sensors')
            format = data.get('format', 'json')
            
            # Validate required parameters
            if not start_date or not end_date:
                return jsonify({
                    "success": False,
                    "error": "start_date and end_date are required"
                }), 400
                
            # Generate report
            result = generate_report(client_id, start_date, end_date, data_type, format)
            
            # Determine response code
            if result.get('success', False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error creating report: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    @report_bp.route('/clients/<client_id>/msad/reports', methods=['GET'])
    def get_client_reports(client_id):
        """Endpoint to list reports for a client"""
        try:
            # Get optional filtering parameters
            format = request.args.get('format')
            data_type = request.args.get('data_type')
            
            # List reports
            result = list_reports(client_id, format, data_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error listing reports: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    @report_bp.route('/msad/reports', methods=['GET'])
    def get_all_reports():
        """Endpoint to list all reports"""
        try:
            # Get optional filtering parameters
            format = request.args.get('format')
            data_type = request.args.get('data_type')
            
            # List reports
            result = list_reports(None, format, data_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error listing reports: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    @report_bp.route('/clients/<client_id>/msad/reports/download/<filename>', methods=['GET'])
    def download_report(client_id, filename):
        """Endpoint to download a report"""
        try:
            # Get file path
            file_path = get_report_file(client_id, filename)
            
            if not file_path:
                return jsonify({
                    "success": False,
                    "error": "File not found"
                }), 404
                
            # Determine MIME type based on extension
            mime_type = "application/octet-stream"  # Default value
            
            if filename.endswith('.json'):
                mime_type = "application/json"
            elif filename.endswith('.csv'):
                mime_type = "text/csv"
                
            # Send file
            return send_file(
                file_path,
                mimetype=mime_type,
                as_attachment=True,
                download_name=filename
            )
                
        except Exception as e:
            logger.error(f"Error downloading report: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    @report_bp.route('/clients/<client_id>/msad/reports/<report_id>', methods=['DELETE'])
    def delete_report(client_id, report_id):
        """Endpoint to delete a report using report_id"""
        try:
            logger.info(f"Intentando eliminar reporte con ID {report_id} del cliente {client_id}")
            
            # Obtener la ruta del archivo usando el report_id
            file_path = get_report_file(client_id, report_id)
            
            if not file_path:
                logger.warning(f"Reporte no encontrado: {report_id}")
                return jsonify({
                    "success": False,
                    "error": "Reporte no encontrado",
                    "report_id": report_id,
                    "client_id": client_id
                }), 404
            
            # Obtener el nombre real del archivo desde la ruta
            filename = os.path.basename(file_path)
            
            # Eliminar el archivo
            try:
                os.remove(file_path)
                logger.info(f"Reporte eliminado: {filename}")
                return jsonify({
                    "success": True,
                    "message": "Reporte eliminado correctamente",
                    "report_id": report_id,
                    "filename": filename,
                    "client_id": client_id
                })
            except Exception as e:
                logger.error(f"Error al eliminar archivo {file_path}: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": f"No se pudo eliminar el archivo: {str(e)}",
                    "report_id": report_id
                }), 500
                
        except Exception as e:
            logger.error(f"Error al eliminar reporte: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
            
    # --- ENDPOINTS DE PROGRAMADOR DE REPORTES ---
    
    @report_bp.route('/msad/reports/scheduler/start', methods=['POST'])
    def start_report_scheduler_endpoint():
        """
        Inicia o reinicia el programador de reportes automáticos para un cliente específico.
        Body JSON:
        - interval_hours: int (obligatorio)
        - client_id: str (obligatorio)
        - start_date: str (YYYY-MM-DD o YYYY-MM-DD HH:MM)
        - end_date: str (YYYY-MM-DD o YYYY-MM-DD HH:MM)
        - data_type: str (opcional)
        - format: str (opcional)
        """
        try:
            config = request.json if request.is_json else None
            if not config or not config.get('client_id'):
                return jsonify({"success": False, "error": "client_id es obligatorio"}), 400
            client_id = config['client_id']
            start_report_scheduler_for_client(client_id, config)
            return jsonify({"success": True, "message": "Programador de reportes iniciado", "config": config}), 200
        except Exception as e:
            logger.error(f"Error al iniciar programador de reportes: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500

    @report_bp.route('/msad/reports/scheduler/stop', methods=['POST'])
    def stop_report_scheduler_endpoint():
        """
        Detiene el programador de reportes automáticos para un cliente específico.
        Body JSON:
        - client_id: str (obligatorio)
        """
        try:
            data = request.json if request.is_json else None
            if not data or not data.get('client_id'):
                return jsonify({"success": False, "error": "client_id es obligatorio"}), 400
            client_id = data['client_id']
            stop_report_scheduler_for_client(client_id)
            return jsonify({"success": True, "message": "Programador de reportes detenido"}), 200
        except Exception as e:
            logger.error(f"Error al detener programador de reportes: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500

    @report_bp.route('/msad/reports/scheduler/status', methods=['GET'])
    def get_report_scheduler_status_endpoint():
        """
        Obtiene el estado del programador de reportes de un cliente o de todos.
        Query param:
        - client_id: str (opcional)
        """
        try:
            client_id = request.args.get('client_id')
            if client_id:
                status = get_report_scheduler_status_for_client(client_id)
            else:
                status = get_all_report_schedulers_status()
            return jsonify(status), 200
        except Exception as e:
            logger.error(f"Error al obtener estado del programador de reportes: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500

    return report_bp