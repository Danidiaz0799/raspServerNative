# Sistema de Gestión Centralizada de Datos y Control Ambiental para Múltiples Cultivos de Orellana Rosada con Módulo de Almacenamiento y Datos (MSAD)

## 2.1 Planteamiento del Problema

La producción de setas Orellana Rosada (*Pleurotus djamor*), especialmente cuando se realiza en **múltiples unidades de cultivo distribuidas o se busca escalar la producción**, enfrenta **importantes desafíos** para monitorear y controlar el ambiente de forma precisa. Un problema clave es la **falta de sistemas integrados** que puedan gestionar y coordinar las condiciones de cada unidad desde un punto central. A menudo, los productores utilizan **métodos manuales o herramientas separadas**, lo que hace difícil mantener constantes las variables ambientales importantes (temperatura, humedad, CO₂). Esta **falta de uniformidad** puede reducir la producción y la calidad, y además **dificulta la supervisión general y el buen funcionamiento**, limitando la capacidad de **crecer de forma competitiva y sostenible**.

Si bien las tecnologías del Internet de las Cosas (IoT) proporcionan **buenas herramientas** para la automatización, su aplicación práctica para el **manejo conjunto de varios entornos de cultivo** a pequeña o mediana escala suele encontrar obstáculos como el **costo, la dificultad para integrar sistemas** y la **falta de ayuda técnica adecuada**. **Se necesita claramente una solución integrada y fácil de usar** que permita **recoger, procesar y mostrar datos de diferentes puntos de cultivo**, ayudando a tomar decisiones y controlar todo desde un solo lugar, pero respetando las necesidades de cada cultivo individual. La falta de un sistema que ofrezca de forma práctica esta **interconexión (usando MQTT), gestión individual por cultivo (`client_id`), visualización centralizada (interfaz web) y una gestión fiable de datos (mediante un Módulo de Almacenamiento y Datos - MSAD - para backups y reportes)**, dificulta el uso eficiente de los recursos y pone en riesgo la **posibilidad de crecer de forma rentable y sostenible** en la producción de esta especie de hongo.

## 2.2 Justificación

La optimización del cultivo de setas Orellana Rosada en entornos controlados, especialmente al **operar con múltiples unidades de producción distribuidas**, enfrenta desafíos cruciales que impactan directamente la productividad y la calidad. Mantener variables ambientales como la temperatura y la humedad dentro de rangos óptimos es vital, pero **coordinar y asegurar esta consistencia en diversas unidades** se vuelve exponencialmente complejo para productores sin infraestructura tecnológica integrada. Esta dificultad no solo limita la capacidad de escalar la producción y competir eficazmente, sino que también incrementa el riesgo de pérdidas y el uso ineficiente de recursos al no poder gestionar cada unidad de forma óptima y centralizada.

La implementación de un sistema de monitoreo y control basado en **un servidor central Raspberry Pi comunicándose vía MQTT con nodos distribuidos** (Objetivo Específico 1) ofrece una solución eficiente y escalable. Este enfoque permite **automatizar la gestión de variables críticas de forma individualizada por cultivo (`client_id`) pero coordinada desde un único punto** (Objetivo Específico 2), eliminando la necesidad de supervisión manual constante en cada unidad. El monitoreo en tiempo real y la **visualización centralizada a través de una interfaz web (Angular)** (Objetivo Específico 3) proporcionan datos precisos y una visión global, garantizando ambientes estables, optimizando el uso de recursos y asegurando una producción consistente y de alta calidad a través de todas las unidades. Además, la integración del **módulo MSAD para la gestión fiable de datos (backups y reportes)** (Objetivo Específico 4) es fundamental para asegurar la persistencia de la información y facilitar el análisis histórico del rendimiento de los múltiples cultivos.

No obstante, la adopción de tecnologías IoT, incluso en arquitecturas como la propuesta, puede enfrentar barreras como el costo inicial de los nodos o la curva de aprendizaje técnico, especialmente en contextos rurales. Este proyecto se justifica al proponer un **diseño basado en componentes accesibles (Raspberry Pi, ESPs, MQTT) y una estructura modular (incluyendo MSAD)**, buscando ofrecer un sistema **adaptable y relativamente fácil de implementar y operar** por pequeños y medianos productores, sin requerir inversiones prohibitivas o conocimientos técnicos extremadamente avanzados para gestionar eficazmente múltiples entornos de cultivo.

