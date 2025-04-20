# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from routes.client_routes import client_bp
from routes.sensor_routes import sensor_bp
from routes.event_routes import event_bp
from routes.actuator_routes import actuator_bp
from routes.app_state_routes import app_state_bp
from routes.statistics_routes import statistics_bp
# La siguiente línea causa error porque ya no existe routes.msad_routes
# from routes.msad_routes import msad_bp
from mqtt_client import connect_mqtt, cleanup as mqtt_cleanup
import os
import threading
from models.sensor_data import cleanup
import atexit
from database import create_tables
# Integración con MSAD
from msad import (
    init_msad, shutdown_msad, 
    create_system_blueprint, create_backup_blueprint, create_report_blueprint
)

# Configuracion de la carpeta donde esta la app Angular
ANGULAR_BUILD_FOLDER = "/home/stevpi/Desktop/raspServer/angular_app/dist/mushroom-automation"

# Configuraciones para optimizacion
DEBUG_MODE = False  # Cambiar a True solo para desarrollo
THREADED = True

# Crear la aplicacion Flask
app = Flask(__name__, static_folder=ANGULAR_BUILD_FOLDER)

# Configurar CORS optimizado - permitir solo origen especifico en produccion
if DEBUG_MODE:
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    CORS(app, resources={r"/api/*": {"origins": "*"}})

# Reducir el tamano de la respuesta con compresion
app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500

# Registrar Blueprints para modularizar las rutas - El orden es importante
app.register_blueprint(client_bp, url_prefix='/api')
app.register_blueprint(sensor_bp, url_prefix='/api')
app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(actuator_bp, url_prefix='/api')
app.register_blueprint(app_state_bp, url_prefix='/api')
app.register_blueprint(statistics_bp, url_prefix='/api')
# app.register_blueprint(msad_bp, url_prefix='/api')  # Comentamos esta línea porque ya no existe msad_bp

# Registramos los blueprints de MSAD de forma modular
system_bp = create_system_blueprint()
backup_bp = create_backup_blueprint()
report_bp = create_report_blueprint()

app.register_blueprint(system_bp, url_prefix='/api')
app.register_blueprint(backup_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')

# Inicializar MSAD (Microservicio de Almacenamiento Distribuido)
msad_status = init_msad(auto_backup=True, backup_interval_hours=24)
print(f"Estado de MSAD: {msad_status['message']}")

# Cache para archivos estaticos
cache_timeout = 3600  # 1 hora para archivos estaticos

# Ruta para servir archivos estaticos (JS, CSS, imagenes, etc.) con cache
@app.route('/<path:filename>')
def serve_static_files(filename):
    file_path = os.path.join(ANGULAR_BUILD_FOLDER, filename)
    # Si el archivo existe, lo sirve normalmente con cache
    if os.path.isfile(file_path):
        response = send_from_directory(ANGULAR_BUILD_FOLDER, filename)
        if not DEBUG_MODE and not filename.endswith('.html'):
            response.headers['Cache-Control'] = f'public, max-age={cache_timeout}'
        return response
    # Si no existe, devolver el index.html (manejo de rutas SPA)
    return send_from_directory(ANGULAR_BUILD_FOLDER, 'index.html')

# Ruta para servir la pagina principal
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_index(path):
    # Evitar conflictos con rutas API
    if path.startswith('api/'):
        return {"error": "No encontrado"}, 404
    return send_from_directory(ANGULAR_BUILD_FOLDER, 'index.html')

# Funcion para conectar MQTT en un hilo separado
def start_mqtt_client():
    connect_mqtt()

# Limpiar recursos al salir
def on_exit():
    print("Limpiando recursos antes de salir...")
    mqtt_cleanup()
    # Limpiar MSAD antes de salir
    shutdown_msad()
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cleanup())
    loop.close()
    print("Recursos liberados correctamente")

# Registrar funcion de limpieza al salir
atexit.register(on_exit)

# Iniciar la aplicacion
if __name__ == '__main__':
    # Crear tablas de la base de datos si no existen
    print("Inicializando la base de datos...")
    create_tables()
    
    # Iniciar cliente MQTT en un hilo separado para no bloquear
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    # Iniciar Flask
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=DEBUG_MODE, 
        threaded=THREADED,
        use_reloader=False
    )
