# Sistema de Gestión Centralizada de Datos y Control Ambiental para Múltiples Cultivos de Orellana Rosada con Módulo de Almacenamiento y Datos (MSAD)

## 2.1 Planteamiento del Problema

La producción de setas Orellana Rosada (*Pleurotus djamor*), especialmente cuando se realiza en **múltiples unidades de cultivo distribuidas o se busca escalar la producción**, enfrenta **importantes desafíos** para monitorear y controlar el ambiente de forma precisa. Un problema clave es la **falta de sistemas integrados** que puedan gestionar y coordinar las condiciones de cada unidad desde un punto central. A menudo, los productores utilizan **métodos manuales o herramientas separadas**, lo que hace difícil mantener constantes las variables ambientales importantes (temperatura, humedad, CO₂). Esta **falta de uniformidad** puede reducir la producción y la calidad, y además **dificulta la supervisión general y el buen funcionamiento**, limitando la capacidad de **crecer de forma competitiva y sostenible**.

Si bien las tecnologías del Internet de las Cosas (IoT) proporcionan **buenas herramientas** para la automatización, su aplicación práctica para el **manejo conjunto de varios entornos de cultivo** a pequeña o mediana escala suele encontrar obstáculos como el **costo, la dificultad para integrar sistemas** y la **falta de ayuda técnica adecuada**. **Se necesita claramente una solución integrada y fácil de usar** que permita **recoger, procesar y mostrar datos de diferentes puntos de cultivo**, ayudando a tomar decisiones y controlar todo desde un solo lugar, pero respetando las necesidades de cada cultivo individual. La falta de un sistema que ofrezca de forma práctica esta **interconexión (usando MQTT), gestión individual por cultivo (`client_id`), visualización centralizada (interfaz web) y una gestión fiable de datos (mediante un Módulo de Almacenamiento y Datos - MSAD - para backups y reportes)**, dificulta el uso eficiente de los recursos y pone en riesgo la **posibilidad de crecer de forma rentable y sostenible** en la producción de esta especie de hongo.

## 3. Estado del Arte

El cultivo de setas en Entornos Agrícolas Controlados (CEA - Controlled Environment Agriculture) ha ganado relevancia debido a su eficiencia y capacidad para producir alimentos de alto valor. Sin embargo, el éxito de estos cultivos, como el de Orellana Rosada (*Pleurotus djamor*), depende críticamente del mantenimiento preciso de variables ambientales (temperatura, humedad, CO₂, iluminación). La tecnología de Internet de las Cosas (IoT) se ha posicionado como una herramienta fundamental para abordar estos desafíos, permitiendo la automatización y optimización de las condiciones de cultivo [2], [6].

### 3.1 Automatización y Monitorización Ambiental Basada en IoT

Una aplicación central del IoT en fungicultura y agricultura de precisión es la monitorización continua y la automatización del control ambiental. Diversos estudios y revisiones demuestran la viabilidad y beneficios de usar redes de sensores inalámbricos y actuadores conectados para mantener las condiciones óptimas de forma autónoma [6]. Sistemas basados en microcontroladores (como NodeMCU en [5]) o miniordenadores (Raspberry Pi) conectados a sensores ambientales permiten recopilar datos en tiempo real. Estos datos, a su vez, activan actuadores (ventiladores, humidificadores, luces, sistemas de riego) mediante relés o controladores PWM para ajustar el ambiente según umbrales predefinidos o algoritmos de control [4]. El uso de protocolos ligeros como **MQTT** es común y efectivo en estas arquitecturas para la comunicación eficiente entre dispositivos [3], [5], aspecto clave abordado en el Objetivo Específico 1. Esta automatización reduce el error humano, asegura consistencia y libera al productor de la supervisión manual constante. Implementaciones específicas para el cultivo de setas han sido reportadas, demostrando sistemas inteligentes que utilizan sensores IoT [8], [9].

### 3.2 Gestión Centralizada y Monitorización Remota