Además de su aplicabilidad práctica, el proyecto contribuye al conocimiento en **agricultura de precisión y gestión distribuida de cultivos**, un área donde el cultivo especializado de setas puede beneficiarse enormemente. Las particularidades de este cultivo, que demandan control ambiental riguroso y a menudo se realizan en lotes separados, hacen que la **implementación documentada de un sistema IoT centralizado con capacidades robustas de gestión de datos (gracias al módulo MSAD)** represente una aportación valiosa. Este desarrollo puede servir como **referencia y base para futuras adaptaciones** en otros cultivos con requisitos ambientales específicos y modelos de producción distribuida.


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

El marco teórico de este proyecto fundamenta los aspectos electrónicos y biológicos necesarios para el diseño e implementación del sistema IoT distribuido propuesto para el cultivo *in-door* de setas Orellana Rosada. Este cultivo requiere un control preciso de condiciones ambientales para optimizar su producción y calidad, lo cual justifica la implementación de un sistema automatizado y centralizado.

#### 4.1.1 Características del Cultivo de Setas Orellana Rosada
La *Pleurotus djamor*, conocida como seta Orellana Rosada, es un hongo valorado por su alto contenido nutricional y su aplicación en la industria alimentaria. Requiere condiciones específicas para garantizar un crecimiento óptimo:
*   **Rango de Temperatura:** 22-28 °C. Afecta directamente el desarrollo micelial y la fructificación.
*   **Humedad Relativa:** 85-95%. Esencial para evitar deshidratación y promover un desarrollo uniforme.
*   **Sustrato:** Mezclas lignocelulósicas (paja, aserrín), esterilizadas.
*   **Luz:** Niveles bajos de luz difusa estimulan la fructificación.

El control preciso de estas variables es fundamental, y la gestión distribuida de múltiples cultivos simultáneos requiere un sistema automatizado como el propuesto para mantener la consistencia y eficiencia.

#### 4.1.2 Componentes Electrónicos Fundamentales
El sistema se basa en una red de dispositivos IoT (clientes y servidor) con sensores y actuadores específicos.

**Sensores:**
1.  **SHT3x:** Sensor digital de alta precisión para Temperatura y Humedad Relativa, comunicándose vía I2C. Es el sensor primario para monitorizar las variables ambientales críticas (Objetivo Específico 2).

**Actuadores:**
1.  **Ventiladores:** Para regulación de aire/CO₂.
2.  **Humidificadores:** Para control de humedad.
3.  **Iluminación LED:** Para control de luz.
    *   *Todos controlados mediante GPIO, permitiendo la acción remota desde el servidor central (Objetivo Específico 2).*

**Plataforma de Control:**
1.  **Nodo Cliente (Raspberry Pi/Compatible):**
    *   Funciones: Lectura de sensores (SHT3x), control local de actuadores vía GPIO, **cliente MQTT para comunicación bidireccional** (Objetivo Específico 1), y **identificación única del cultivo (`client_id`)** para gestión diferenciada (Objetivo Específico 2).
2.  **Servidor Central (Raspberry Pi):**
    *   Funciones: Actúa como **Broker MQTT central** (Objetivo Específico 1), ejecuta el **servidor web (Flask)** para la API RESTful y sirve la **interfaz web (Angular)** (Objetivo Específico 3), gestiona la **base de datos (SQLite)** para históricos, coordina **múltiples clientes (`client_id`)** (Objetivo Específico 2), y ejecuta el **Módulo de Almacenamiento y Datos (MSAD)** para backups y reportes (Objetivo Específico 4).

#### 4.1.3 Arquitectura de Comunicación

**Protocolo MQTT:** Fundamental para la interconexión (Objetivo Específico 1).
1.  **Roles:** Clientes (Nodos) publican datos y suscriben a comandos; Broker (Servidor) gestiona el flujo de mensajes; Aplicación (Servidor) actúa como cliente para interactuar con el broker.
2.  **Tópicos:** Estructurados jerárquicamente para identificar el cultivo (`[id_cultivo]`/`client_id`) y la función (sensor/actuador/estado), permitiendo la gestión individualizada (Objetivo Específico 2). Ejemplo: `sensor/[client_id]/temperatura`, `actuador/[client_id]/[dispositivo]/set`.

