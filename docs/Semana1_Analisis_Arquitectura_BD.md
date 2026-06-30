# Semana 1 — Proyecto Integrador de Sistemas Operativos
## Mini Monitor de Recursos para Linux utilizando Python

**Entregables de esta etapa:** Análisis de requerimientos, Diseño de arquitectura, Diseño de base de datos.

---

## 1. Análisis de Requerimientos (Formato IEEE 830)

### 1.1 Propósito

Este documento especifica los requerimientos funcionales y no funcionales del sistema **Mini Monitor de Recursos para Linux**, una aplicación interactiva por consola desarrollada en Python que permite observar el estado de los recursos del sistema operativo (CPU, memoria, procesos, usuarios, disco y red) y administrar un historial de capturas de ese estado mediante operaciones CRUD. En esta primera versión, toda la navegación se realizará mediante menús numerados en terminal; no se presenta una interfaz gráfica como parte obligatoria del alcance inicial.

### 1.2 Alcance

El sistema obtiene información directamente del kernel de Linux a través del sistema de archivos virtual `/proc` y de comandos nativos del sistema operativo (`ps`, `who`, `df`, `free`, `ip`). Adicionalmente, demuestra el uso de mecanismos de concurrencia del sistema operativo (procesos mediante `fork()` e hilos mediante `threading`) y persiste capturas del estado del sistema en una base de datos SQLite, sobre la cual se ofrecen operaciones de creación, consulta, actualización y eliminación.

La primera versión será una aplicación interactiva por consola: el usuario accederá a los módulos mediante menús, opciones numeradas y formularios de entrada en terminal. La arquitectura MVC permitirá reemplazar posteriormente la capa de Vista por una interfaz gráfica sin modificar el Modelo ni la lógica de obtención y persistencia de datos, pero dicha interfaz gráfica no forma parte obligatoria de esta versión.

El sistema **no** controla ni modifica el estado real del sistema operativo (no mata procesos, no libera memoria, no configura red); su función es exclusivamente de **monitoreo y registro**.

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Término | Definición |
|---|---|
| RF | Requerimiento Funcional |
| RNF | Requerimiento No Funcional |
| CRUD | Create, Read, Update, Delete (Crear, Leer, Actualizar, Eliminar) |
| `/proc` | Sistema de archivos virtual de Linux que expone información del kernel en tiempo real |
| PID | Process Identifier, identificador único de un proceso en ejecución |
| Captura | Registro del estado del sistema en un instante de tiempo dado, persistido en la base de datos |
| Hilo (Thread) | Unidad de ejecución concurrente que comparte el espacio de memoria del proceso que lo crea |
| Proceso hijo | Proceso creado mediante `fork()`, con su propio espacio de memoria independiente del proceso padre |

### 1.4 Requerimientos Funcionales (RF)

Cada requerimiento sigue la estructura estándar IEEE 830: identificador, nombre, descripción, entradas, proceso, salidas, prioridad y criterio de aceptación. Los RF están agrupados por módulo para mantener trazabilidad directa con la arquitectura y la base de datos que se definen más adelante.

#### Módulo CPU

| Campo | Detalle |
|---|---|
| **ID** | RF-01 |
| **Nombre** | Obtener información de CPU |
| **Descripción** | El sistema debe leer y mostrar información del procesador, el número de procesadores lógicos, la frecuencia del procesador, la carga promedio y el porcentaje de utilización actual de la CPU. Salvo que se implemente explícitamente el cálculo de núcleos físicos, el número mostrado corresponde a procesadores lógicos. |
| **Fuente de datos** | `/proc/cpuinfo`, `/proc/stat`, `/proc/loadavg` |
| **Entradas** | Ninguna (lectura automática al invocar el módulo) |
| **Salidas** | Procesadores lógicos (entero), frecuencia (MHz), carga promedio, porcentaje de uso (%) |
| **Prioridad** | Alta |
| **Criterio de aceptación** | La información del procesador debe coincidir con `lscpu`; la carga promedio debe corresponder a `/proc/loadavg`; y el porcentaje de utilización debe calcularse desde `/proc/stat` mediante dos lecturas consecutivas y la diferencia entre tiempos activos e inactivos, con un margen de error aceptable frente a `top` debido a la naturaleza variable de la medición. |

#### Módulo Memoria

| Campo | Detalle |
|---|---|
| **ID** | RF-02 |
| **Nombre** | Obtener información de memoria |
| **Descripción** | El sistema debe leer y mostrar la memoria total, memoria usada, memoria libre, memoria disponible y memoria swap (total/usada) del sistema. La memoria libre (`MemFree`) representa páginas sin uso inmediato, mientras que la memoria disponible (`MemAvailable`) estima la memoria que puede utilizarse sin recurrir a swap. |
| **Fuente de datos** | `/proc/meminfo` |
| **Entradas** | Ninguna |
| **Salidas** | Memoria total, usada, libre y disponible (MB), swap total y usada (MB) |
| **Prioridad** | Alta |
| **Criterio de aceptación** | Los valores deben corresponder con los reportados por `/proc/meminfo` y `free -h`; `mem_usada_mb` debe calcularse como `MemTotal - MemAvailable`, y `swap_usada_mb` como `SwapTotal - SwapFree`. |