Más allá del control local, una tendencia clave en 'Smart Farming' es la **centralización de la gestión y la monitorización remota** [2], especialmente relevante cuando se manejan **múltiples unidades de cultivo distribuidas**. Plataformas basadas en la nube o servidores locales permiten agregar datos de diversos puntos, ofrecer una visión global del estado de los cultivos y facilitar el control remoto a través de interfaces web o móviles [6]. Esto responde a la necesidad de escalar la producción manteniendo un control efectivo. **Este proyecto** se alinea con esta tendencia al proponer un **servidor central (Raspberry Pi) que gestiona múltiples nodos cliente (`client_id`)** (Objetivo Específico 2) y ofrece una **interfaz web (Angular) para visualización y control unificado** (Objetivo Específico 3).

### 3.3 Gestión de Datos, Reportes y Backups

Con la monitorización continua se genera un volumen significativo de datos históricos. La capacidad de almacenar, procesar y analizar estos datos es crucial para entender patrones, optimizar parámetros y tomar decisiones informadas. Aunque muchas plataformas IoT incluyen funcionalidades para la **generación de reportes y visualización de históricos** [6], la **gestión robusta de estos datos, incluyendo backups periódicos y mecanismos de restauración fiables**, es un aspecto fundamental para la integridad y disponibilidad de la información a largo plazo, el cual no siempre se detalla explícitamente en las implementaciones revisadas. El **módulo MSAD** integrado en este proyecto aborda específicamente esta necesidad (Objetivo Específico 4), proporcionando una solución local para backups automáticos/manuales y generación de reportes, diferenciándose de sistemas que dependen exclusivamente de servicios en la nube o carecen de estas funcionalidades explícitas de gestión de datos resiliente.

### 3.4 Aplicación de Analítica Avanzada (Machine Learning)

Un área emergente y de gran potencial es la integración de técnicas de Machine Learning (ML) en los sistemas IoT agrícolas [1]. Algunos sistemas utilizan ML para análisis predictivo (predecir rendimientos, detectar enfermedades tempranamente), optimización de parámetros de control basados en datos históricos [10], o incluso clasificación de imágenes. La revisión de Sarkar et al. [1] destaca las diversas aplicaciones de ML en 'Smart Agriculture'. Si bien **el presente proyecto** actual se centra en el monitoreo, control y gestión de datos fundamentales, la arquitectura implementada con almacenamiento estructurado sienta las bases para futuras integraciones de ML si se requiere un análisis más avanzado.

### 3.5 Desafíos de Adopción: Costo, Usabilidad y Sostenibilidad

A pesar de los beneficios, la adopción de IoT en la agricultura, especialmente por pequeños y medianos productores, enfrenta barreras. El **costo inicial** de sensores, actuadores y plataformas puede ser un factor limitante [7]. La **complejidad técnica** y la necesidad de **infraestructura de red estable** también son desafíos reconocidos. Por ello, existe una demanda de **soluciones IoT más accesibles, modulares y fáciles de usar**, como las que proponen sistemas de bajo costo [7], que no requieran conocimientos técnicos profundos. **Este proyecto** busca contribuir en esta línea utilizando hardware accesible (Raspberry Pi) y software de código abierto. La sostenibilidad operativa, mediante la integración de energías renovables, también se explora en la literatura, aunque no es un foco actual de este proyecto.

### 3.6 Conclusión del Estado del Arte y Posicionamiento del Proyecto

En resumen, el estado del arte en monitorización y control de cultivos mediante IoT [2], [6] muestra avances significativos en automatización [4], [5], [8], [9], comunicación vía MQTT [3], [5], y la aplicación creciente de ML [1], [10]. Sin embargo, persisten desafíos importantes relacionados con el **costo [7], la complejidad de integración, la usabilidad para no expertos y, crucialmente, la gestión eficiente, robusta y local de datos (backups/restauración) en sistemas distribuidos**.

Este proyecto se posiciona dentro de este contexto abordando directamente la necesidad de un **sistema integrado, accesible y escalable para la gestión centralizada de múltiples unidades de cultivo de Orellana Rosada**. Utiliza tecnologías estándar y de relativo bajo costo (Raspberry Pi, MQTT, Python/Flask, Angular) y se diferencia al incorporar el **módulo MSAD**, que provee funcionalidades esenciales para la **gestión local y fiable de backups y la generación de reportes históricos**, contribuyendo a la robustez y utilidad del sistema para el productor a largo plazo. Busca ofrecer una solución práctica y bien documentada que facilite la adopción tecnológica en este sector específico.

## 4. Marco de Referencia

### 4.1 Marco Teórico