**Flujo de Datos:** Los Nodos publican datos periódicamente; el Servidor Central recibe, almacena, procesa, y publica comandos según la lógica de control y las interacciones desde la interfaz web (Objetivo Específico 3) o la API. El módulo MSAD accede a la base de datos para sus funciones (Objetivo Específico 4).

#### 4.1.4 Impacto del Sistema Distribuido
La arquitectura propuesta permite:
*   **Gestión Centralizada:** Supervisión y control unificado de múltiples unidades (Objetivo Específico 3).
*   **Escalabilidad:** Fácil adición de nuevos nodos/cultivos (inherente a la arquitectura MQTT y gestión por `client_id` - Objetivo Específico 2).
*   **Eficiencia Operativa:** Optimización de recursos y mejora de consistencia.

### 4.2 Marco Legal

El marco legal orienta el desarrollo del sistema para cumplir con estándares de calidad, seguridad y sostenibilidad.

#### 4.2.1 Normas de Calidad y Seguridad

**Normas Internacionales:** Se consideran estándares como ISO/IEC 27001 (seguridad información IoT), IEEE 802.11 (redes inalámbricas) y las especificaciones del protocolo MQTT (v3.1.1/v5.0) utilizado (Objetivo Específico 1).

**Normas Nacionales (Ejemplo Colombia):** Se tienen en cuenta regulaciones como RETIE (instalaciones eléctricas), normativas CRC (telecomunicaciones) y Ley 1581 de 2012 (protección de datos personales).

**Normativas Específicas Aplicables al Sistema:**
*   **Seguridad de Datos:** Consideraciones sobre seguridad en MQTT, autenticación de dispositivos y protección de datos almacenados y en backups (relevante para Objetivo Específico 4).
*   **Seguridad Eléctrica:** Cumplimiento de normas para equipos electrónicos (IEC 62368-1), protección y aislamiento.
*   **Sostenibilidad:** Consideraciones sobre eficiencia energética y gestión de recursos.

Este marco busca una implementación segura y conforme a normativas.

## 5. Objetivos

### 5.1 Objetivo General

Desarrollar una serie de nodos dentro de una red de monitoreo y control ambiental que permita la gestión centralizada de múltiples cultivos de setas Orellana Rosada usando un servidor local que integra el **Módulo de Almacenamiento y Datos (MSAD)** para la gestión de información.

### 5.2 Objetivos Específicos

1.  Implementar un esquema de comunicación basado en el protocolo MQTT para la interconexión entre múltiples Nodos sensores/actuadores y un servidor central Raspberry Pi.
2.  Desarrollar un sistema de identificación y gestión de múltiples cultivos (`client_id`) que permita el monitoreo independiente de variables ambientales (temperatura y humedad) y el control específico de actuadores para cada instalación.
3.  Crear una interfaz web (Angular) que permita visualizar y controlar múltiples cultivos desde un panel centralizado, con la capacidad de generar reportes de datos históricos (vía MSAD) y visualizar alertas del sistema.
4.  Implementar un sistema de respaldo y gestión de datos local, utilizando el **módulo MSAD** integrado, para realizar copias de seguridad automáticas/manuales y permitir la restauración de la base de datos del sistema.

## 6. Alternativa de Solución Propuesta

La solución desarrollada implementa una **arquitectura cliente-servidor distribuida** para responder a las necesidades de monitoreo y control centralizado de múltiples unidades de cultivo de Orellana Rosada, alineándose con el Objetivo General.

### 6.1 Componentes de la Solución

*   **Nodo Cliente (por cultivo):**
    *   Plataforma: Raspberry Pi 3B+ o compatible.
    *   Sensores: **SHT3x (Temp/Humedad)** para monitorización ambiental (Objetivo Específico 2).
    *   Actuadores: Ventiladores, Humidificadores, LEDs, controlados vía GPIO según comandos del servidor (Objetivo Específico 2).
    *   Software: **Cliente MQTT** para comunicación (Objetivo Específico 1) e identificación única (`client_id`) (Objetivo Específico 2).