#### Módulo Procesos

| Campo | Detalle |
|---|---|
| **ID** | RF-03 |
| **Nombre** | Listar procesos en ejecución |
| **Descripción** | El sistema debe obtener y mostrar el listado de procesos activos, incluyendo su PID, nombre, estado y usuario propietario. |
| **Fuente de datos** | Comando `ps` (vía `subprocess`) y/o directorios numéricos de `/proc/[pid]/` |
| **Entradas** | Ninguna |
| **Salidas** | Lista de procesos: PID, nombre, estado (ejecutando, dormido, zombie, etc.), usuario |
| **Prioridad** | Alta |
| **Criterio de aceptación** | ELos campos PID, nombre, estado y usuario propietario deben corresponder con los datos mostrados por ps en una consulta realizada en el mismo intervalo. No se exige una cantidad idéntica de procesos debido a que estos pueden iniciarse o finalizar durante la medición. |

#### Módulo Usuarios

| Campo | Detalle |
|---|---|
| **ID** | RF-04 |
| **Nombre** | Mostrar usuarios conectados |
| **Descripción** | El sistema debe mostrar los usuarios actualmente conectados al sistema, la terminal utilizada y la fecha/hora de inicio de sesión. La duración de conexión se calcula al presentar los datos, mediante la diferencia entre la hora actual y el inicio de sesión. |
| **Fuente de datos** | Comando `who` (vía `subprocess`) |
| **Entradas** | Ninguna |
| **Salidas** | Nombre de usuario, terminal, fecha/hora de inicio de sesión y duración calculada para presentación |
| **Prioridad** | Media |
| **Criterio de aceptación** | La salida debe coincidir con la del comando `who` ejecutado manualmente. |

#### Módulo Disco

| Campo | Detalle |
|---|---|
| **ID** | RF-05 |
| **Nombre** | Obtener información de almacenamiento |
| **Descripción** | El sistema debe mostrar el espacio total, utilizado y libre de los sistemas de archivos montados. |
| **Fuente de datos** | Comando `df` (vía `subprocess`) |
| **Entradas** | Ninguna |
| **Salidas** | Por cada punto de montaje: sistema de archivos, punto de montaje, espacio total, usado y libre (GB), porcentaje de uso |
| **Prioridad** | Alta |
| **Criterio de aceptación** | Los valores deben coincidir con los reportados por `df -h`. |

#### Módulo Red

| Campo | Detalle |
|---|---|
| **ID** | RF-06 |
| **Nombre** | Obtener información de red |
| **Descripción** | El sistema debe mostrar las interfaces de red disponibles, sus direcciones IP y estadísticas básicas de tráfico (bytes/paquetes enviados y recibidos). |
| **Fuente de datos** | `/proc/net/dev`, comando `ip` (vía `subprocess`) |
| **Entradas** | Ninguna |
| **Salidas** | Nombre de interfaz, dirección IP, bytes recibidos, bytes enviados, paquetes recibidos y paquetes enviados |
| **Prioridad** | Alta |
| **Criterio de aceptación** | Los datos deben coincidir con los reportados por `ip addr` y el contenido de `/proc/net/dev`. |

#### Módulo de Concurrencia (Procesos e Hilos)

| Campo | Detalle |
|---|---|
| **ID** | RF-07 |
| **Nombre** | Ejecutar monitoreo mediante proceso hijo |
| **Descripción** | El sistema debe crear al menos un proceso hijo mediante `os.fork()` para ejecutar una tarea de monitoreo de forma aislada del proceso principal. |
| **Entradas** | Ninguna (disparado internamente por el sistema) |
| **Salidas** | Resultado del proceso hijo comunicado al proceso padre (por ejemplo, vía código de salida o archivo/pipe) |
| **Prioridad** | Alta (requisito técnico obligatorio del curso) |
| **Criterio de aceptación** | Debe verificarse, mediante `ps` o logs, la existencia de un PID distinto al del proceso padre durante la ejecución. |

| Campo | Detalle |
|---|---|
| **ID** | RF-08 |
| **Nombre** | Ejecutar monitoreo mediante hilos concurrentes |
| **Descripción** | El sistema debe ejecutar al menos dos hilos concurrentes (`threading.Thread`) que recolecten datos de distintos módulos (por ejemplo, CPU y Red) de forma simultánea. |
| **Entradas** | Ninguna |
| **Salidas** | Datos recolectados por cada hilo, integrados en una sola estructura de resultado |
| **Prioridad** | Alta (requisito técnico obligatorio del curso) |
| **Criterio de aceptación** | Debe demostrarse, mediante logs con timestamps o identificador de hilo, que ambos hilos se ejecutan de forma concurrente y no secuencial. |

#### Módulo CRUD / Persistencia