El marco teórico de este proyecto fundamenta los aspectos electrónicos y biológicos necesarios para el diseño e implementación de un sistema IoT distribuido para el cultivo in-door de setas Orellana Rosada. Este cultivo requiere un control preciso de condiciones ambientales, como temperatura y humedad, para optimizar su producción y calidad. El presente documento desarrolla las bases tecnológicas y técnicas que sustentan el proyecto.

#### 4.1.1 Características del Cultivo de Setas Orellana Rosada
La *Pleurotus djamor*, conocida como seta Orellana Rosada, es un hongo valorado por su alto contenido nutricional y su aplicación en la industria alimentaria. Requiere condiciones específicas para garantizar un crecimiento óptimo:
*   **Rango de Temperatura:** 22-28 °C. La temperatura afecta directamente el desarrollo micelial y la fructificación.
*   **Humedad Relativa:** 85-95%. Es fundamental para evitar deshidratación y promover un desarrollo uniforme.
*   **Sustrato:** Comúnmente compuesto por mezclas lignocelulósicas (paja de trigo, aserrín), esterilizado para evitar contaminación.
*   **Luz:** Aunque no realizan fotosíntesis, necesitan niveles bajos de luz difusa para estimular la fructificación.

Cualquier desviación en estas condiciones puede reducir la calidad del cultivo, incrementar el desperdicio o afectar negativamente la productividad. Por ello, un sistema automatizado distribuido es clave para mantener estas variables bajo control en múltiples cultivos simultáneamente.

#### 4.1.2 Componentes Electrónicos Fundamentales
El sistema electrónico está compuesto por una red de Raspberry Pis que actúan como clientes y servidor, junto con sensores y actuadores que interactúan mediante una red IoT para medir y ajustar las variables ambientales.

**Sensores:**
1.  **SHT3x:**
    *   Sensor digital de alta precisión.
    *   Mide temperatura (-40 a 125°C) y humedad relativa (0-100%).
    *   Precisión de temperatura: ±0.3°C.
    *   Precisión de humedad: ±2%.
    *   Interfaz I2C.

**Actuadores:**
1.  **Ventiladores:**
    *   Regulan la circulación de aire y/o renovación (CO₂).
    *   Control mediante GPIO de Raspberry Pi (directo, relé o driver).
2.  **Humidificadores:**
    *   Generan niebla ultrafina para mantener la humedad.
    *   Control mediante GPIO de Raspberry Pi (generalmente vía relé).
3.  **Iluminación LED:**
    *   Control de intensidad lumínica o ciclo ON/OFF.
    *   Manejo mediante GPIO de Raspberry Pi (relé o driver/MOSFET).

**Plataforma de Control:**
1.  **Raspberry Pi Cliente (Nodo):**
    *   Modelo: Raspberry Pi 3B+ (u otros modelos/microcontroladores compatibles con MQTT).
    *   Sistema Operativo: Raspberry Pi OS (o firmware específico si es ESP/Arduino).
    *   Funciones:
        *   Lectura de sensores (ej. vía I2C).
        *   Control de actuadores (ej. vía GPIO).
        *   Cliente MQTT para comunicación con servidor.
        *   Identificación única por cultivo (`client_id`).
2.  **Raspberry Pi Servidor Central:**
    *   Modelo: Raspberry Pi 3B+ (o superior recomendado).
    *   Sistema Operativo: Raspberry Pi OS.
    *   Funciones:
        *   Broker MQTT central (ej. Mosquitto).
        *   Servidor web (Flask) para API y frontend.
        *   Base de datos (SQLite) para almacenamiento de datos históricos.
        *   Gestión de múltiples clientes (`client_id`).
        *   **Ejecución del Módulo de Almacenamiento y Datos (MSAD)** para backups y reportes.

#### 4.1.3 Arquitectura de Comunicación

**Protocolo MQTT:**
1.  **Roles:**
    *   **Clientes (Nodos):** Raspberry Pis (u otros dispositivos) en cada cultivo que publican datos de sensores y estados, y se suscriben a comandos de actuadores.
    *   **Servidor (Broker):** Instancia central de Mosquitto (u otro broker MQTT) que gestiona la comunicación publicador/suscriptor entre todos los nodos y el servidor de aplicación.
    *   **Servidor (Aplicación):** La aplicación Flask actúa también como cliente MQTT, suscribiéndose a los datos de los nodos y publicando comandos.