*   **Servidor Central (Raspberry Pi):**
    *   Plataforma: Raspberry Pi 3B+ o superior.
    *   **Broker MQTT:** Gestión central de mensajes (Objetivo Específico 1).
    *   **Servidor de Aplicación (Flask):** Provee la API RESTful y la lógica de control.
    *   **Interfaz Web (Angular):** Panel centralizado para visualización y control (Objetivo Específico 3).
    *   **Base de Datos (SQLite):** Almacenamiento de datos históricos por `client_id`.
    *   **Módulo de Almacenamiento y Datos (MSAD):** Integrado para **backups, reportes y gestión de datos** (Objetivo Específico 4).

*   **Red de Comunicación:**
    *   **Protocolo MQTT:** Comunicación eficiente nodo-servidor (Objetivo Específico 1).
    *   Red Local (WiFi/Ethernet).

### 6.2 Especificaciones Técnicas Clave

*   **Hardware Base:** Raspberry Pi 3B+.
*   **Sensor Ambiental:** SHT3x (I2C).
*   **Software Servidor:** Raspberry Pi OS, Mosquitto, Python/Flask, SQLite, Angular.
*   **Librerías Python Clave:** `paho-mqtt` (para Obj. 1), `Flask`, `Flask-Cors`, `aiosqlite`, `numpy`, `schedule` (para Obj. 4 - MSAD).
*   **Protocolo:** MQTT v3.1.1/v5.0.
*   **Estructura de Tópicos MQTT:** Jerárquica basada en `[client_id]`, `sensor`/`actuador`/`estado`, y `[tipo]`, permitiendo la gestión individualizada y comunicación bidireccional (Obj. 1 y 2).

Esta solución ofrece un sistema **distribuido y centralizado**, utilizando hardware accesible y protocolos estándar para cumplir los objetivos de monitoreo, control, visualización y gestión de datos para múltiples cultivos de Orellana Rosada, con énfasis en la fiabilidad aportada por el módulo MSAD.

## 7. METODOLOGÍA PROPUESTA

La metodología propuesta se orienta a garantizar el desarrollo eficiente y funcional de la red de monitoreo y control ambiental para el cultivo de setas Orellana Rosada. Este enfoque se centra en la implementación de una arquitectura distribuida que optimice las condiciones ambientales, priorizando estrategias prácticas y aplicables en entornos controlados.

### 7.1 Enfoque Metodológico

El enfoque del proyecto es experimental y aplicado, basado en una arquitectura cliente-servidor distribuida. Este modelo permite el desarrollo de un sistema que monitorea y controla automáticamente variables críticas como temperatura y humedad en múltiples cultivos, con el objetivo de mejorar la productividad y facilitar la gestión centralizada.

### 7.2 Procedimientos y Estrategias

1.  **Diseño e Implementación del Sistema**
    *   Configuración de Raspberry Pi clientes con sensores **SHT3x** mediante conexión I2C.
    *   Implementación del servidor central en Raspberry Pi con broker MQTT y servidor web Flask.
    *   Integración de actuadores (ventiladores, humidificadores, LEDs) mediante control GPIO.
    *   Desarrollo de software cliente para gestión de sensores y actuadores.
    *   Implementación de la comunicación MQTT entre clientes y servidor.

2.  **Desarrollo de la Interfaz Web**
    *   Creación del frontend en Angular con visualización en tiempo real.
    *   Implementación del backend en Flask con API REST.
    *   Integración con el broker MQTT para datos en tiempo real.
    *   Desarrollo de paneles de control y monitoreo por cultivo.

3.  **Pruebas de Operación**
    *   Validación de la comunicación entre clientes y servidor.
    *   Pruebas de lectura de sensores y control de actuadores.
    *   Verificación del sistema de monitoreo en tiempo real.
    *   Comprobación de la gestión multi-cultivo.
    *   Pruebas de respuesta automática ante cambios ambientales.

4.  **Optimización del Sistema**
    *   Ajuste de parámetros de control ambiental.
    *   Optimización del rendimiento de la red.
    *   Mejora de la experiencia de usuario en la interfaz web.
    *   Refinamiento de la lógica de control automático.

