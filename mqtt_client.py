import paho.mqtt.client as mqtt
from models.sensor_data import save_sht3x_data, get_ideal_params
from models.event import save_event
from models.client import update_client_status, register_client, client_exists
import time
from models.actuator import update_actuator_state, get_actuator_state, get_actuator_by_name
from models.app_state import get_app_state
import asyncio
import re
from collections import defaultdict
from functools import lru_cache
import threading

client = None
client_last_events = {}  # Diccionario para rastrear el último evento por cliente y tipo
client_actuator_cache = {}  # Caché de actuadores por cliente
client_status_update_time = {}  # Último momento en que se actualizó el estado de un cliente

# Límite de tiempo para actualizar el estado del cliente (segundos)
CLIENT_STATUS_UPDATE_INTERVAL = 60

# Bucle de eventos para operaciones asincronas
loop = None
loop_thread = None
loop_ready = threading.Event()

# Extraer client_id del tópico con regex compilado para mayor eficiencia
_client_id_pattern = re.compile(r'clients/([^/]+)/')

def extract_client_id(topic):
    match = _client_id_pattern.match(topic)
    if match:
        return match.group(1)
    return None

# Funcion para ejecutar corrutinas en el bucle de eventos
def run_coroutine(coro):
    global loop
    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(coro, loop)
    else:
        print("Error: El bucle de eventos no esta en ejecucion")

# Manejo de mensajes optimizado
def on_message(client, userdata, msg):
    try:
        # Extraer el client_id del tópico
        client_id = extract_client_id(msg.topic)
        if not client_id:
            print(f"No se pudo extraer client_id del topico: {msg.topic}")
            return
        
        # Actualizar estado del cliente con throttling
        current_time = time.time()
        if (client_id not in client_status_update_time or 
            current_time - client_status_update_time.get(client_id, 0) > CLIENT_STATUS_UPDATE_INTERVAL):
            run_coroutine(update_client_status(client_id))
            client_status_update_time[client_id] = current_time
        
        # Procesar el mensaje según el tópico
        if msg.topic == f'clients/{client_id}/sensor/sht3x':
            data = msg.payload.decode('utf-8', errors='ignore').split(',')
            if len(data) == 2:
                run_coroutine(handle_sht3x_message(client_id, data))
        elif msg.topic == f'clients/{client_id}/register':
            data = msg.payload.decode('utf-8', errors='ignore').split(',')
            if len(data) >= 2:
                name = data[0]
                description = data[1] if len(data) > 1 else ""
                run_coroutine(register_client(client_id, name, description))
        else:
            print(f"Topico no reconocido: {msg.topic}")
    except Exception as e:
        print(f'Error al procesar el mensaje: {e}')

async def handle_sht3x_message(client_id, data):
    try:
        temperatura, humedad = float(data[0]), float(data[1])
        
        # Guardar datos en la base (ahora con buffer)
        await save_sht3x_data(client_id, temperatura, humedad)
        
        # Verificar eventos con throttling
        current_time = time.time()
        
        # Inicializar entradas para este cliente si no existen
        if client_id not in client_last_events:
            client_last_events[client_id] = {'temp': 0, 'hum': 0}
        
        # Obtener parámetros ideales (ahora con caché)
        ideal_temp_params = await get_ideal_params(client_id, 'temperatura')
        ideal_humidity_params = await get_ideal_params(client_id, 'humedad')
        
        if not ideal_temp_params or not ideal_humidity_params:
            return
        
        min_temp = ideal_temp_params['min_value']
        max_temp = ideal_temp_params['max_value']
        min_humidity = ideal_humidity_params['min_value']
        max_humidity = ideal_humidity_params['max_value']
        
        # Verificar temperatura con throttling
        if not (min_temp <= temperatura <= max_temp):
            if current_time - client_last_events[client_id]['temp'] > 60:
                await save_event(
                    client_id, 
                    f"Advertencia! Temperatura fuera de rango: {temperatura} C (Ideal: {min_temp}-{max_temp} C)", 
                    "temperatura"
                )
                client_last_events[client_id]['temp'] = current_time
        
        # Verificar humedad con throttling
        if not (min_humidity <= humedad <= max_humidity):
            if current_time - client_last_events[client_id]['hum'] > 60:
                await save_event(
                    client_id, 
                    f"Advertencia! Humedad fuera de rango: {humedad} % (Ideal: {min_humidity}-{max_humidity} %)", 
                    "humedad"
                )
                client_last_events[client_id]['hum'] = current_time
        
        # Verificar modo automático y actualizar actuadores
        app_state = await get_app_state(client_id)
        if app_state == 'automatico':
            await update_actuators(client_id, temperatura, humedad)
    except Exception as e:
        print(f"Error procesando mensaje SHT3x: {e}")

