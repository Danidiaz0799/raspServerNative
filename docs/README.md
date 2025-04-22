# 🍄 RaspServer: Sistema de Control Ambiental para Cultivo de Hongos

![Versión](https://img.shields.io/badge/versión-1.0.0-blue) <!-- Ajustar si necesario -->
![Estado](https://img.shields.io/badge/estado-activo-green)
![Licencia](https://img.shields.io/badge/licencia-MIT-orange) <!-- Verificar licencia real -->

## 📋 Contenido
- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Sistema Electrónico](#sistema-electrónico)
- [Cultivo de Orellana Rosada](#cultivo-de-orellana-rosada)
- [Módulo MSAD (Microservicio de Almacenamiento y Datos)](#módulo-msad-microservicio-de-almacenamiento-y-datos)
- [Pila Tecnológica](#pila-tecnológica)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecutar la Aplicación](#ejecutar-la-aplicación)
- [Comunicación MQTT](#comunicación-mqtt)
- [Documentación de la API](#documentación-de-la-api)
- [Documentación Detallada de MSAD](#documentación-detallada-de-msad)
- [Módulos Clave](#módulos-clave)
- [Resolución de Problemas](#resolución-de-problemas)
- [Actualización del Sistema](#actualización-del-sistema)
- [Soporte](#soporte)

## 📝 Descripción

RaspServer automatiza y monitorea las condiciones ambientales óptimas para el cultivo de hongos, utilizando una Raspberry Pi como servidor central. Interactúa con clientes MQTT (que pueden ser otras Raspberry Pi, ESP32, u otros microcontroladores) para recibir datos de sensores y controlar actuadores. Incluye una interfaz web (Angular) y un **módulo integrado MSAD** para gestión avanzada de datos.

**Objetivos:**
- Ser energéticamente eficiente.

## 🏗️ Arquitectura

**Flujo de datos:**
6.  El **módulo MSAD integrado** realiza backups periódicos de la base de datos y permite generar/descargar reportes de datos históricos vía API.

## 🔌 Sistema Electrónico

## 🍄 Cultivo de Orellana Rosada (*Pleurotus djamor*)

## 📊 Módulo MSAD (Microservicio de Almacenamiento y Datos)

RaspServer integra el módulo MSAD, diseñado para la gestión eficiente de los datos generados por el sistema de cultivo.

**Capacidades Principales:**
*   **Backups:** Realiza copias de seguridad automáticas (programables) y manuales de la base de datos principal (`sensor_data.db`). Permite listar, descargar, restaurar y eliminar estos backups a través de la API.
*   **Reportes:** Genera reportes de datos históricos (sensores, eventos, actuadores) en formatos JSON o CSV, filtrados por cliente, rango de fechas y tipo de dato. Permite listar y descargar los reportes generados.

Para una descripción detallada de la arquitectura interna, funcionalidades completas, configuración avanzada y solución de problemas específicos de MSAD, consulta el documento:
**[MSAD_DETAILS.md](MSAD_DETAILS.md)**

## ��️ Pila Tecnológica

## 📁 Estructura del Proyecto

```
.
├── app.py                  # Punto de entrada principal de la aplicación Flask
├── database.py             # Lógica de creación de tablas de la base de datos
├── mqtt_client.py          # Cliente MQTT para comunicación con dispositivos y control
├── sensor_data.db          # Archivo de la base de datos SQLite (ignorado por Git)
├── requirements.txt        # Dependencias de Python para el servidor
├── README.md               # Este archivo
├── API_DOCUMENTATION.md    # Documentación detallada de la API RESTful
├── MSAD_DETAILS.md         # Documentación detallada del módulo MSAD
├── .gitignore              # Archivos y carpetas ignorados por Git
├── angular_app/            # Código fuente y build de la aplicación Angular
│   ├── dist/               # Carpeta de build de Angular (servida por Flask, ignorada por Git)
│   └── ...                 # Otros archivos de Angular (package.json, src/, etc.)
├── models/                 # Módulos para interactuar con la base de datos (tablas)
│   ├── ... (actuator.py, client.py, etc.)
├── routes/                 # Blueprints de Flask para las rutas principales de la API
│   ├── ... (actuator_routes.py, client_routes.py, etc.)
├── msad/                   # Módulo del Microservicio de Almacenamiento Distribuido
│   ├── __init__.py         # Inicialización y registro de blueprints MSAD
│   ├── api/                # Blueprints y lógica de las rutas API de MSAD
│   │   ├── backup_routes.py, report_routes.py, system_routes.py
│   ├── config/             # Configuración de MSAD
│   └── core/               # Lógica principal de MSAD (backup, reportes, sistema)
└── __pycache__/            # Archivos de caché de Python (ignorados por Git)
```
*(Nota: La existencia de código específico para nodos debe verificarse en el repositorio real)*

## ⚙️ Instalación y Configuración

### Requisitos Previos
*   Hardware ensamblado (Servidor RPi, Nodos, Sensores, Actuadores, Fuentes de alimentación).
*   Sistema Operativo instalado en la Raspberry Pi del servidor (Raspberry Pi OS Lite 64-bit recomendado).
*   Conexión de red configurada para el servidor y los nodos.
*   Broker MQTT instalado y funcionando (Mosquitto recomendado).

### 1. Preparación de la Raspberry Pi (Servidor y Nodos si son RPi)
    ```bash
# Acceder por SSH o terminal
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar paquetes esenciales
sudo apt install -y git python3-pip python3-venv mosquitto mosquitto-clients i2c-tools

# (Opcional pero recomendado) Dependencias para librerías científicas/imagen
# sudo apt install -y libopenjp2-7 libatlas-base-dev

# Habilitar interfaces necesarias (ej. I2C para SHT3x, Serial para MH-Z19)
sudo raspi-config
# Ir a 'Interface Options' y habilitar I2C, Serial Port (deshabilitar login shell, habilitar hardware serial).
# Reiniciar si es necesario.

# Verificar I2C (debería detectar el SHT3X en 0x44 o 0x45 si está conectado)
i2cdetect -y 1
```

### 2. Configuración del Servidor Central (Raspberry Pi)
    ```bash
# Clonar el repositorio (ajusta la URL)
git clone <url-del-repositorio> raspServerNative
cd raspServerNative

# Crear y activar entorno virtual
    python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt

# Configurar Broker MQTT (si se usa el local)
# Puedes editar /etc/mosquitto/mosquitto.conf o añadir config en /etc/mosquitto/conf.d/
# Asegúrate de permitir conexiones anónimas o configura usuarios si es necesario.
# Ejemplo: Añadir 'allow_anonymous true' a un archivo .conf en conf.d
# sudo nano /etc/mosquitto/conf.d/local.conf
# Contenido:
# listener 1883
# allow_anonymous true
# Reiniciar Mosquitto
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto # Para que inicie automáticamente

# Ajustar la ruta de Angular en app.py ¡IMPORTANTE!
nano app.py 
# Modificar la variable ANGULAR_BUILD_FOLDER para que apunte a la carpeta dist/ correcta de tu build de Angular.

# (Opcional) Configurar como servicio systemd para ejecución automática
# Crear un archivo de servicio (ej. /etc/systemd/system/raspserver.service)
# sudo nano /etc/systemd/system/raspserver.service
# Contenido Ejemplo:
# [Unit]
# Description=RaspServer Flask Application
# After=network.target mosquitto.service
# 
# [Service]
# # ¡IMPORTANTE! Ajusta User y WorkingDirectory a tu configuración
# User=pi 
# WorkingDirectory=/home/pi/raspServerNative 
# ExecStart=/home/pi/raspServerNative/venv/bin/python app.py
# Restart=always
# Environment="PATH=/home/pi/raspServerNative/venv/bin"
# 
# [Install]
# WantedBy=multi-user.target

# Habilitar e iniciar el servicio
# sudo systemctl daemon-reload
# sudo systemctl enable raspserver
# sudo systemctl start raspserver
# sudo systemctl status raspserver # Para verificar
```

### 3. Configuración de Nodos Cliente
*   **Si el nodo es otra Raspberry Pi:** Sigue pasos similares a la preparación del servidor, instala dependencias específicas del nodo (si hay un `requirements-node.txt`) y configura un script/servicio para que publique datos MQTT al broker central.
*   **Si el nodo es un ESP32/Arduino:** Flashea el código correspondiente (no incluido en este repositorio backend) configurado con la IP/hostname del broker MQTT y los tópicos correctos.
    *   **Nota Importante:** Evita quemar (hardcode) la dirección IP o el hostname del broker directamente en el código del nodo si es posible. Considera métodos de configuración (ej. WiFiManager en ESP) o descubrimiento (mDNS/Bonjour si tu red lo soporta y el nodo es compatible) para mayor flexibilidad. Si usas un nombre `.local` como `raspserver.local`, asegúrate que tanto el servidor como el nodo estén en la misma red y soporten resolución mDNS.

### 4. Construcción del Frontend (Angular)
*   Navega al directorio `angular_app/`.
*   Instala dependencias: `npm install`
*   Construye la aplicación: `ng build` (o el comando específico de tu proyecto Angular).
*   **Verifica que la carpeta de salida** (ej. `angular_app/dist/nombre-app`) **coincida exactamente** con la ruta configurada en `ANGULAR_BUILD_FOLDER` dentro de `app.py`.

### 5. Configuración Específica de MSAD (Opcional)
*   La configuración básica de MSAD (como la activación de backups automáticos) se puede gestionar al iniciar `app.py` o mediante su API.
*   Consulta [MSAD_DETAILS.md](MSAD_DETAILS.md) para detalles sobre permisos de directorios y configuración avanzada.

## ▶️ Ejecutar la Aplicación

Si **NO** configuraste el servicio `systemd`, puedes ejecutar manualmente:

1.  Navega al directorio raíz del proyecto (`raspServerNative`).
2.  Activa el entorno virtual: `source venv/bin/activate`
3.  Inicia la aplicación: `python app.py`

El servidor Flask se iniciará (por defecto en `http://0.0.0.0:5000`).
*   Accede a la **Interfaz Web Angular** desde `http://raspserver.local:5000/`.
*   La **API RESTful** está disponible bajo `http://raspserver.local:5000/api`. Consulta [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para detalles.
*   El cliente MQTT intentará conectarse al broker (configurado por defecto en `localhost`, revisa `mqtt_client.py` si necesitas cambiarlo).
*   MSAD se inicializará (backups automáticos si están habilitados en `app.py` o vía API).

## �� Comunicación MQTT

La comunicación entre el servidor y los nodos se realiza vía MQTT. Los tópicos listados abajo son los usados por defecto en el servidor, asegúrate que el código de tus nodos cliente utilice los mismos.

*   **Publicación de Datos del Nodo al Servidor:**
    *   Sensor SHT3x: `clients/<client_id>/sensor/sht3x` (Payload JSON: `{ "temperature": 25.5, "humidity": 85.2 }`)
    *   Estado/Heartbeat: `clients/<client_id>/status/heartbeat` (Payload: "online" o JSON con info)
    *   Registro inicial: `clients/<client_id>/register` (Payload JSON: `{ "device_type": "RPi-Node", "location": "Incubadora1" }`)
*   **Publicación de Comandos del Servidor al Nodo:**
    *   Control Actuador: `clients/<client_id>/actuator/<actuator_name>/set` (Payload: "on", "off", "toggle", o valor numérico para PWM)
*   **Publicación de Estado del Actuador (Confirmación del Nodo al Servidor):**
    *   `clients/<client_id>/actuator/<actuator_name>/state` (Payload: "on", "off", o valor actual)

*(`<client_id>` debe ser único para cada nodo; `<actuator_name>` ej: "light", "fan", "humidifier")*

## 📚 Documentación de la API

Para una descripción detallada de **todos** los endpoints de la API RESTful (incluyendo los de MSAD), consulta:
**[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## 📄 Documentación Detallada de MSAD

Para profundizar en el funcionamiento interno, configuración avanzada y funcionalidades específicas del módulo MSAD, consulta:
**[MSAD_DETAILS.md](MSAD_DETAILS.md)**

## 🔑 Módulos Clave

*   **`app.py`:** Orquesta la aplicación Flask, registra Blueprints, inicializa MQTT y MSAD, sirve el frontend Angular.
*   **`mqtt_client.py`:** Gestiona la lógica MQTT (conexión, suscripción, publicación, procesamiento de mensajes, control automático).
*   **`database.py` / `models/*.py`:** Creación de tablas y funciones de acceso a datos (muchas asíncronas con `aiosqlite`).
*   **`routes/*.py`:** Endpoints de la API principal.
*   **`msad/`:** Módulo integrado para backups, reportes y sus APIs. Ver [MSAD_DETAILS.md](MSAD_DETAILS.md).

## 🐛 Resolución de Problemas

1.  **Error de conexión MQTT:**
    *   Verifica que el servicio Mosquitto esté activo en el servidor: `sudo systemctl status mosquitto`.
    *   Comprueba la configuración del broker (IP/hostname) en el servidor (`mqtt_client.py`, por defecto `localhost`) y en los nodos cliente (deben apuntar a la IP o hostname `.local` del servidor, ej. `raspserver.local`).
    *   Revisa las reglas de firewall (ej. `sudo ufw status`) si UFW está activo. Asegúrate de que el puerto 1883 (o el configurado) esté abierto.
    *   Usa `mosquitto_sub -h <broker_ip> -t "#" -v` (reemplaza `<broker_ip>` por la IP o hostname del servidor) para ver si los mensajes llegan al broker.
2.  **Sensor SHT3X no detectado o no lee:**
    *   Verifica las conexiones físicas (SDA, SCL, VCC, GND).
    *   Asegúrate de que I2C esté habilitado (`sudo raspi-config`).
    *   Ejecuta `i2cdetect -y 1` para ver si el dispositivo aparece (dirección 0x44 o 0x45).
    *   Revisa los logs del script/servicio que lee el sensor en el nodo.
3.  **API/Interfaz Web inaccesible:**
    *   Verifica que la aplicación Flask (`app.py`) esté ejecutándose (manualmente o vía `systemd status raspserver`).
    *   Comprueba la salida de `python app.py` por errores.
    *   Asegúrate de estar usando la IP correcta o el hostname `.local` (ej. `raspserver.local`) de la Raspberry Pi del servidor en la URL del navegador.
    *   Verifica el firewall si está activo.
4.  **Problemas con la base de datos (`sensor_data.db`):**
    *   Comprueba los permisos del archivo `sensor_data.db` y el directorio que lo contiene. El usuario que ejecuta `app.py` debe tener permisos de lectura/escritura.
    *   Si la base de datos está corrupta (raro, pero posible tras cortes de energía), considera restaurar desde un backup de MSAD o eliminar el archivo `.db` (¡perderás todos los datos!) para que se cree de nuevo al iniciar `app.py`.

## 🔄 Actualización del Sistema

```bash
# Navega al directorio del proyecto
cd ~/raspServerNative # O la ruta donde lo clonaste

# Detén el servicio si está corriendo
# sudo systemctl stop raspserver

# Descarga los últimos cambios desde Git
git pull origin main # O la rama que uses

# Activa el entorno virtual
source venv/bin/activate

# Actualiza las dependencias
pip install -r requirements.txt

# (Opcional) Reconstruye el frontend si hubo cambios
# cd angular_app && npm install && ng build && cd ..

# (Opcional) Ejecuta scripts de migración de base de datos si existen

# Reinicia el servicio o la aplicación
# sudo systemctl start raspserver
# O manualmente: python app.py
```

## 🆘 Soporte

*   **Documentación API:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
*   **Issues/Problemas:** Registrar en [Issues del Repositorio GitHub](issues)
*   **Contacto:** danidiaz0799@gmail.com

---

<div align="center">
  <p>Desarrollado para cultivos inteligentes.</p>
</div>