| Campo | Detalle |
|---|---|
| **ID** | RF-09 |
| **Nombre** | Registrar captura del sistema (Create) |
| **Descripción** | El sistema debe permitir guardar una captura del estado actual del sistema (CPU, memoria, disco, red, procesos y usuarios en un instante dado) en la base de datos, opcionalmente con un comentario o etiqueta del usuario. |
| **Entradas** | Datos recolectados de los módulos RF-01 a RF-06, comentario/etiqueta opcional (texto) |
| **Salidas** | Confirmación de registro guardado con identificador único |
| **Prioridad** | Alta |
| **Criterio de aceptación** | Tras la captura, el registro debe ser consultable inmediatamente mediante RF-10. |

| Campo | Detalle |
|---|---|
| **ID** | RF-10 |
| **Nombre** | Consultar capturas almacenadas (Read) |
| **Descripción** | El sistema debe permitir listar y visualizar el detalle de capturas previamente almacenadas, con posibilidad de filtrar por fecha. |
| **Entradas** | Filtro de fecha (opcional), identificador de captura (para ver detalle) |
| **Salidas** | Listado de capturas (fecha, etiqueta) o detalle completo de una captura específica |
| **Prioridad** | Alta |
| **Criterio de aceptación** | El listado debe reflejar fielmente todas las capturas creadas y no eliminadas. |

| Campo | Detalle |
|---|---|
| **ID** | RF-11 |
| **Nombre** | Actualizar metadatos de una captura (Update) |
| **Descripción** | El sistema debe permitir modificar el comentario y/o etiqueta asociados a una captura existente. Los datos crudos de la captura (métricas) no son editables, solo sus metadatos descriptivos. |
| **Entradas** | Identificador de captura, nuevo comentario/etiqueta |
| **Salidas** | Confirmación de actualización |
| **Prioridad** | Media |
| **Criterio de aceptación** | Al consultar nuevamente la captura, el comentario/etiqueta debe reflejar el nuevo valor. |

| Campo | Detalle |
|---|---|
| **ID** | RF-12 |
| **Nombre** | Eliminar captura almacenada (Delete) |
| **Descripción** | El sistema debe permitir eliminar de forma permanente una captura previamente almacenada. |
| **Entradas** | Identificador de captura |
| **Salidas** | Confirmación de eliminación |
| **Prioridad** | Media |
| **Criterio de aceptación** | Tras la eliminación, la captura no debe aparecer en el listado de RF-10. |

### 1.5 Requerimientos No Funcionales (RNF)

| ID | Nombre | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|---|
| RNF-01 | Plataforma de ejecución | El sistema debe ejecutarse en distribuciones Linux (Ubuntu Desktop, Ubuntu Server o equivalente), dado que depende de `/proc` y comandos exclusivos de Linux. | Alta | La aplicación debe ejecutarse correctamente en una distribución Linux y leer datos desde `/proc` o comandos nativos sin requerir compatibilidad con Windows o macOS. |
| RNF-02 | Lenguaje y entorno | El sistema debe estar desarrollado íntegramente en Python 3, codificado y depurado en Visual Studio Code. | Alta | El proyecto debe ejecutarse con Python 3 y sus archivos fuente principales deben estar implementados en Python. |
| RNF-03 | Persistencia seleccionada y separable | La primera versión del sistema debe almacenar los datos en SQLite. La lógica de acceso debe mantenerse separada en `repositorio.py` para permitir sustituciones futuras sin afectar la lógica del resto de módulos. | Alta | El acceso a datos debe estar encapsulado en `repositorio.py`; el resto de módulos no deben ejecutar consultas SQL directamente y SQLite debe activar `PRAGMA foreign_keys = ON` al abrir la conexión. |
| RNF-04 | Usabilidad y navegación | La aplicación debe presentar un menú numerado, consistente y comprensible desde el cual el usuario pueda acceder a todos los módulos, regresar al menú principal y salir del sistema. | Alta | Todas las operaciones principales deben poder ejecutarse mediante opciones visibles del menú, sin necesidad de escribir manualmente comandos de Linux. |
| RNF-05 | Mantenibilidad | El código debe organizarse modularmente (separación por responsabilidad) para facilitar su mantenimiento, extensión y comprensión por terceros. | Alta | Los archivos deben estar organizados en capas `model`, `view`, `controller` y `database`, manteniendo separadas la obtención de datos, la presentación, la lógica de control y la persistencia. |
| RNF-06 | Manejo de errores | El sistema debe manejar adecuadamente la ausencia de permisos o archivos no disponibles en `/proc`, evitando que la aplicación se cierre abruptamente. | Media | Si una lectura de `/proc` o un comando del sistema falla, la aplicación debe mostrar un mensaje de error comprensible y permitir continuar o volver al menú. |
| RNF-07 | Rendimiento | La recolección de datos mediante hilos no debe bloquear la interfaz por más de 2 segundos en condiciones normales de uso. | Media | Durante una recolección normal, el menú o la respuesta al usuario no debe quedar bloqueada por más de 2 segundos antes de mostrar resultados, progreso o mensaje de espera. |
| RNF-08 | Portabilidad de control de versiones | El código fuente debe versionarse mediante Git y publicarse en GitHub, con historial de commits que evidencie el trabajo incremental del grupo. | Media | El repositorio debe contener historial de commits, archivo `README.md` y estructura de proyecto suficiente para clonar y ejecutar la aplicación. |
| RNF-09 | Documentación | El sistema debe incluir manual de instalación y manual de ejecución como parte del repositorio. | Alta | El `README.md` o los manuales del proyecto deben explicar requisitos, instalación, ejecución y uso básico del menú principal. |
| RNF-10 | Legibilidad de la información | Los resultados deben mostrarse agrupados por módulo, utilizando títulos, etiquetas, unidades de medida, fecha y hora de actualización. No se debe presentar directamente la salida cruda de `/proc` o de los comandos ejecutados. | Alta | Los módulos de CPU, memoria, disco y red deben mostrar valores formateados con sus respectivas unidades y un máximo de dos decimales. |
| RNF-11 | Accesibilidad de la interfaz | Todas las funciones deben poder utilizarse únicamente con el teclado. La aplicación no debe depender exclusivamente del color, barras gráficas o símbolos para comunicar información. | Media | Al ejecutar la aplicación sin colores, todos los valores, estados, advertencias y mensajes deben continuar siendo comprensibles mediante texto. |
| RNF-12 | Consistencia de presentación | Los menús, encabezados, tablas, mensajes y opciones deben conservar un formato uniforme durante toda la ejecución. | Media | Las operaciones equivalentes deben mantener los mismos nombres, numeración, estructura y estilo de presentación. |
| RNF-13 | Retroalimentación al usuario | El sistema debe informar al usuario cuando una operación esté en ejecución, se complete correctamente o produzca un error. | Alta | Las operaciones de captura, consulta, actualización y eliminación deben mostrar un mensaje explícito de éxito o error. |
| RNF-14 | Prevención y recuperación de errores | La aplicación debe validar las entradas del usuario y permitir corregirlas sin cerrarse abruptamente. Las acciones destructivas deben solicitar confirmación. | Alta | Una opción inexistente, un identificador inválido o una entrada vacía no deben cerrar el programa. La eliminación de una captura debe requerir confirmación explícita. |
| RNF-15 | Presentación de listados extensos | Los listados de procesos, capturas y sistemas de archivos deben mostrarse mediante tablas con encabezados y mecanismos de paginación, límite o filtrado. | Media | El listado de procesos no debe llenar indefinidamente la terminal y debe permitir avanzar, regresar o cancelar la consulta. |
| RNF-16 | Compatibilidad de terminal | La interfaz debe funcionar correctamente en terminales Linux comunes, incluso cuando no exista soporte para colores o caracteres gráficos avanzados. | Media | La aplicación debe poder ejecutarse en modo de texto simple sin perder información funcional. |