2.  **Tópicos (Ejemplo de estructura):**
    *   Publicación de datos: `sensor/[id_cultivo]/temperatura`, `sensor/[id_cultivo]/humedad`, `sensor/[id_cultivo]/luz`, `estado/[id_cultivo]`
    *   Publicación de comandos: `actuador/[id_cultivo]/[dispositivo]/set` (Payload: "ON", "OFF", valor)
    *   Publicación de estado actuador: `actuador/[id_cultivo]/[dispositivo]/state` (Payload: "ON", "OFF", valor)

*(Nota: Asegurar que esta estructura de tópicos coincida con la implementación final o la descrita en el README)*

**Flujo de Datos:**
1.  Cada **Nodo Cliente**:
    *   Lee datos de sus sensores periódicamente.
    *   Publica las lecturas en sus tópicos MQTT específicos (`sensor/...`, `estado/...`).
    *   Se suscribe y escucha comandos en sus tópicos de actuador (`actuador/.../set`).
    *   (Opcional) Publica el estado actual de sus actuadores (`actuador/.../state`).
2.  **Servidor Central (Aplicación Flask/MQTT Client):**
    *   Se suscribe a los tópicos de datos de todos los clientes (`sensor/+/...`, `estado/+/...`).
    *   Recibe los datos, los procesa y los almacena en la base de datos.
    *   Se suscribe a los estados de los actuadores (si los nodos los publican).
    *   Publica comandos en los tópicos de actuador (`actuador/.../set`) basado en la lógica de control (automática o manual desde la API/web).
    *   Sirve la interfaz web y la API RESTful para monitoreo y control.
    *   Interactúa con el **módulo MSAD** para operaciones de backup y reporte.

#### 4.1.4 Impacto del Sistema Distribuido
*   **Gestión Centralizada:**
    *   Control unificado de múltiples cultivos desde una única interfaz.
    *   Monitoreo en tiempo real del estado agregado de todas las instalaciones.
    *   Optimización del uso de recursos humanos y técnicos.
*   **Escalabilidad:**
    *   Facilidad para añadir nuevos nodos/cultivos al sistema existente.
    *   Arquitectura modular que permite adaptaciones y expansiones.
    *   Mantenimiento potencialmente simplificado al centralizar la lógica principal.
*   **Eficiencia Operativa:**
    *   Reducción de costos asociados a la supervisión manual individualizada.
    *   Optimización del consumo de recursos (energía, agua) mediante control preciso.
    *   Mejora potencial en la calidad y consistencia del producto final a través de condiciones ambientales estables.

### 4.2 Marco Legal

*(Esta sección se incluye tal como la proporcionaste, asumiendo que es adecuada para tu contexto. Si necesitas ajustes específicos para Colombia u otra región, házmelo saber.)*

El marco legal de este proyecto asegura que el sistema IoT distribuido para el cultivo de setas Orellana Rosada cumpla con los estándares de calidad, seguridad y sostenibilidad necesarios.

#### 4.2.1 Normas de Calidad y Seguridad

**Normas Internacionales:**
*   ISO/IEC 27001: Gestión de seguridad de la información en sistemas IoT.
*   IEEE 802.11: Estándares para redes inalámbricas (aplicable a nodos WiFi).
*   MQTT v3.1.1/v5.0: Especificaciones del protocolo de comunicación IoT utilizado.

**Normas Nacionales (Ejemplo Colombia):**
*   RETIE: Reglamento Técnico de Instalaciones Eléctricas (para seguridad de instalaciones).
*   Resolución CRC 5050 de 2016: Regulación de redes y servicios de telecomunicaciones (uso del espectro, etc.).
*   Ley 1581 de 2012: Protección de datos personales (si el sistema maneja datos de usuarios).

**Normativas Específicas Aplicables al Sistema:**
*   **Seguridad de Datos:**
    *   Consideraciones sobre encriptación en comunicaciones MQTT (ej. TLS).
    *   Métodos de autenticación de dispositivos cliente en el broker MQTT.
    *   Protección de datos almacenados en la base de datos y backups.
