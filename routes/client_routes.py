from flask import Blueprint, request, jsonify
from models.client import get_all_clients, get_client_by_id, register_client, update_client_status, enable_client, update_client_info, delete_client

client_bp = Blueprint('client_bp', __name__)

# API para listar todos los clientes
@client_bp.route('/clients', methods=['GET'])
async def list_clients():
    try:
        clients = await get_all_clients()
        return jsonify([dict(client) for client in clients])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para obtener un cliente especifico
@client_bp.route('/clients/<client_id>', methods=['GET'])
async def get_client(client_id):
    try:
        client = await get_client_by_id(client_id)
        if client:
            return jsonify(dict(client))
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para registrar un nuevo cliente
@client_bp.route('/clients', methods=['POST'])
async def create_client():
    try:
        data = request.json
        client_id = data.get('client_id')
        name = data.get('name')
        description = data.get('description', '')
        
        if not client_id or not name:
            return jsonify({"error": "Se requiere client_id y name"}), 400
            
        await register_client(client_id, name, description)
        return jsonify({"message": "Cliente registrado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para actualizar el estado de un cliente
@client_bp.route('/clients/<client_id>/status', methods=['PUT'])
async def update_status(client_id):
    try:
        data = request.json
        status = data.get('status')
        
        if not status or status not in ['online', 'offline']:
            return jsonify({"error": "Estado no valido"}), 400
        
        if status == 'online':
            # Si estamos activando, usar la funcion especifica para ello
            await enable_client(client_id)
        else:
            # Si estamos desactivando, usar funcion existente
            await update_client_status(client_id, status)
            
        return jsonify({"message": "Estado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para actualizar informacion del cliente (nombre y descripcion)
@client_bp.route('/clients/<client_id>/info', methods=['PUT'])
async def update_info(client_id):
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"error": "Se requiere name"}), 400
            
        # Verificar si el cliente existe
        client = await get_client_by_id(client_id)
        if not client:
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        await update_client_info(client_id, name, description)
        return jsonify({"message": "Informacion del cliente actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para eliminar un cliente y todos sus datos relacionados
@client_bp.route('/clients/<client_id>', methods=['DELETE'])
async def remove_client(client_id):
    try:
        # Verificar si el cliente existe
        client = await get_client_by_id(client_id)
        if not client:
            return jsonify({"error": "Cliente no encontrado"}), 404
            
        # Eliminar cliente y todos los datos relacionados
        await delete_client(client_id)
        return jsonify({"message": "Cliente y todos sus datos eliminados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