### 1.6 Restricciones del Sistema

| ID | Restricción |
|---|---|
| RST-01 | El sistema debe ejecutarse exclusivamente sobre Linux; no se garantiza compatibilidad con Windows o macOS debido al uso de `/proc` y `os.fork()` (no disponible en Windows). |
| RST-02 | El uso de `/proc`, `os.fork()` y `threading.Thread()` es obligatorio según los lineamientos del proyecto; no pueden sustituirse por bibliotecas de alto nivel que oculten estos mecanismos (ej. usar exclusivamente `psutil` sin pasar por `/proc` no cumple el requisito técnico). |
| RST-03 | El proyecto debe desarrollarse en grupos de 2 a 3 estudiantes. |

---

## 2. Diseño de Arquitectura (Patrón MVC)

### 2.1 Justificación del patrón

Se adopta el patrón **Modelo-Vista-Controlador (MVC)** porque separa con claridad tres responsabilidades que el proyecto exige mantener independientes: la **obtención de datos del sistema operativo** (que cambia con cada llamada y depende del kernel), la **presentación de esa información al usuario**, y la **orquestación de la lógica**, incluyendo la concurrencia (`fork()`, `threading`) y las decisiones de cuándo leer, guardar o eliminar datos. Esta separación facilita además que cada integrante del grupo trabaje en un módulo distinto sin generar conflictos de código, y mantiene una trazabilidad directa con los RF definidos: cada RF de obtención de datos (RF-01 a RF-06) corresponde a un componente de Modelo; cada RF de concurrencia (RF-07, RF-08) corresponde a lógica de Controlador; y cada RF de CRUD (RF-09 a RF-12) involucra tanto Modelo (acceso a base de datos) como Controlador (reglas de negocio).

### 2.2 Estructura general