# Función para obtener y almacenar en caché los actuadores
async def get_cached_actuator(client_id, name):
    # Usar caché si está disponible
    cache_key = f"{client_id}_{name}"
    if cache_key in client_actuator_cache:
        return client_actuator_cache[cache_key]
    
    # Obtener de la base de datos
    actuator = await get_actuator_by_name(client_id, name)
    if actuator:
        client_actuator_cache[cache_key] = actuator
    
    return actuator

async def update_actuators(client_id, temperature, humidity):
    try:
        # Obtener parámetros ideales (caché)
        ideal_temp_params = await get_ideal_params(client_id, 'temperatura')
        ideal_humidity_params = await get_ideal_params(client_id, 'humedad')
        
        if not ideal_temp_params or not ideal_humidity_params:
            return
        
        min_temp = ideal_temp_params['min_value']
        max_temp = ideal_temp_params['max_value']
        min_humidity = ideal_humidity_params['min_value']
        max_humidity = ideal_humidity_params['max_value']
        
        # Obtener actuadores con caché
        light_actuator = await get_cached_actuator(client_id, "Iluminacion")
        fan_actuator = await get_cached_actuator(client_id, "Ventilacion")
        humidifier_actuator = await get_cached_actuator(client_id, "Humidificador")
        motor_actuator = await get_cached_actuator(client_id, "Motor")
        
        if not all([light_actuator, fan_actuator, humidifier_actuator, motor_actuator]):
            return
        
        # Lista para todas las tareas de actualización
        all_tasks = []
        
        # Acciones para temperatura
        if temperature < min_temp:
            # Temperatura baja: encender luz
            all_tasks.append(update_actuator_and_log(client_id, light_actuator['id'], 'true', "Temperatura baja, encendiendo luz", f'clients/{client_id}/light'))
            all_tasks.append(update_actuator_and_log(client_id, fan_actuator['id'], 'false', "Ventilador apagado", f'clients/{client_id}/fan'))
        elif temperature > max_temp:
            # Temperatura alta: encender ventilador
            all_tasks.append(update_actuator_and_log(client_id, light_actuator['id'], 'false', "Luz apagada", f'clients/{client_id}/light'))
            all_tasks.append(update_actuator_and_log(client_id, fan_actuator['id'], 'true', "Temperatura alta, encendiendo ventilador", f'clients/{client_id}/fan'))
        else:
            # Temperatura normal: apagar ambos
            all_tasks.append(update_actuator_and_log(client_id, light_actuator['id'], 'false', "Temperatura normal, luz apagada", f'clients/{client_id}/light'))
            all_tasks.append(update_actuator_and_log(client_id, fan_actuator['id'], 'false', "Temperatura normal, ventilador apagado", f'clients/{client_id}/fan'))
        
        # Acciones para humedad
        if humidity < min_humidity:
            # Humedad baja: encender humidificador
            all_tasks.append(update_actuator_and_log(client_id, humidifier_actuator['id'], 'true', "Humedad baja, encendiendo humidificador", f'clients/{client_id}/humidifier'))
            all_tasks.append(update_actuator_and_log(client_id, motor_actuator['id'], 'false', "Motor apagado", f'clients/{client_id}/motor'))
        elif humidity > max_humidity:
            # Humedad alta: encender motor
            all_tasks.append(update_actuator_and_log(client_id, humidifier_actuator['id'], 'false', "Humidificador apagado", f'clients/{client_id}/humidifier'))
            all_tasks.append(update_actuator_and_log(client_id, motor_actuator['id'], 'true', "Humedad alta, encendiendo motor", f'clients/{client_id}/motor'))
        else:
            # Humedad normal: apagar ambos
            all_tasks.append(update_actuator_and_log(client_id, humidifier_actuator['id'], 'false', "Humedad normal, humidificador apagado", f'clients/{client_id}/humidifier'))
            all_tasks.append(update_actuator_and_log(client_id, motor_actuator['id'], 'false', "Humedad normal, motor apagado", f'clients/{client_id}/motor'))
        
        # Ejecutar todas las tareas en paralelo
        await asyncio.gather(*all_tasks)
    except Exception as e:
        print(f"Error actualizando actuadores: {e}")

# Caché para el estado del actuador
_actuator_state_cache = {}
_actuator_last_update = {}
ACTUATOR_CACHE_DURATION = 5  # Segundos

