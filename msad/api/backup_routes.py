"""
Backup routes module for MSAD - Backup management endpoints
"""
from flask import Blueprint, jsonify, request, send_file
from msad.core.system import logger
from msad.core.backup import (
    init_backup_system, create_backup, list_backups, get_backup_file,
    restore_backup, delete_backup, start_backup_scheduler, 
    stop_backup_scheduler, get_backup_status
)

def create_backup_blueprint():
    """
    Creates and returns a blueprint for backup-related endpoints
    """
    backup_bp = Blueprint('msad_backup_bp', __name__)
    
    @backup_bp.route('/msad/backups', methods=['GET'])
    def get_backups():
        """Endpoint to list available backups"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Get optional filtering parameters
            backup_type = request.args.get('type')  # 'manual' or 'auto'
            
            # List backups
            result = list_backups(backup_type)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error listing backups: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/create', methods=['POST'])
    def backup_db():
        """Endpoint to create a manual backup"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Create manual backup
            result = create_backup(manual=True)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/download/<filename>', methods=['GET'])
    def download_backup(filename):
        """Endpoint to download a backup"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Get file path
            file_path = get_backup_file(filename)
            
            if not file_path:
                return jsonify({
                    "success": False,
                    "error": "Backup file not found"
                }), 404
                
            # Send file
            return send_file(
                file_path,
                mimetype="application/octet-stream",
                as_attachment=True,
                download_name=filename
            )
                
        except Exception as e:
            logger.error(f"Error downloading backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/<filename>', methods=['DELETE'])
    def remove_backup(filename):
        """Endpoint to delete a backup"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Delete backup
            result = delete_backup(filename)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 404
                
        except Exception as e:
            logger.error(f"Error deleting backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/restore/<filename>', methods=['POST'])
    def restore_db(filename):
        """Endpoint to restore a backup"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Restore backup
            result = restore_backup(filename)
            
            if result.get("success", False):
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/scheduler', methods=['GET'])
    def get_scheduler_status():
        """Endpoint to get the status of the backup scheduler"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Get status
            result = get_backup_status()
            # Siempre incluir interval_hours
            if 'interval_hours' not in result:
                from msad.core.backup import interval_hours as global_interval_hours
                result['interval_hours'] = global_interval_hours
            return jsonify(result)
                
        except Exception as e:
            logger.error(f"Error getting scheduler status: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @backup_bp.route('/msad/backups/scheduler', methods=['POST'])
    def configure_scheduler():
        """Endpoint to configure the backup scheduler"""
        try:
            # Initialize backup system if needed
            init_backup_system()
            
            # Get parameters
            data = request.json or {}
            enabled = data.get('enabled', True)
            interval_hours = int(data.get('interval_hours', 24))
            
            # Configure scheduler
            if enabled:
                result = start_backup_scheduler(interval_hours)
                message = f"Backup scheduler started with interval of {interval_hours} hours"
            else:
                result = stop_backup_scheduler()
                message = "Backup scheduler stopped"
            
            status = get_backup_status()
            status['interval_hours'] = interval_hours  # Asegura que se devuelve el valor correcto
            if result:
                return jsonify({
                    "success": True,
                    "message": message,
                    "status": status
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Error configuring backup scheduler"
                }), 400
                
        except Exception as e:
            logger.error(f"Error configuring scheduler: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    return backup_bp 