```
linux-resource-monitor/
│
├── model/
│   ├── cpu_model.py          # Lectura de /proc/cpuinfo, /proc/stat, /proc/loadavg → RF-01
│   ├── memoria_model.py      # Lectura de /proc/meminfo                       → RF-02
│   ├── procesos_model.py     # Lectura vía ps / /proc/[pid]/                  → RF-03
│   ├── usuarios_model.py     # Lectura vía who                                → RF-04
│   ├── disco_model.py        # Lectura vía df                                 → RF-05
│   ├── red_model.py          # Lectura de /proc/net/dev, ip                   → RF-06
│   └── repositorio.py        # Acceso a la base de datos (capa de datos CRUD) → RF-09 a RF-12
│
├── view/
│   ├── consola_view.py       # Presentación en terminal (formateo de salida)
│   └── menu_view.py          # Renderizado de menús y formularios de entrada
│
├── controller/
│   ├── monitor_controller.py # Orquesta la recolección de datos de todos los módulos
│   ├── concurrencia_controller.py  # Maneja fork() e hilos                    → RF-07, RF-08
│   └── crud_controller.py    # Reglas de negocio del CRUD (validaciones, etc.)→ RF-09 a RF-12
│
├── database/
│   ├── conexion.py           # Configuración de conexión SQLite
│   └── esquema.sql           # Script de creación de tablas
│
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt
└── README.md                 # Manual de instalación y ejecución → RNF-09
```

### 2.3 Responsabilidad de cada capa

**Modelo (Model).** Es la única capa autorizada a comunicarse directamente con el sistema operativo y con la base de datos. Cada submódulo del Modelo (`cpu_model.py`, `memoria_model.py`, etc.) encapsula la lectura de un archivo específico de `/proc` o la ejecución de un comando del sistema vía `subprocess`, y expone una función que retorna los datos ya parseados en una estructura de Python (diccionario o clase de datos), nunca texto crudo. El Modelo no sabe cómo se va a mostrar la información ni quién la solicitó; solo sabe cómo obtenerla correctamente. `repositorio.py` cumple el mismo principio pero para la base de datos: expone funciones como `guardar_captura()`, `obtener_capturas()`, `actualizar_etiqueta()` y `eliminar_captura()`, encapsulando SQLite como persistencia seleccionada para la primera versión y dejando abierta la sustitución futura sin afectar a los demás módulos (esto da cumplimiento directo a RNF-03).

**Vista (View).** Es responsable de la interacción y la presentación en la aplicación de consola. Recibe datos ya procesados desde el Controlador; no accede directamente a `/proc`, no ejecuta comandos de Linux, no interpreta archivos del sistema y no se comunica directamente con la base de datos. Su responsabilidad es presentar menús numerados, encabezados, tablas, etiquetas, unidades de medida, fechas de actualización y mensajes comprensibles para el usuario. Todas las opciones deben ser accesibles mediante teclado. Los colores, barras visuales o símbolos pueden utilizarse únicamente como apoyo, pero los estados también deben expresarse con texto, por ejemplo: `NORMAL`, `ADVERTENCIA` o `CRÍTICO`. Para procesos, capturas y otros listados extensos, la Vista debe aplicar paginación, límites o filtros que eviten saturar la terminal.

**Controlador (Controller).** Es el intermediario y orquestador. `monitor_controller.py` decide qué módulos del Modelo invocar y en qué momento, y entrega los resultados a la Vista. `concurrencia_controller.py` es donde se implementan explícitamente `os.fork()` (creando un proceso hijo que, por ejemplo, ejecuta un módulo de monitoreo en paralelo al padre) y `threading.Thread()` (lanzando al menos dos hilos que recolecten datos de módulos distintos de forma simultánea, por ejemplo CPU y Red), cumpliendo RF-07 y RF-08 de forma aislada y fácil de demostrar/depurar. `crud_controller.py` aplica las reglas de negocio antes de delegar al Modelo: por ejemplo, valida que un comentario no esté vacío antes de actualizar, o confirma la existencia de una captura antes de eliminarla.

### 2.4 Flujo de interacción típico

1. El usuario interactúa con `menu_view.py` mediante teclado y selecciona, por ejemplo, "Ver estado actual del sistema" desde un menú numerado.
2. `menu_view.py` notifica la elección a `monitor_controller.py`.
3. `monitor_controller.py` invoca a `concurrencia_controller.py`, que lanza los hilos necesarios para recolectar en paralelo los datos de CPU, memoria, disco, red, procesos y usuarios (cada hilo llama internamente a su `*_model.py` correspondiente).
4. Los resultados de cada hilo se consolidan en una sola estructura de datos (por ejemplo, un diccionario) dentro del Controlador.
5. `monitor_controller.py` entrega esa estructura a `consola_view.py`, que la formatea con encabezados, etiquetas, unidades, fecha y hora de actualización, sin mostrar salidas crudas de `/proc` o de comandos.
6. Si el usuario decide "Guardar esta captura" (RF-09) desde el menú, la Vista recoge el comentario/etiqueta opcional y lo envía a `crud_controller.py`, que valida los datos y delega en `repositorio.py` el guardado real en la base de datos.

Este flujo es el mismo, en sentido inverso, para Consultar (RF-10), Actualizar (RF-11) y Eliminar (RF-12): la Vista captura la intención del usuario mediante opciones visibles del menú, el Controlador la valida y orquesta, y el Modelo (`repositorio.py`) ejecuta la operación concreta sobre la base de datos. En las acciones destructivas, como eliminar una captura, el flujo debe incluir confirmación explícita antes de ejecutar la operación.

### 2.5 Diagrama de componentes

