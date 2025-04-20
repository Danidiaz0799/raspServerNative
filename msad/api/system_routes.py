"""
System routes module for MSAD - Status and general system endpoints
"""
from flask import Blueprint, jsonify

def create_system_blueprint():
    """
    Creates and returns a blueprint for system-related endpoints
    """
    system_bp = Blueprint('msad_system_bp', __name__)

    @system_bp.route('/msad/status', methods=['GET'])
    def get_status():
        """Endpoint to check service status"""
        return jsonify({
            "success": True,
            "service": "msad",
            "version": "1.1.0",
            "status": "running"
        })

    return system_bp