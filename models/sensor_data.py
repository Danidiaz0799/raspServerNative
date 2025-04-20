import aiosqlite
from datetime import datetime
import time
import asyncio
import functools
from typing import Dict, Any, Optional, List, Tuple

# Caché para parámetros ideales
_ideal_params_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
_cache_expiry: Dict[Tuple[str, str], float] = {}
CACHE_DURATION = 60  # Duración de la caché en segundos

# Conectar a la base de datos
async def get_db_connection():
    conn = await aiosqlite.connect('/home/stevpi/Desktop/raspServer/sensor_data.db')
    conn.row_factory = aiosqlite.Row
    return conn

async def execute_query_with_retry(query, params=(), retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = await get_db_connection()
            async with conn.execute(query, params) as cursor:
                result = await cursor.fetchall()
            await conn.commit()
            await conn.close()
            return result
        except aiosqlite.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

async def execute_write_query_with_retry(query, params=(), retries=5, delay=1):
    for attempt in range(retries):
        try:
            conn = await get_db_connection()
            await conn.execute(query, params)
            await conn.commit()
            await conn.close()
            return
        except aiosqlite.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

# Función para agrupar múltiples inserciones
async def batch_insert_sht3x_data(data_list):
    if not data_list:
        return
    
    conn = await get_db_connection()
    try:
        await conn.executemany(
            'INSERT INTO sht3x_data (client_id, timestamp, temperature, humidity) VALUES (?, ?, ?, ?)',
            data_list
        )
        await conn.commit()
    finally:
        await conn.close()

# Buffer para acumular datos antes de inserción
_sht3x_buffer: List[Tuple[str, str, float, float]] = []
_last_flush_time = time.time()
MAX_BUFFER_SIZE = 10
MAX_BUFFER_TIME = 5  # segundos

# Guardar datos del sht3x en la base de datos (con buffer)
async def save_sht3x_data(client_id, temperature, humidity):
    global _sht3x_buffer, _last_flush_time
    
    timestamp = datetime.now().isoformat()
    _sht3x_buffer.append((client_id, timestamp, temperature, humidity))
    
    current_time = time.time()
    should_flush = (
        len(_sht3x_buffer) >= MAX_BUFFER_SIZE or 
        current_time - _last_flush_time > MAX_BUFFER_TIME
    )
    
    if should_flush:
        buffer_copy = _sht3x_buffer.copy()
        _sht3x_buffer = []
        _last_flush_time = current_time
        await batch_insert_sht3x_data(buffer_copy)

# Obtener todos los datos de sht3x desde la base de datos
async def get_all_sht3x_data(client_id, page, page_size):
    query = '''
        SELECT * FROM sht3x_data 
        WHERE client_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
    '''
    params = (client_id, page_size, (page - 1) * page_size)
    result = await execute_query_with_retry(query, params)
    return result

# Obtener parametros ideales desde la base de datos (con caché)
async def get_ideal_params(client_id, param_type):
    cache_key = (client_id, param_type)
    current_time = time.time()
    
    # Verificar si los datos están en caché y son válidos
    if cache_key in _ideal_params_cache and current_time < _cache_expiry.get(cache_key, 0):
        return _ideal_params_cache[cache_key]
    
    # Consultar la base de datos
    query = '''
        SELECT * FROM ideal_params 
        WHERE client_id = ? AND param_type = ? 
        ORDER BY timestamp DESC LIMIT 1
    '''
    params = (client_id, param_type)
    result = await execute_query_with_retry(query, params)
    
    if result:
        # Guardar en caché
        _ideal_params_cache[cache_key] = dict(result[0])
        _cache_expiry[cache_key] = current_time + CACHE_DURATION
        return _ideal_params_cache[cache_key]
    return None

# Actualizar parametros ideales en la base de datos (y caché)
async def update_ideal_params(client_id, param_type, min_value, max_value):
    # Actualizar en la base de datos
    query = '''
        UPDATE ideal_params
        SET min_value = ?, max_value = ?, timestamp = ?
        WHERE client_id = ? AND param_type = ?
    '''
    timestamp = datetime.now().isoformat()
    params = (min_value, max_value, timestamp, client_id, param_type)
    await execute_write_query_with_retry(query, params)
    
    # Actualizar caché
    cache_key = (client_id, param_type)
    _ideal_params_cache[cache_key] = {
        'client_id': client_id,
        'param_type': param_type,
        'min_value': min_value,
        'max_value': max_value,
        'timestamp': timestamp
    }
    _cache_expiry[cache_key] = time.time() + CACHE_DURATION

# Limpiar buffer y cerrar conexiones antes de salir
async def cleanup():
    if _sht3x_buffer:
        await batch_insert_sht3x_data(_sht3x_buffer.copy())
        _sht3x_buffer.clear()