async def update_actuator_and_log(client_id, actuator_id, state, description, topic):
    try:
        # Verificar si el cambio es necesario usando caché
        cache_key = f"{client_id}_{actuator_id}"
        current_time = time.time()
        
        # Si el estado está en caché y es reciente, usarlo
        if (cache_key in _actuator_state_cache and
            current_time - _actuator_last_update.get(cache_key, 0) < ACTUATOR_CACHE_DURATION):
            current_state = _actuator_state_cache[cache_key]
        else:
            # Obtener de la base de datos
            current_state = await get_actuator_state(client_id, actuator_id)
            # Actualizar caché
            _actuator_state_cache[cache_key] = current_state
            _actuator_last_update[cache_key] = current_time
        
        # Actualizar sólo si es necesario
        if current_state != state:
            # Primero actualizar la base de datos
            await update_actuator_state(client_id, actuator_id, state)
            
            # Luego publicar el mensaje MQTT inmediatamente
            message = str(state).lower()
            if client and client.is_connected():
                client.publish(topic, message, qos=1)  # QoS 1 para asegurar al menos una entrega
                print(f"Publicando mensaje MQTT - Topico: {topic}, Mensaje: {message}")
            
            # Actualizar caché
            _actuator_state_cache[cache_key] = state
            _actuator_last_update[cache_key] = current_time
            
            # Guardar evento
            await save_event(client_id, description, "actuador")
    except Exception as e:
        print(f"Error en update_actuator_and_log: {e}")

# Cola de mensajes para publicación MQTT
_mqtt_message_queue = []
_last_mqtt_publish = time.time()
MAX_QUEUE_SIZE = 10
MAX_QUEUE_TIME = 0.1  # segundos

# Función para publicar mensajes MQTT
async def publish_message(topic, message):
    global client, _mqtt_message_queue, _last_mqtt_publish
    
    _mqtt_message_queue.append((topic, message))
    current_time = time.time()
    
    # Publicar inmediatamente si la cola está llena o ha pasado suficiente tiempo
    if len(_mqtt_message_queue) >= MAX_QUEUE_SIZE or current_time - _last_mqtt_publish > MAX_QUEUE_TIME:
        await _process_mqtt_queue()

async def _process_mqtt_queue():
    global client, _mqtt_message_queue, _last_mqtt_publish
    
    if not _mqtt_message_queue:
        return
    
    if client and client.is_connected():
        queue_copy = _mqtt_message_queue.copy()
        _mqtt_message_queue = []
        _last_mqtt_publish = time.time()
        
        for topic, message in queue_copy:
            try:
                client.publish(topic, message, qos=1)  # QoS 1 para asegurar al menos una entrega
                print(f"Procesando cola MQTT - Topico: {topic}, Mensaje: {message}")
            except Exception as e:
                print(f"Error al publicar mensaje MQTT: {e}")
                # Reintentar más tarde
                _mqtt_message_queue.append((topic, message))
    else:
        print("Cliente MQTT no esta conectado, reintentando mas tarde...")

# Funcion para ejecutar el bucle de eventos asincrono
def run_event_loop():
    global loop
    asyncio.set_event_loop(loop)
    loop_ready.set()
    loop.run_forever()

# Configuración del cliente MQTT
def connect_mqtt():
    global client, loop, loop_thread
    
    # Iniciar bucle de eventos asincrono en un hilo separado
    loop = asyncio.new_event_loop()
    loop_thread = threading.Thread(target=run_event_loop, daemon=True)
    loop_thread.start()
    
    # Esperar a que el bucle este listo
    loop_ready.wait()
    
    # Configurar cliente MQTT
    client = mqtt.Client()
    client.on_message = on_message
    
    # Configurar reconexión automática
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    
    try:
        client.connect('localhost', 1883, 60)
        
        # Suscribirse a todos los tópicos de clientes
        client.subscribe('clients/+/sensor/sht3x')
        client.subscribe('clients/+/register')
        
        client.loop_start()
        print("Cliente MQTT inicializado y suscrito a topicos de multiples clientes")
    except Exception as e:
        print(f"Error al conectar con el broker MQTT: {e}")
        print("Reintentando en 5 segundos...")
        time.sleep(5)
        connect_mqtt()

# Limpiar recursos al salir
def cleanup():
    global client, loop
    
    if client:
        client.loop_stop()
        client.disconnect()
        
    if loop:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        
        loop.call_soon_threadsafe(loop.stop)
        if loop_thread and loop_thread.is_alive():
            loop_thread.join(timeout=5)