5.  **Documentación Técnica**
    *   Manual de instalación y configuración de nodos cliente.
    *   Documentación de la arquitectura del sistema.
    *   Guía de operación del sistema de monitoreo.
    *   Registro de configuraciones y procedimientos.

### 7.3 Recursos Requeridos

**Recursos Materiales por Nodo Cliente:**
*   Raspberry Pi 3B+ (o compatible)
*   Sensor **SHT3x** (temperatura y humedad)
*   Ventilador 12V DC (control de temperatura/aire)
*   Humidificador 5V (control de humedad)
*   Sistema de iluminación LED
*   Cables y componentes de conexión (relés, drivers si aplica)

**Recursos Materiales para Servidor:**
*   Raspberry Pi 3B+ (o superior)
*   Tarjeta SD de alta capacidad
*   Adaptador de corriente
*   Cables de red (si aplica)

**Recursos de Software:**
*   Raspberry Pi OS
*   Python 3
*   Flask Framework
*   Angular CLI
*   Mosquitto MQTT Broker
*   SQLite
*   Librerías Python: `paho-mqtt`, `Flask-Cors`, `aiosqlite`, `numpy`, `schedule`, etc.

Esta metodología está diseñada para ser práctica y eficiente, enfocándose en la implementación de una arquitectura distribuida que permita el monitoreo y control centralizado de múltiples cultivos de setas Orellana Rosada. El resultado final será un sistema funcional y documentado que facilite su replicación y mantenimiento.

## 8. CRONOGRAMA DE ACTIVIDADES

El desarrollo del proyecto se distribuye en aproximadamente cuatro meses y medio, asegurando que cada fase se ejecute de manera ordenada y eficiente, culminando con la entrega final el 1 de mayo. Las actividades se presentan con sus respectivos períodos de inicio y finalización.

**Relación de Actividades con su Período de Ejecución Ajustado:**

| Actividad                                       | Inicio    | Duración (días) | Fin       |
| :---------------------------------------------- | :-------- | :-------------- | :-------- |
| Definir requerimientos y objetivos técnicos     | 10-dic-23 | 5               | 14-dic-23 |
| Diseño del diagrama de bloques                  | 15-dic-23 | 7               | 21-dic-23 |
| Adquisición de componentes                      | 22-dic-23 | 10              | 31-dic-23 |
| Configuración inicial del entorno               | 1-ene-24  | 7               | 7-ene-24  |
| Instalación de sensores y actuadores          | 8-ene-24  | 10              | 17-ene-24 |
| Configuración de Raspberry Pi (Cliente y Servidor) | 18-ene-24 | 8               | 25-ene-24 |
| Pruebas iniciales del sistema                   | 26-ene-24 | 10              | 4-feb-24  |
| Optimización del sistema                        | 5-feb-24  | 14              | 18-feb-24 |
| Ejecución de pruebas prolongadas                | 19-feb-24 | 14              | 3-mar-24  |
| Documentación inicial (introducción, objetivos) | 4-mar-24  | 10              | 13-mar-24 |
| Elaboración del marco teórico y estado del arte | 14-mar-24 | 15              | 28-mar-24 |
| Descripción del sistema implementado            | 29-mar-24 | 12              | 9-abr-24  |
| Análisis de resultados                          | 10-abr-24 | 10              | 19-abr-24 |
| Redacción de conclusiones                       | 20-abr-24 | 7               | 26-abr-24 |
| Revisión y entrega final de la monografía       | 27-abr-24 | 5               | 1-may-24  |

*(Nota: El diagrama de Gantt visual correspondiente a esta tabla debería reflejar estas fechas ajustadas.)*

## 9. IMPACTO ESPERADO

El desarrollo de una **red de monitoreo y control ambiental para la gestión centralizada de múltiples cultivos** de setas Orellana Rosada representa un avance significativo en la modernización de la agricultura controlada en Colombia. Su impacto trasciende el ámbito técnico, contribuyendo a la mejora de la productividad, la **accesibilidad tecnológica para gestionar operaciones distribuidas**, y la sostenibilidad del sector.
Este sistema permite a los productores automatizar el control ambiental de **forma coordinada en diversas unidades**, optimizando variables críticas como temperatura y humedad, lo que reduce el margen de error en la producción y minimiza costos operativos asociados a la supervisión individual. A nivel regional y nacional, su implementación favorece la integración de tecnologías de bajo costo en la agricultura, impulsando la innovación en sectores que tradicionalmente han tenido limitado acceso a la automatización centralizada.