*   **Seguridad Eléctrica:**
    *   IEC 60950-1 / IEC 62368-1: Normas de seguridad para equipos de tecnología de la información y comunicaciones.
    *   Implementación de protecciones contra sobretensiones.
    *   Uso de fuentes de alimentación certificadas y aislamiento eléctrico adecuado entre bajo voltaje (RPi) y alto voltaje (actuadores).
*   **Sostenibilidad:**
    *   Consideraciones sobre eficiencia energética de los dispositivos seleccionados.
    *   Gestión responsable de recursos (agua, energía para actuadores).
    *   Minimización del impacto ambiental (gestión de residuos electrónicos al final de vida útil).

Este marco legal orienta una implementación segura y eficiente del sistema, buscando cumplir con las normativas relevantes mientras se mantiene la flexibilidad necesaria para la funcionalidad y escalabilidad futura.

## 5. Objetivos

### 5.1 Objetivo General

Desarrollar una serie de nodos dentro de una red de monitoreo y control ambiental que permita la gestión centralizada de múltiples cultivos de setas Orellana Rosada usando un servidor local que integra el **Módulo de Almacenamiento y Datos (MSAD)** para la gestión de información.

### 5.2 Objetivos Específicos

1.  Implementar un esquema de comunicación basado en el protocolo MQTT para la interconexión entre múltiples Nodos sensores/actuadores y un servidor central Raspberry Pi.
2.  Desarrollar un sistema de identificación y gestión de múltiples cultivos (`client_id`) que permita el monitoreo independiente de variables ambientales (temperatura y humedad) y el control específico de actuadores para cada instalación.
3.  Crear una interfaz web (Angular) que permita visualizar y controlar múltiples cultivos desde un panel centralizado, con la capacidad de generar reportes de datos históricos (vía MSAD) y visualizar alertas del sistema.
4.  Implementar un sistema de respaldo y gestión de datos local, utilizando el **módulo MSAD** integrado, para realizar copias de seguridad automáticas/manuales y permitir la restauración de la base de datos del sistema.

## Bibliografía

[1] M. A. R. Sarkar et al., "Smart Agriculture Using IoT and Machine Learning: A Comprehensive Review," IEEE Access, vol. 9, pp. 140067–140103, 2021.

[2] L. A. da Silva, F. L. Leite, M. A. Simões, and R. C. F. Lima, "IoT-based Smart Farming: Trends and Future Perspectives," IEEE Latin America Transactions, vol. 19, no. 9, pp. 1618–1625, Sep. 2021.

[3] A. K. Tripathy, S. K. Panda, and D. Puthal, "An IoT-Based Smart Irrigation System Using MQTT Protocol," IEEE Internet of Things Journal, vol. 8, no. 5, pp. 3652–3660, Mar. 2021.

[4] P. Patel, K. Modi, and H. Joshi, "Design and Implementation of IoT-based Greenhouse Automation System," IEEE Xplore, 2020.

[5] S. O. T. Oladokun and M. O. Oladokun, "IoT-based Agricultural Environment Monitoring System Using MQTT and NodeMCU," in Proc. IEEE International Conference on Internet of Things and Intelligence Systems (IoTaIS), 2022.

[6] D. E. Besada-Portas, J. A. López-Orozco, and M. J. Álvarez-Hernández, "IoT-Based Smart Monitoring System for Greenhouses: A Review," IEEE Sensors Journal, vol. 21, no. 19, pp. 22367–22380, Oct. 2021.

[7] S. Choudhury, R. Sharma, and A. P. Bhondekar, "Low-cost Smart Agriculture System using IoT and Wireless Sensor Networks," in Proc. IEEE 6th World Forum on Internet of Things (WF-IoT), 2020, pp. 1–6.

[8] H. Nguyen, H. Le, and T. T. Nguyen, "An Intelligent System for Mushroom Cultivation Using IoT and Environmental Sensors," in Proc. IEEE 9th International Conference on Green Computing and IoT (ICGCIoT), 2022.

[9] M. G. Ramesh, P. Rajalakshmi, and D. Kumar, "Design and Implementation of an IoT-Based Smart Mushroom Farming System," in Proc. IEEE International Conference on Advanced Networks and Telecommunications Systems (ANTS), 2023.

[10] V. Singh and N. Gupta, "Optimizing Greenhouse Conditions Using an IoT and AI-based System," IEEE Transactions on Computational Agriculture, vol. 2, no. 1, pp. 12–19, 2022.