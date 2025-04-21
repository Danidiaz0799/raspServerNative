# Servidor Raspberry Pi para Automatización de Cultivo de Hongos

Este proyecto implementa un servidor web Flask que se ejecuta en una Raspberry Pi para monitorear y controlar un sistema de cultivo de hongos automatizado. Interactúa con clientes MQTT (probablemente ESP32 u otros microcontroladores) para recibir datos de sensores (temperatura, humedad) y controlar actuadores (luces, ventiladores, humidificadores, motores). También incluye una interfaz web construida con Angular y un microservicio para almacenamiento distribuido (MSAD).

## Características Principales

*   **Servidor Web Flask:** Proporciona una API RESTful para interactuar con el sistema.
*   **Cliente MQTT:** Se comunica con dispositivos IoT para recibir datos de sensores y enviar comandos a actuadores.
*   **Base de Datos:** Almacena datos de sensores, eventos, información de clientes y estados de actuadores (probablemente SQLite).
*   **Control Automático:** Ajusta los actuadores (luz, ventilador, humidificador, motor) según los parámetros ideales de temperatura y humedad definidos para cada cliente.
*   **Gestión de Clientes:** Registra y monitorea el estado de los clientes MQTT conectados.
*   **Registro de Eventos:** Guarda eventos importantes como alertas de sensores fuera de rango o cambios en los actuadores.
*   **Interfaz Web Angular:** Permite visualizar datos y controlar el sistema (ubicada en `angular_app/`).
*   **MSAD (Microservicio de Almacenamiento Distribuido):** Módulo para gestionar copias de seguridad y reportes del sistema.
*   **Optimización:** Incluye configuraciones para compresión de respuestas, caché de archivos estáticos y manejo eficiente de tareas asíncronas y MQTT.

## Pila Tecnológica

*   **Backend:** Python, Flask
*   **Comunicación IoT:** MQTT (Paho MQTT)
*   **Frontend:** Angular (servido por Flask)
*   **Base de Datos:** SQLite (implícito por `database.py` y `sensor_data.db`)
*   **Asincronía:** `asyncio`, `threading`

## Estructura del Proyecto

```
.
├── app.py                  # Punto de entrada principal de la aplicación Flask
├── database.py             # Lógica de inicialización y conexión a la base de datos
├── mqtt_client.py          # Cliente MQTT para comunicación con dispositivos
├── sensor_data.db          # Archivo de la base de datos SQLite
├── angular_app/            # Código fuente y build de la aplicación Angular
├── models/                 # Clases y funciones para interactuar con la base de datos (sensores, clientes, eventos, etc.)
├── routes/                 # Blueprints de Flask para definir las rutas de la API
├── msad/                   # Módulo del Microservicio de Almacenamiento Distribuido
│   ├── api/                # Rutas API específicas de MSAD
│   ├── config/             # Configuración de MSAD
│   ├── core/               # Lógica principal de MSAD (backup, reportes)
│   ├── server/             # Servidor de MSAD
│   └── run_msad.py         # Script para ejecutar MSAD de forma independiente
└── __pycache__/            # Archivos de caché de Python
```

## Configuración e Instalación (Pasos Generales)

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd raspServer
    ```
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate   # En Windows
    ```
3.  **Instalar dependencias:** (Necesitarás un archivo `requirements.txt`)
    ```bash
    pip install Flask Flask-Cors paho-mqtt # ... y otras dependencias necesarias
    ```
4.  **Construir la aplicación Angular:** Navega a `angular_app/` y sigue las instrucciones de construcción de Angular (ej. `npm install && ng build`). Asegúrate de que la ruta `ANGULAR_BUILD_FOLDER` en `app.py` coincida con la carpeta de salida de la compilación de Angular.
5.  **Configurar el Broker MQTT:** Asegúrate de tener un broker MQTT ejecutándose (por ejemplo, Mosquitto) en `localhost:1883`.

## Ejecutar la Aplicación

```bash
python app.py
```

El servidor Flask se iniciará, generalmente en `http://0.0.0.0:5000`. El cliente MQTT intentará conectarse al broker local. La aplicación Angular será accesible desde la raíz (`/`).

## Módulos Clave

*   **`app.py`:** Orquesta la aplicación Flask, registra las rutas (Blueprints), inicializa el cliente MQTT en un hilo separado, configura CORS, compresión, y sirve la aplicación Angular. También inicializa el módulo MSAD.
*   **`mqtt_client.py`:** Gestiona la conexión al broker MQTT, se suscribe a los tópicos relevantes (`clients/+/sensor/sht3x`, `clients/+/register`), procesa los mensajes entrantes (datos de sensores, registros de clientes), guarda datos y eventos, y controla los actuadores en modo automático. Utiliza `asyncio` para operaciones asíncronas y optimizaciones como caché y throttling.
*   **`msad/`:** Contiene la lógica para el Microservicio de Almacenamiento Distribuido, encargado de tareas como copias de seguridad automáticas y generación de reportes. Puede ejecutarse de forma independiente con `python msad/run_msad.py`.
*   **`models/`:** Define la interacción con la base de datos para las diferentes entidades (Sensores, Clientes, Eventos, Actuadores, Estado de la App, Estadísticas).
*   **`routes/`:** Define los endpoints de la API RESTful utilizando Flask Blueprints para organizar las rutas por funcionalidad.