### 9.1 Impacto Social
El sistema desarrollado tiene un impacto directo en la comunidad agrícola, especialmente en pequeños y medianos productores dedicados al cultivo de hongos en entornos controlados, **particularmente aquellos que gestionan o desean escalar a múltiples unidades de cultivo**. La implementación de esta tecnología democratiza el acceso a herramientas de automatización y **gestión centralizada**, permitiendo que agricultores con recursos limitados puedan mejorar la eficiencia y rentabilidad de su producción distribuida.

**Beneficiarios Clave:**
*   **Pequeños y medianos productores agrícolas:** Contarán con un sistema accesible que les permitirá optimizar sus procesos **en múltiples cultivos simultáneamente**, reduciendo pérdidas y garantizando una mayor estabilidad en la producción.
*   **Centros de formación técnica y universidades:** El proyecto servirá como base para la enseñanza de tecnologías aplicadas a la agricultura, promoviendo el aprendizaje en automatización, **sistemas distribuidos basados en IoT**, y gestión de datos agrícolas.
*   **Asociaciones agrícolas y gremios:** Entidades del sector podrán utilizar esta tecnología como referencia para la modernización y escalabilidad de las operaciones de sus asociados.
*   **Entidades gubernamentales y ONG:** Programas enfocados en la sostenibilidad agrícola podrán incorporar esta solución en estrategias de apoyo a comunidades rurales para mejorar su competitividad.

### 9.2 Impacto Económico
El proyecto genera un impacto económico positivo al mejorar la eficiencia de la producción de hongos mediante la **gestión centralizada**, la reducción de costos operativos y el incremento de la productividad. Al automatizar procesos clave de forma coordinada, se minimizan pérdidas por inconsistencias entre cultivos y se optimiza el uso de recursos.

**Beneficios Clave:**
*   **Reducción de costos operativos:**
    *   Disminución del desperdicio de insumos mediante el ajuste automático y consistente de temperatura y humedad en todas las unidades.
    *   Ahorro en mano de obra, al **centralizar la supervisión** en lugar de requerir monitoreo constante e individualizado.
    *   Optimización del consumo energético, al coordinar el funcionamiento de dispositivos.
*   **Aumento de la rentabilidad:**
    *   Se estima que un sistema automatizado y centralizado puede aumentar la eficiencia global del cultivo entre un 20% y un 30%, al mantener condiciones óptimas de forma homogénea o adaptada por unidad.
    *   La implementación de tecnologías de control y **la capacidad de gestionar datos históricos (vía MSAD)** permite a los productores mejorar la calidad y consistencia del producto, facilitando el acceso a mercados más exigentes.

### 9.3 Impacto Tecnológico
Desde el punto de vista tecnológico, este proyecto representa una innovación en la aplicación de **sistemas distribuidos IoT para la agricultura controlada**, particularmente en el cultivo de hongos.

**Principales contribuciones tecnológicas:**
*   **Mejora sobre sistemas existentes:**
    *   A diferencia de soluciones comerciales costosas o sistemas aislados, este proyecto ofrece un **sistema integrado y accesible** para la gestión de múltiples unidades.
    *   Se basa en hardware de código abierto (Raspberry Pi) y protocolos estándar (MQTT), facilitando su **replicación, escalabilidad** y mejora continua.
    *   Incorpora el **módulo MSAD**, proporcionando una solución **local y robusta para la gestión de datos (backups y reportes)**, un aspecto crucial a menudo descuidado en sistemas de bajo costo.
*   **Innovación en el mercado local:**
    *   Representa una solución potencialmente pionera en Colombia para la **gestión centralizada y automatizada** del cultivo de hongos a esta escala.
    *   Su diseño modular permite que la tecnología sea adaptable a otros tipos de cultivos en entornos controlados y distribuidos.

## 10. RESULTADOS ESPERADOS