```
                         +----------------------+
                         |       Usuario        |
                         +----------+-----------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |              VISTA                |
                  |   consola_view.py / menu_view.py  |
                  |   menus, tablas y mensajes        |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |            CONTROLADOR            |
                  |   monitor_controller.py           |
                  |   concurrencia_controller.py      |
                  |   crud_controller.py              |
                  +-----------------+-----------------+
                                    |
                     +--------------+--------------+
                     |                             |
                     v                             v
       +-------------+-------------+   +-----------+-------------+
       |      MODELO - Recursos    |   |   MODELO - Persistencia |
       | cpu_model.py              |   | repositorio.py          |
       | memoria_model.py          |   | CRUD sobre datos        |
       | procesos_model.py         |   +-----------+-------------+
       | usuarios_model.py         |               |
       | disco_model.py            |               v
       | red_model.py              |   +-----------+-------------+
       +-------------+-------------+   | Base de datos           |
                     |                 | SQLite                  |
                     v                 |                         |
       +-------------+-------------+   +-------------------------+
       |     Sistema Operativo     |
       | /proc, ps, who, df, ip    |
       +---------------------------+
```

Este diagrama reemplaza y detalla, en términos de MVC, la arquitectura referencial general dada en el enunciado del proyecto (Interfaz Python → módulos CPU/memoria/Procesos/Disco/Red → Base de Datos → CRUD), conservando exactamente los mismos componentes funcionales pero explicitando dónde vive cada uno dentro del patrón.

### 2.6 Criterios de usabilidad, accesibilidad y presentación

La interfaz de esta versión debe diseñarse para una terminal Linux común y operar completamente mediante teclado. La Vista debe separar con claridad la información del estado actual del sistema y el historial de capturas almacenadas, evitando mezclar resultados en una misma pantalla sin contexto.

Los criterios mínimos de presentación son:

- Menú principal numerado.
- Opción para regresar al menú anterior.
- Opción para volver al menú principal.
- Opción para salir.
- Validación de entradas.
- Confirmación antes de eliminar registros.
- Mensajes de éxito, advertencia y error.
- Encabezados claros.
- Unidades de medida junto a cada valor.
- Fecha y hora de actualización.
- Máximo de dos decimales en valores numéricos.
- Navegación completa mediante teclado.
- No depender únicamente de colores.
- Paginación para procesos y capturas.
- Compatibilidad con terminales sin colores.
- Presentación separada del estado actual y del historial de capturas.

Ejemplo de referencia para el menú principal:

```text
==================================================
       MINI MONITOR DE RECURSOS PARA LINUX
==================================================
Última actualización: DD/MM/AAAA - HH:MM:SS

[1] Estado general del sistema
[2] Información de CPU
[3] Información de memoria
[4] Procesos activos
[5] Disco y almacenamiento
[6] Interfaces de red
[7] Usuarios conectados
[8] Historial de capturas
[9] Salir

Seleccione una opción:
```

Este ejemplo es una referencia de presentación para orientar la consistencia visual de la aplicación de consola; no constituye una implementación definitiva ni limita ajustes posteriores de formato.

### 2.7 Consideraciones técnicas de concurrencia y persistencia

La implementación de concurrencia debe evitar combinaciones inseguras entre procesos, hilos y acceso a base de datos. `os.fork()` no debe ejecutarse mientras existan hilos activos, porque el proceso hijo podría heredar un estado parcial de bloqueos o recursos abiertos. Las conexiones SQLite tampoco deben compartirse entre procesos ni entre hilos; cada flujo de ejecución que necesite persistencia debe abrir y cerrar su propia conexión mediante la capa de repositorio.

Para guardar una captura completa, primero se deben consolidar los resultados de CPU, memoria, disco, red, procesos y usuarios en el Controlador. Después de esa consolidación, `repositorio.py` debe almacenar la captura y sus métricas relacionadas mediante una transacción SQLite, de modo que no queden capturas incompletas si ocurre un error durante el guardado.

---

## 3. Diseño de Base de Datos

### 3.1 Enfoque

Se diseña el esquema usando **SQLite** como persistencia seleccionada para la primera versión, por simplicidad de despliegue y porque cumple adecuadamente las necesidades del proyecto académico. No se exige implementar PostgreSQL ni archivos JSON en esta etapa; sin embargo, el acceso queda encapsulado en `repositorio.py` para permitir sustituciones futuras sin modificar el Modelo de recursos, el Controlador ni la Vista. En SQLite se debe activar `PRAGMA foreign_keys = ON` al abrir la conexión para que las restricciones `ON DELETE CASCADE` se apliquen correctamente.

La decisión clave de diseño es **separar la "captura" (metadatos: cuándo se tomó, qué comentario/etiqueta tiene) de las "métricas" (los valores numéricos de cada módulo en ese instante)**. Esto evita una tabla única gigante y desnormalizada, permite que RF-11 (actualizar solo comentario/etiqueta) no toque jamás los datos crudos de la métrica, y refleja con fidelidad la arquitectura: cada `*_model.py` aporta su propio conjunto de columnas/tabla.

### 3.2 Modelo Entidad-Relación (descripción textual)

