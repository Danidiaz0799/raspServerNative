# 🍄 RaspServer: Sistema de Control Ambiental para Cultivo de Hongos

![Versión](https://img.shields.io/badge/versión-1.1.0-blue)
![Estado](https://img.shields.io/badge/estado-activo-green)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-important)
![MQTT](https://img.shields.io/badge/mqtt-paho--mqtt-orange)
![Database](https://img.shields.io/badge/database-SQLite-lightgrey)

## 📋 Contenido

- [Descripción](#-descripción)
- [Características Principales](#-características-principales)
- [Arquitectura](#️-arquitectura)
- [Pila Tecnológica](#️-pila-tecnológica)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Esquema de la Base de Datos](#-esquema-de-la-base-de-datos)
- [Comunicación MQTT](#-comunicación-mqtt)
- [Instalación y Configuración](#️-instalación-y-configuración)
- [Ejecutar la Aplicación](#️-ejecutar-la-aplicación)
- [Documentación Adicional](#-documentación-adicional)
- [Módulos Clave](#-módulos-clave)
- [Resolución de Problemas](#-resolución-de-problemas)
- [Soporte](#-soporte)

## 📝 Descripción

**RaspServer** es una aplicación backend basada en Flask diseñada para automatizar y monitorear las condiciones ambientales óptimas para el cultivo de hongos (u otros entornos controlados). Utiliza una Raspberry Pi (o similar) como servidor central, interactuando con dispositivos cliente (nodos) a través del protocolo MQTT para recopilar datos de sensores (temperatura, humedad) y controlar actuadores (luces, ventiladores, humidificadores, motores).

El sistema incluye una API RESTful para la gestión de clientes, datos, eventos y configuración, así como un módulo integrado llamado **MSAD (Microservicio de Almacenamiento y Datos)** para funciones avanzadas de copia de seguridad y generación de reportes. El frontend se sirve como una aplicación Angular separada (no incluida en este repositorio backend, pero servida por él).

**Objetivo:** Proporcionar un sistema robusto, eficiente y fácil de gestionar para el control ambiental automatizado.

## ✨ Características Principales

*   **Monitoreo de Sensores:** Recibe y almacena datos de sensores (SHT3x para temperatura y humedad) enviados por clientes MQTT.
*   **Control de Actuadores:**
    *   **Manual:** Permite controlar actuadores (Iluminación, Ventilación, Humidificador, Motor) individualmente a través de la API.
    *   **Automático:** Ajusta automáticamente el estado de los actuadores según los parámetros ideales configurados (temperatura y humedad) cuando el sistema está en modo 'automatico'.
*   **Gestión de Clientes:** Registra, lista, actualiza el estado (online/offline) y elimina clientes MQTT.
*   **Registro de Eventos:** Guarda eventos importantes del sistema (advertencias de sensores fuera de rango, acciones de actuadores, etc.) para auditoría y seguimiento.
*   **Estadísticas:** Provee endpoints para obtener estadísticas básicas sobre los datos recolectados.
*   **Modo de Operación:** Permite cambiar el modo de funcionamiento del sistema entre 'manual' y 'automatico' por cliente.
*   **Parámetros Ideales:** Configura los rangos de temperatura y humedad deseados por cliente para el modo automático.
*   **Interfaz Web:** Sirve una aplicación frontend (Angular) para la interacción del usuario (el build de Angular debe colocarse en la ruta especificada).
*   **Módulo MSAD Integrado:**
    *   **Backups:** Creación manual y automática (programable) de backups de la base de datos SQLite (`sensor_data.db`). Permite listar, descargar, restaurar y eliminar backups.
    *   **Reportes:** Generación de reportes de datos históricos (sensores, eventos) en formatos JSON o CSV, filtrados por cliente, rango de fechas y tipo de dato. Permite listar y descargar reportes.

## 🏗️ Arquitectura

El sistema sigue una arquitectura cliente-servidor distribuida:

1.  **Servidor Central (RaspServer - Flask):**
    *   Ejecuta la aplicación Flask (`app.py`).
    *   Se conecta a un broker MQTT (local o remoto).
    *   Se suscribe a tópicos MQTT para recibir datos de los nodos cliente.
    *   Procesa los mensajes recibidos:
        *   Guarda datos de sensores en la base de datos SQLite (`database.py`, `models/`).
        *   Registra eventos (`models/event.py`).
        *   Actualiza el estado de los clientes (`models/client.py`).
        *   En modo automático, evalúa los datos y publica comandos MQTT a los actuadores de los nodos (`mqtt_client.py`).
    *   Expone una API RESTful (`routes/`) para interactuar con el frontend y otros sistemas.
    *   Sirve los archivos estáticos de la aplicación frontend Angular.
    *   Gestiona el módulo MSAD para backups y reportes (`msad/`).
2.  **Broker MQTT (Ej: Mosquitto):** Actúa como intermediario para toda la comunicación entre el servidor y los nodos cliente.
3.  **Nodos Cliente (Ej: Raspberry Pi, ESP32):**
    *   Dispositivos con sensores y/o actuadores conectados.
    *   Ejecutan código (no incluido en este repo) que:
        *   Lee datos de sensores.
        *   Publica los datos en tópicos MQTT específicos del servidor.
        *   Se suscribe a tópicos MQTT para recibir comandos del servidor.
        *   Actúa sobre los actuadores según los comandos recibidos.
        *   Opcionalmente, publica su estado (registro, heartbeat).
4.  **Base de Datos (SQLite):** Almacena todos los datos persistentes: clientes, datos de sensores, eventos, estados de actuadores, parámetros ideales, estado de la aplicación.
5.  **Frontend (Angular):** Aplicación web que interactúa con la API RESTful del servidor Flask para visualizar datos y controlar el sistema.

## 🛠️ Pila Tecnológica

*   **Backend:** Python 3, Flask
*   **Comunicación:** MQTT (Paho-MQTT)
*   **Base de Datos:** SQLite (con `aiosqlite` para operaciones asíncronas)
*   **Asincronía:** `asyncio` (usado en modelos y cliente MQTT)
*   **Frontend (Servido por Flask):** Angular (requiere build separado)
*   **Broker MQTT:** Mosquitto (recomendado)

## 📁 Estructura del Proyecto

```
.
├── app.py                  # Punto de entrada principal de la aplicación Flask
├── database.py             # Lógica de creación e inicialización de la BD SQLite
├── mqtt_client.py          # Cliente MQTT: conexión, suscripción, manejo de mensajes, lógica automática
├── sensor_data.db          # Archivo de la base de datos SQLite (creado al iniciar, ignorado por Git)
├── requirements.txt        # Dependencias Python del backend
├── docs/                   # Documentación del proyecto
│   ├── README.md           # Este archivo
│   ├── API_DOCUMENTATION.md # Documentación detallada de la API RESTful
│   ├── MSAD_DETAILS.md     # Documentación detallada del módulo MSAD
│   └── ...
├── models/                 # Módulos con lógica de acceso a datos (interacción con BD)
│   ├── __init__.py
│   ├── actuator.py         # Modelo para Actuadores
│   ├── app_state.py        # Modelo para Estado de la Aplicación (manual/auto)
│   ├── client.py           # Modelo para Clientes MQTT
│   ├── event.py            # Modelo para Eventos
│   ├── sensor_data.py      # Modelo para Datos de Sensores y Parámetros Ideales
├── routes/                 # Blueprints Flask para las rutas de la API principal
│   ├── __init__.py
│   ├── actuator_routes.py
│   ├── app_state_routes.py
│   ├── client_routes.py
│   ├── event_routes.py
│   ├── sensor_routes.py
├── msad/                   # Módulo MSAD (Microservicio de Almacenamiento y Datos)
│   ├── __init__.py         # Inicialización, funciones públicas y registro de blueprints MSAD
│   ├── api/                # Blueprints y lógica de las rutas API específicas de MSAD
│   │   ├── __init__.py
│   │   ├── backup_routes.py # Endpoints para gestión de Backups
│   │   ├── report_routes.py # Endpoints para gestión de Reportes
│   │   └── system_routes.py # Endpoints de estado de MSAD
│   ├── config/             # Configuración interna de MSAD (ej: backup_config.json)
│   │   └── ...
│   ├── core/               # Lógica principal de MSAD (backup, reportes, sistema)
│   │   ├── __init__.py
│   │   ├── backup.py       # Funcionalidad de Backup/Restore
│   │   ├── reports.py      # Funcionalidad de Generación de Reportes
│   │   └── system.py       # Utilidades del sistema MSAD (logs, etc.)
│   └── server/             # (Potencialmente para ejecución independiente, verificar uso actual)
├── .gitignore              # Archivos y carpetas ignorados por Git
└── venv/                   # Entorno virtual Python (ignorado por Git)
```
*(Nota: La ruta `ANGULAR_BUILD_FOLDER` en `app.py` debe apuntar a la carpeta `dist/` del build de Angular)*

## 💾 Esquema de la Base de Datos

La base de datos SQLite (`sensor_data.db`) contiene las siguientes tablas principales:

*   `clients`: Información sobre los dispositivos cliente registrados (ID, nombre, estado, etc.).
    *   `client_id` (TEXT, UNIQUE)
    *   `name` (TEXT)
    *   `description` (TEXT)
    *   `last_seen` (TEXT)
    *   `status` (TEXT: 'online', 'offline')
    *   `created_at` (TEXT)
    *   `manually_disabled` (INTEGER)
*   `sht3x_data`: Datos históricos de temperatura y humedad del sensor SHT3x.
    *   `client_id` (TEXT)
    *   `timestamp` (TEXT)
    *   `temperature` (REAL)
    *   `humidity` (REAL)
*   `events`: Registro de eventos importantes del sistema.
    *   `client_id` (TEXT)
    *   `message` (TEXT)
    *   `timestamp` (TEXT)
    *   `topic` (TEXT: 'temperatura', 'humedad', 'actuador', 'sistema', etc.)
*   `actuators`: Estado actual de los actuadores registrados por cliente.
    *   `client_id` (TEXT)
    *   `name` (TEXT: 'Iluminacion', 'Ventilacion', 'Humidificador', 'Motor')
    *   `state` (BOOLEAN)
    *   `timestamp` (TEXT)
*   `ideal_params`: Parámetros ideales (mínimo y máximo) para sensores, usados en modo automático.
    *   `client_id` (TEXT)
    *   `param_type` (TEXT: 'temperatura', 'humedad')
    *   `min_value` (REAL)
    *   `max_value` (REAL)
    *   `timestamp` (TEXT)
*   `app_state`: Modo de operación actual ('manual' o 'automatico') por cliente.
    *   `client_id` (TEXT)
    *   `mode` (TEXT)
    *   `timestamp` (TEXT)

*(Consulte `database.py` para la definición exacta y valores predeterminados)*

## 📡 Comunicación MQTT

La comunicación se basa en tópicos MQTT estructurados. Los nodos cliente deben publicar y suscribirse a los tópicos correctos.

*   **Tópicos a los que se suscribe el Servidor (Nodos publican aquí):**
    *   Datos Sensor SHT3x: `clients/<client_id>/sensor/sht3x`
        *   Payload: `"<temperatura>,<humedad>"` (Ej: `"25.5,85.2"`)
    *   Registro de Cliente: `clients/<client_id>/register`
        *   Payload: `"<nombre>,<descripcion>"` (Ej: `"NodoIncubadora1,RPi con SHT3x"`)
    *   *Otros tópicos posibles (ej: heartbeat, estado actuador) podrían implementarse en los nodos.*
*   **Tópicos en los que publica el Servidor (Nodos se suscriben aquí):**
    *   Control Luz: `clients/<client_id>/light`
        *   Payload: `"true"` / `"false"`
    *   Control Ventilador: `clients/<client_id>/fan`
        *   Payload: `"true"` / `"false"`
    *   Control Humidificador: `clients/<client_id>/humidifier`
        *   Payload: `"true"` / `"false"`
    *   Control Motor: `clients/<client_id>/motor`
        *   Payload: `"true"` / `"false"`

*(Donde `<client_id>` es el identificador único del nodo cliente)*

## ⚙️ Instalación y Configuración

### Requisitos Previos

*   Hardware: Raspberry Pi (o similar) para el servidor, nodos cliente (RPi, ESP32, etc.), sensores (SHT3x), actuadores (relés, etc.), fuentes de alimentación.
*   Sistema Operativo: Raspberry Pi OS (o Linux compatible) en el servidor.
*   Software: Python 3.x, pip, git.
*   Broker MQTT: Mosquitto instalado y funcionando (recomendado `sudo apt install mosquitto mosquitto-clients`).
*   Red: Conexión de red configurada para servidor y nodos.

### Pasos de Configuración del Servidor

1.  **Preparar el Entorno:**
    ```bash
    # Actualizar sistema
sudo apt update && sudo apt upgrade -y

    # Instalar dependencias del sistema (ej: git, python3-pip, python3-venv)
    sudo apt install -y git python3-pip python3-venv i2c-tools

    # (Opcional pero recomendado) Instalar y habilitar Mosquitto localmente
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto
    sudo systemctl start mosquitto
    # Verificar estado: sudo systemctl status mosquitto

    # (Opcional) Configurar Mosquitto (ej: permitir conexiones anónimas para pruebas)
    # sudo nano /etc/mosquitto/conf.d/local.conf
    # -> Añadir: listener 1883
    # -> Añadir: allow_anonymous true
    # sudo systemctl restart mosquitto
    ```
2.  **Clonar y Configurar la Aplicación:**
    ```bash
    # Clonar el repositorio
git clone <url-del-repositorio> raspServerNative
cd raspServerNative

# Crear y activar entorno virtual
    python3 -m venv venv
source venv/bin/activate

    # Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

    # ¡IMPORTANTE! Configurar la ruta del Frontend Angular
    # Edita el archivo app.py
nano app.py 
    # Modifica la variable ANGULAR_BUILD_FOLDER para que apunte a la
    # carpeta 'dist/<nombre-app>' de tu build de Angular.
    # Ejemplo: ANGULAR_BUILD_FOLDER = "/home/pi/raspServerNative/angular_app/dist/mushroom-automation"

    # (Opcional) Configurar la ubicación de la base de datos
    # Edita el archivo database.py si deseas cambiar la ruta
    # nano database.py
    # Modifica la ruta en: conn = sqlite3.connect('/ruta/deseada/sensor_data.db')
    ```
3.  **Configurar Nodos Cliente:**
    *   Programa tus nodos cliente (RPi, ESP32, etc.) para:
        *   Conectarse al broker MQTT (IP o hostname del servidor donde corre Mosquitto).
        *   Usar un `client_id` único.
        *   Publicar datos de sensores y (opcionalmente) estado en los tópicos MQTT correctos (ver [Comunicación MQTT](#-comunicación-mqtt)).
        *   Suscribirse a los tópicos de control de actuadores correspondientes.
4.  **Construir y Desplegar Frontend (Angular):**
    *   Asegúrate de tener Node.js y Angular CLI instalados.
    *   Navega al directorio de tu aplicación Angular.
*   Instala dependencias: `npm install`
    *   Construye la aplicación para producción: `ng build` (o comando similar).
    *   Copia el contenido de la carpeta `dist/<nombre-app>` generada a la ubicación que configuraste en `ANGULAR_BUILD_FOLDER` dentro del proyecto `raspServerNative`.

### Configuración Específica de MSAD

*   La configuración principal de MSAD (directorio de backups, intervalo automático) se gestiona en `msad/config/backup_config.json` (se crea si no existe) y se puede inicializar/modificar vía `app.py` o API.
*   Consulta [MSAD_DETAILS.md](docs/MSAD_DETAILS.md) para detalles sobre configuración avanzada y permisos.

## ▶️ Ejecutar la Aplicación

1.  Navega al directorio raíz del proyecto (`raspServerNative`).
2.  Activa el entorno virtual: `source venv/bin/activate`
3.  Inicia la aplicación Flask: `python app.py`

El servidor se iniciará, escuchando por defecto en `http://0.0.0.0:5000`.

*   **Inicialización:**
    *   Creará las tablas de la base de datos (`sensor_data.db`) si no existen y aplicará valores iniciales (cliente 'mushroom1', parámetros, actuadores).
    *   Se conectará al broker MQTT (configurado en `mqtt_client.py`, por defecto `localhost`).
    *   Inicializará el módulo MSAD (iniciando backups automáticos si está configurado).
*   **Acceso:**
    *   **Interfaz Web Angular:** Abre un navegador y ve a `http://<IP_SERVIDOR>:5000/`.
    *   **API RESTful:** Disponible bajo `http://<IP_SERVIDOR>:5000/api/`.

*(Reemplaza `<IP_SERVIDOR>` con la dirección IP de la Raspberry Pi donde corre el servidor).*

### Ejecución como Servicio (systemd - Opcional)

Para que la aplicación se ejecute automáticamente al inicio y se reinicie en caso de fallo, puedes configurarla como un servicio `systemd`.

1.  Crea un archivo de servicio: `sudo nano /etc/systemd/system/raspserver.service`
2.  Pega el siguiente contenido, **ajustando `User`, `Group`, `WorkingDirectory` y `ExecStart`** a tu configuración específica:

    ```ini
    [Unit]
    Description=RaspServer Flask Application for Mushroom Control
    After=network.target mosquitto.service # Asegura que la red y MQTT estén listos

    [Service]
    User=pi # Cambia 'pi' por tu usuario
    Group=pi # Cambia 'pi' por tu grupo
    WorkingDirectory=/home/pi/raspServerNative # Ruta absoluta a tu proyecto
    Environment="PATH=/home/pi/raspServerNative/venv/bin" # Ruta al bin del venv
    ExecStart=/home/pi/raspServerNative/venv/bin/python app.py # Ruta absoluta a python dentro del venv y a app.py
    Restart=always # Reiniciar siempre si falla
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```
3.  Habilita e inicia el servicio:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable raspserver
    sudo systemctl start raspserver
    sudo systemctl status raspserver # Verifica que esté corriendo
    # Para ver logs: sudo journalctl -u raspserver -f
    ```

## 📚 Documentación Adicional

*   **API RESTful Detallada:** Consulta [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) para ver todos los endpoints, parámetros, ejemplos de solicitud/respuesta.
*   **Módulo MSAD:** Consulta [MSAD_DETAILS.md](docs/MSAD_DETAILS.md) para entender la configuración avanzada, funcionamiento interno y solución de problemas específicos de backups y reportes.

## 🔑 Módulos Clave

*   **`app.py`:** Orquestador principal. Inicializa Flask, registra blueprints, configura CORS, sirve el frontend, inicia MQTT y MSAD, maneja el ciclo de vida.
*   **`database.py`:** Define el esquema de la base de datos y la lógica de inicialización.
*   **`mqtt_client.py`:** Gestiona toda la lógica MQTT: conexión al broker, suscripciones dinámicas, procesamiento de mensajes entrantes (sensores, registro), publicación de comandos a actuadores (especialmente en modo automático), manejo de reconexiones, y uso de `asyncio` para operaciones no bloqueantes.
*   **`models/*.py`:** Capa de acceso a datos. Contiene funciones (muchas `async`) para interactuar con las tablas de la base de datos SQLite (CRUD).
*   **`routes/*.py`:** Define los endpoints de la API RESTful principal usando Blueprints de Flask.
*   **`msad/`:** Módulo autónomo encapsulado para la gestión de datos (backups, reportes). Ver [MSAD_DETAILS.md](docs/MSAD_DETAILS.md).

## 🐛 Resolución de Problemas

1.  **Error de conexión MQTT:**
    *   Verifica que `mosquitto` esté activo (`sudo systemctl status mosquitto`).
    *   Confirma que la IP/hostname del broker en `mqtt_client.py` (si no es `localhost`) y en los nodos cliente sea correcta y accesible.
    *   Revisa firewalls (`sudo ufw status`) en el servidor (puerto 1883 TCP debe estar permitido).
    *   Usa `mosquitto_sub -h <BROKER_IP> -t "#" -v` para depurar mensajes en el broker.
2.  **Sensor SHT3X no detectado/lee:**
    *   Verifica conexiones físicas (SDA, SCL, VCC, GND).
    *   Asegúrate de que I2C esté habilitado en el nodo (`sudo raspi-config` si es RPi).
    *   Ejecuta `i2cdetect -y 1` en el nodo para ver si se detecta (dirección 0x44 o 0x45).
3.  **API / Interfaz Web inaccesible:**
    *   Confirma que `app.py` o el servicio `raspserver` esté corriendo (`python app.py` o `sudo systemctl status raspserver`).
    *   Revisa los logs de la aplicación por errores (`sudo journalctl -u raspserver -f` si usas systemd).
    *   Verifica que usas la IP correcta del servidor en el navegador.
    *   Revisa el firewall del servidor (puerto 5000 TCP debe estar permitido).
4.  **Problemas con Base de Datos (`sensor_data.db`):**
    *   Verifica permisos de archivo/directorio. El usuario que ejecuta `app.py` necesita escribir en el archivo y su directorio. La ruta por defecto está en `database.py`.
    *   Si sospechas corrupción, considera restaurar desde un backup MSAD o (como último recurso) elimina `sensor_data.db` (¡perderás datos!) para que se recree al reiniciar `app.py`.
5.  **MSAD no funciona (Backups/Reportes):**
    *   Verifica los permisos de escritura en el directorio configurado para backups/reportes (ver `msad/config/backup_config.json` o `MSAD_DETAILS.md`).
    *   Consulta los logs de la aplicación para errores específicos de MSAD.

## 📞 Soporte

Para problemas, preguntas o sugerencias, por favor abre un **Issue** en el repositorio de GitHub del proyecto.