El desarrollo de la red de monitoreo y control ambiental distribuida para el cultivo de setas Orellana Rosada permitirá alcanzar resultados verificables que optimicen la producción agrícola mediante el uso de tecnología accesible y eficiente. Se espera que el sistema funcione de manera autónoma, ajustando variables ambientales como temperatura y humedad en tiempo real, reduciendo la intervención manual y garantizando condiciones óptimas para el crecimiento del cultivo en **múltiples unidades gestionadas centralmente**.

### 10.1 Resultados Técnicos
*   **Sistema de Control Distribuido Funcional:**
    *   Red operativa de nodos cliente (Raspberry Pi o compatibles) para monitoreo y control individualizado.
    *   Servidor central con broker MQTT estable y aplicación Flask funcionando correctamente.
    *   Comunicación bidireccional MQTT efectiva entre nodos y servidor.
    *   Capacidad demostrada de controlar las variables ambientales dentro de los rangos objetivo (ej. 22-28°C, 85-95% humedad).
*   **Interfaz de Usuario Operativa:**
    *   Panel web centralizado desarrollado en Angular, accesible y funcional.
    *   Visualización en tiempo real de datos de sensores de múltiples cultivos.
    *   Sistema funcional de alertas y notificaciones básicas.
    *   Capacidad de generar reportes históricos y visualizar tendencias **(a través del módulo MSAD)**.
*   **Módulo MSAD Funcional:**
    *   Sistema de backups automáticos y manuales operativo.
    *   Capacidad de listar, descargar y restaurar backups funcional.
    *   Generación de reportes en formatos JSON/CSV validada.

### 10.2 Resultados Operativos
*   **Automatización Efectiva:**
    *   Control automático de actuadores funcionando correctamente basado en lecturas de sensores y parámetros definidos.
    *   Mantenimiento estable de las condiciones ambientales óptimas definidas por cultivo.
    *   Reducción significativa de la necesidad de intervención manual en operaciones rutinarias de control ambiental.
    *   (Opcional) Implementación de un sistema básico de respaldo ante fallos de comunicación (ej. comportamiento por defecto de actuadores).
*   **Eficiencia Mejorada:**
    *   Evidencia de optimización en el uso de recursos (energía para actuadores, agua para humidificación) comparado con control manual.
    *   Reducción de pérdidas potenciales de cultivo debidas a fluctuaciones ambientales no controladas.
    *   Mejora en la consistencia y calidad potencial del producto final.
    *   Demostración de la escalabilidad del sistema al gestionar datos y control para un número definido de cultivos simultáneamente.

### 10.3 Resultados Documentales
*   **Documentación Técnica Completa:**
    *   Manual detallado de instalación y configuración para el servidor y los nodos cliente.
    *   Guías de mantenimiento básico y resolución de problemas comunes.
    *   Diagramas actualizados de la arquitectura del sistema y conexiones físicas.
    *   Código fuente comentado y organizado en un repositorio.
    *   Documentación específica del módulo MSAD (contenida en `MSAD_DETAILS.md`).
*   **Documentación Académica:**
    *   Monografía final del proyecto completa y estructurada.
    *   Análisis de los resultados obtenidos y métricas de rendimiento del sistema implementado.
    *   Establecimiento de una base documentada para futuras investigaciones o mejoras en automatización agrícola para este tipo de cultivo.
    *   Evaluación preliminar de la viabilidad de adaptar el sistema a otros tipos de cultivos con necesidades similares.

### 10.4 Impacto Esperado en el Sector
*   **Modernización y Accesibilidad:**
    *   Disponibilidad de una solución tecnológica de control ambiental accesible y escalable para el cultivo de Orellana Rosada.
    *   Provisión de un modelo replicable para otros productores interesados en la automatización.
    *   Contribución al fomento de la agricultura de precisión en el sector fungícola.
*   **Transferencia de Conocimiento:**
    *   Material base para capacitación técnica en IoT aplicado a la agricultura.
    *   Documentación de una implementación práctica y mejores prácticas observadas.
    *   Promoción del uso de tecnologías de código abierto en el sector agrícola.

Finalmente, se espera que este proyecto contribuya a la modernización del sector agrícola colombiano al proporcionar una solución tecnológica accesible y escalable. Su implementación fomentará la adopción de herramientas digitales en la producción agrícola, promoviendo la innovación y la sostenibilidad en el sector.

## 11. Bibliografía

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