Una **captura** (`capturas`) representa un evento de monitoreo en el tiempo. Cada captura tiene una relación **uno a uno** con sus métricas de CPU y memoria, y una relación **uno a muchos** con disco, procesos, interfaces de red y usuarios conectados. La relación de disco es N:1 porque RF-05 exige registrar información por cada punto de montaje, no solo un agregado del disco principal.

```
capturas (1) ───── (1) cpu_metricas
capturas (1) ───── (1) memoria_metricas
capturas (1) ───── (N) disco_metricas
capturas (1) ───── (N) procesos_metricas
capturas (1) ───── (N) red_metricas
capturas (1) ───── (N) usuarios_metricas
```

### 3.3 Tabla `capturas`

Es la tabla central. Cada fila representa una "fotografía" del sistema en un instante dado, junto con sus metadatos editables (esto es lo que da soporte directo a RF-09, RF-10, RF-11, RF-12).

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_captura` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único de la captura |
| `fecha_hora` | DATETIME | NOT NULL, default `CURRENT_TIMESTAMP` | Momento exacto en que se tomó la captura |
| `etiqueta` | VARCHAR(50) | NULL | Etiqueta corta definida por el usuario (ej. "antes de actualizar", "carga alta") — editable vía RF-11 |
| `comentario` | TEXT | NULL | Comentario libre del usuario sobre esa captura — editable vía RF-11 |
| `usuario_registro` | VARCHAR(50) | NULL | Usuario del sistema operativo que generó la captura (trazabilidad) |

### 3.4 Tabla `cpu_metricas`

Relación 1:1 con `capturas`. Soporta RF-01.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_captura` | INTEGER | PRIMARY KEY, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `procesadores_logicos` | INTEGER | NOT NULL | Número de procesadores lógicos detectados; no equivale necesariamente a núcleos físicos |
| `frecuencia_mhz` | FLOAT | NULL | Frecuencia del procesador en MHz |
| `carga_promedio_1m` | FLOAT | NULL | Carga promedio del sistema en el último minuto, leída desde `/proc/loadavg` |
| `carga_promedio_5m` | FLOAT | NULL | Carga promedio del sistema en los últimos cinco minutos, leída desde `/proc/loadavg` |
| `carga_promedio_15m` | FLOAT | NULL | Carga promedio del sistema en los últimos quince minutos, leída desde `/proc/loadavg` |
| `porcentaje_uso` | FLOAT | NOT NULL | Porcentaje de utilización de CPU al momento de la captura |

### 3.5 Tabla `memoria_metricas`

Relación 1:1 con `capturas`. Soporta RF-02.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_captura` | INTEGER | PRIMARY KEY, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `mem_total_mb` | FLOAT | NOT NULL | Memoria total del sistema |
| `mem_usada_mb` | FLOAT | NOT NULL | Memoria en uso, calculada como `MemTotal - MemAvailable` |
| `mem_libre_mb` | FLOAT | NOT NULL | Memoria libre reportada por `MemFree` |
| `mem_disponible_mb` | FLOAT | NOT NULL | Memoria disponible reportada por `MemAvailable` |
| `swap_total_mb` | FLOAT | NULL | Memoria swap total |
| `swap_usada_mb` | FLOAT | NULL | Memoria swap en uso, calculada como `SwapTotal - SwapFree` |

### 3.6 Tabla `disco_metricas`

Relación N:1 con `capturas` (varios sistemas de archivos o puntos de montaje por captura). Soporta RF-05.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_disco_metrica` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador interno de la fila |
| `id_captura` | INTEGER | NOT NULL, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `sistema_archivos` | VARCHAR(100) | NOT NULL | Sistema de archivos reportado por `df` |
| `punto_montaje` | VARCHAR(255) | NOT NULL | Punto de montaje asociado al sistema de archivos |
| `espacio_total_gb` | FLOAT | NOT NULL | Espacio total del sistema de archivos |
| `espacio_usado_gb` | FLOAT | NOT NULL | Espacio utilizado |
| `espacio_libre_gb` | FLOAT | NOT NULL | Espacio disponible |
| `porcentaje_uso` | FLOAT | NULL | Porcentaje de uso del disco |

### 3.7 Tabla `procesos_metricas`

Relación N:1 con `capturas` (varios procesos por captura). Soporta RF-03.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_proceso_metrica` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador interno de la fila |
| `id_captura` | INTEGER | NOT NULL, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `pid` | INTEGER | NOT NULL | PID real del proceso en el sistema operativo |
| `nombre_proceso` | VARCHAR(100) | NOT NULL | Nombre del proceso |
| `estado` | VARCHAR(20) | NULL | Estado del proceso (running, sleeping, zombie, etc.) |
| `usuario_propietario` | VARCHAR(50) | NULL | Usuario dueño del proceso |

### 3.8 Tabla `red_metricas`

Relación N:1 con `capturas` (varias interfaces por captura). Soporta RF-06.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_red_metrica` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador interno de la fila |
| `id_captura` | INTEGER | NOT NULL, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `interfaz` | VARCHAR(20) | NOT NULL | Nombre de la interfaz de red (ej. eth0, wlan0) |
| `direccion_ip` | VARCHAR(45) | NULL | Dirección IP asignada (soporta IPv4 e IPv6) |
| `bytes_recibidos` | BIGINT | NULL | Total de bytes recibidos en la interfaz |
| `bytes_enviados` | BIGINT | NULL | Total de bytes enviados en la interfaz |
| `paquetes_recibidos` | BIGINT | NULL | Total de paquetes recibidos en la interfaz |
| `paquetes_enviados` | BIGINT | NULL | Total de paquetes enviados en la interfaz |

### 3.9 Tabla `usuarios_metricas`

Relación N:1 con `capturas` (varios usuarios conectados por captura). Soporta RF-04.

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_usuario_metrica` | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador interno de la fila |
| `id_captura` | INTEGER | NOT NULL, FOREIGN KEY → `capturas(id_captura)` | Referencia a la captura padre |
| `nombre_usuario` | VARCHAR(50) | NOT NULL | Nombre del usuario conectado |
| `terminal` | VARCHAR(20) | NULL | Terminal desde la que se conectó |
| `inicio_sesion` | DATETIME | NULL | Fecha/hora de inicio de la sesión; la duración de conexión se calcula al presentar los datos |

### 3.10 Script de referencia (SQLite)

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE capturas (
    id_captura       INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    etiqueta         VARCHAR(50),
    comentario       TEXT,
    usuario_registro VARCHAR(50)
);

CREATE TABLE cpu_metricas (
    id_captura           INTEGER PRIMARY KEY,
    procesadores_logicos INTEGER NOT NULL,
    frecuencia_mhz       FLOAT,
    carga_promedio_1m    FLOAT,
    carga_promedio_5m    FLOAT,
    carga_promedio_15m   FLOAT,
    porcentaje_uso       FLOAT NOT NULL,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE memoria_metricas (
    id_captura         INTEGER PRIMARY KEY,
    mem_total_mb       FLOAT NOT NULL,
    mem_usada_mb       FLOAT NOT NULL,
    mem_libre_mb       FLOAT NOT NULL,
    mem_disponible_mb FLOAT NOT NULL,
    swap_total_mb      FLOAT,
    swap_usada_mb      FLOAT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE disco_metricas (
    id_disco_metrica  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura        INTEGER NOT NULL,
    sistema_archivos  VARCHAR(100) NOT NULL,
    punto_montaje     VARCHAR(255) NOT NULL,
    espacio_total_gb  FLOAT NOT NULL,
    espacio_usado_gb  FLOAT NOT NULL,
    espacio_libre_gb  FLOAT NOT NULL,
    porcentaje_uso    FLOAT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE procesos_metricas (
    id_proceso_metrica  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura          INTEGER NOT NULL,
    pid                 INTEGER NOT NULL,
    nombre_proceso      VARCHAR(100) NOT NULL,
    estado              VARCHAR(20),
    usuario_propietario VARCHAR(50),
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE red_metricas (
    id_red_metrica     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura         INTEGER NOT NULL,
    interfaz           VARCHAR(20) NOT NULL,
    direccion_ip       VARCHAR(45),
    bytes_recibidos    BIGINT,
    bytes_enviados     BIGINT,
    paquetes_recibidos BIGINT,
    paquetes_enviados  BIGINT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE usuarios_metricas (
    id_usuario_metrica  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura          INTEGER NOT NULL,
    nombre_usuario       VARCHAR(50) NOT NULL,
    terminal             VARCHAR(20),
    inicio_sesion        DATETIME,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);
```

### 3.11 Sobre tu pregunta: ¿el modelo anterior estaba correcto?

Sí, en esencia el modelo que se planteó antes apuntaba en la dirección correcta (una tabla de capturas con métricas asociadas), pero este diseño lo formaliza y lo corrige en dos puntos importantes que vale la pena que tengas presentes:

Primero, se **separan las métricas por módulo en tablas independientes** en lugar de una sola tabla ancha con todas las columnas juntas. Esto importa porque disco, procesos, red y usuarios pueden tener **múltiples filas por captura** (varios puntos de montaje, varios procesos corriendo a la vez, varias interfaces de red), mientras que CPU y memoria son **un solo conjunto de valores por captura**. Mezclarlos en una sola tabla habría forzado una estructura inconsistente o datos duplicados.

Segundo, se usa `ON DELETE CASCADE` en las llaves foráneas, de modo que al eliminar una captura (RF-12) se eliminen automáticamente todas sus métricas asociadas en las seis tablas, sin dejar registros huérfanos y sin que tengas que escribir lógica manual de limpieza en cada eliminación.

Si en tu implementación decides simplificar (por ejemplo, para avanzar más rápido en las primeras semanas), puedes empezar solo con `capturas` + `cpu_metricas` + `memoria_metricas` y añadir después `disco_metricas`, `procesos_metricas`, `red_metricas` y `usuarios_metricas` cuando implementes esos módulos. La estructura general no cambia, solo se construye de forma incremental, igual que el cronograma del proyecto lo sugiere.
