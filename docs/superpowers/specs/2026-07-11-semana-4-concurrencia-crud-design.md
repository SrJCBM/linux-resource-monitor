# Diseno de Semana 4: concurrencia y CRUD

## Objetivo

Completar la Semana 4 del proyecto mediante una captura consolidada de recursos,
el uso explicito de hilos y `os.fork()`, y operaciones CRUD sobre SQLite. La
implementacion debe conservar la arquitectura MVC, utilizar solamente la
biblioteca estandar y funcionar en Linux sin privilegios de administrador.

## Alcance

La entrega incluye:

- Recoleccion concurrente con al menos dos instancias explicitas de
  `threading.Thread`.
- Demostracion aislada de un proceso hijo creado con `os.fork()`.
- Consolidacion de CPU, memoria, disco, red, procesos y usuarios.
- Persistencia atomica de capturas completas en SQLite.
- Creacion, consulta, actualizacion de metadatos y eliminacion de capturas.
- Controladores y menus de consola necesarios para operar el CRUD.
- Pruebas unitarias y evidencia Linux para los mecanismos anteriores.
- Instrucciones de validacion en Ubuntu y WSL.

No se incluyen funcionalidades de la Semana 5, interfaces graficas, servicios
web, motores de persistencia adicionales ni dependencias externas.

## Relacion con el orden de actividades definido

El trabajo conserva la secuencia incremental de
`docs/ESTRUCTURA_PROYECTO.md`. Semana 4 no vuelve a implementar los recolectores
de recursos: utiliza como entradas los contratos terminados en las semanas 2 y
3 y agrega coordinacion y persistencia sobre ellos.

| Etapa definida | Resultado utilizado o producido | Relacion con Semana 4 |
|---|---|---|
| Semana 1: requisitos, arquitectura y base de datos | RF-07 a RF-12, MVC y modelo relacional | Define los contratos que deben respetar concurrencia y CRUD. |
| Semana 2: CPU, memoria y `/proc` | `cpu_model.py` y `memoria_model.py` | Se incorporan como tareas de la captura concurrente sin modificar sus formulas. |
| Semana 3: disco, red, procesos y usuarios | Cuatro modelos y sus listas de metricas | Completan los seis modulos necesarios para una captura integral. |
| Semana 4: concurrencia | `concurrencia_controller.py` y evidencia de hilos y `fork()` | Consolida los modelos existentes antes de cualquier escritura. |
| Semana 4: persistencia | `conexion.py`, `esquema.sql` y `repositorio.py` | Guarda la estructura consolidada mediante una transaccion SQLite. |
| Semana 4: CRUD e interfaz | `crud_controller.py` y menus numerados | Expone RF-09 a RF-12 al usuario sin romper la separacion MVC. |
| Semana 5: integracion y entrega | Pruebas integrales, manuales, evidencias y correcciones | Recibe la Semana 4 funcional para validacion final; no se adelantan articulo, presentacion ni video. |

Aunque `database/esquema.sql` aparece en la creacion prevista para Semana 1,
actualmente no existe en el repositorio. Se incorpora al primer bloque de Semana
4 como recuperacion de un entregable de diseno pendiente, antes de implementar
el repositorio. Esto no cambia el alcance funcional ni agrega una actividad
nueva.

### Secuencia interna de Semana 4

Para mantener las dependencias en orden, las actividades se ejecutaran asi:

1. Materializar el esquema de Semana 1 en `database/esquema.sql` y crear
   `database/conexion.py`.
2. Implementar y probar `model/repositorio.py` sobre una base temporal.
3. Crear `controller/monitor_controller.py` para definir la consolidacion de los
   seis modelos ya implementados.
4. Implementar `controller/concurrencia_controller.py`, primero con hilos y
   despues con la demostracion aislada de `os.fork()`.
5. Implementar `controller/crud_controller.py` y los menus de consola para
   operar RF-09 a RF-12.
6. Ejecutar las pruebas unitarias y obtener evidencia funcional en WSL.
7. Actualizar el README con el procedimiento de validacion de Semana 4.

Cada paso depende solamente de resultados producidos por los pasos anteriores:
el CRUD no se conecta directamente a los recolectores, SQLite no se usa desde
los hilos y el proceso hijo se ejecuta fuera de la fase concurrente.

## Arquitectura

### Base de datos

`database/conexion.py` abrira una conexion nueva por operacion y ejecutara
`PRAGMA foreign_keys = ON`. `database/esquema.sql` sera la fuente del esquema
SQLite y creara `capturas` junto con las seis tablas de metricas documentadas en
Semana 1. Los archivos de ejecucion se almacenaran bajo `database/data/` y no se
versionaran.

### Repositorio

`model/repositorio.py` sera el unico componente que contenga SQL. Expondra
operaciones para:

- Inicializar el esquema.
- Guardar una captura completa.
- Listar capturas con filtro de fecha opcional.
- Consultar el detalle completo por identificador.
- Actualizar solamente `etiqueta` y `comentario`.
- Eliminar una captura.

El guardado insertara la captura padre y todas sus metricas dentro de una sola
transaccion. Cualquier fallo provocara rollback y no dejara registros parciales.
Las relaciones hijas usaran `ON DELETE CASCADE`.

Los valores de disco que los modelos entregan en bytes se convertiran a GB en
el limite del repositorio para respetar el esquema documentado, sin alterar el
contrato de `disco_model.py`.

### Controlador de monitoreo

`controller/monitor_controller.py` conocera las funciones publicas de los seis
modelos y producira una estructura consolidada con estas claves estables:

```python
{
    "cpu": {...},
    "memoria": {...},
    "discos": [...],
    "red": [...],
    "procesos": [...],
    "usuarios": [...],
}
```

El controlador no ejecutara SQL ni analizara salidas de `/proc` o comandos.

### Hilos

`controller/concurrencia_controller.py` creara explicitamente varios objetos
`threading.Thread` para tareas independientes. Todos los hilos se iniciaran
antes de esperar sus resultados. Cada tarea escribira en una ranura de resultado
aislada y cualquier excepcion se conservara con el nombre del modulo.

La recoleccion podra devolver resultados parciales para presentacion, junto con
errores controlados. Una captura persistente solo se guardara cuando esten
presentes todos los modulos obligatorios. Ningun hilo abrira o utilizara una
conexion SQLite.

Para evidenciar concurrencia, el resultado incluira nombre del hilo, instante de
inicio e instante de finalizacion de cada tarea. Estos datos son evidencia de
ejecucion y no forman parte de las tablas de metricas.

### Proceso hijo

La demostracion de `os.fork()` se ejecutara en una funcion separada cuando no
existan hilos activos. Padre e hijo se comunicaran mediante un pipe del sistema
operativo. El hijo enviara su PID, el PID del padre y un resultado pequeno de
monitoreo; el padre cerrara los descriptores que no utiliza y llamara a
`os.waitpid()` para evitar procesos zombie.

No se abrira SQLite antes del `fork()` y el hijo no recibira ni reutilizara una
conexion de base de datos. En sistemas sin `os.fork()`, la funcion terminara con
un error controlado que indique que la demostracion requiere Linux.

### CRUD y Vista

`controller/crud_controller.py` coordinara la recoleccion, validara si la
captura esta completa y llamara al repositorio. Tambien coordinara listar,
consultar, actualizar y eliminar, sin contener SQL.

`view/menu_view.py` presentara opciones numeradas para las operaciones CRUD,
validara entradas basicas y solicitara confirmacion explicita antes de eliminar.
La Vista recibira los datos desde los controladores y no accedera directamente
a modelos, `/proc`, comandos ni SQLite.

## Flujo de una captura

1. El usuario solicita guardar una captura y proporciona metadatos opcionales.
2. El controlador inicia las tareas de monitoreo mediante hilos.
3. Los hilos finalizan y el controlador consolida resultados y errores.
4. Si falta un modulo obligatorio, se informa el fallo y no se inicia ninguna
   escritura.
5. El repositorio abre su propia conexion SQLite.
6. La captura y todas las metricas se insertan en una unica transaccion.
7. Al confirmar la transaccion, el controlador recibe el identificador generado
   y la Vista muestra el resultado.

## Manejo de errores

- Las excepciones de tareas concurrentes se asocian al modulo que fallo.
- Los fallos parciales pueden mostrarse, pero no se persisten como captura
  completa.
- Un error SQL revierte toda la captura y se convierte en un error controlado.
- Consultar, actualizar o eliminar un identificador inexistente devuelve un
  resultado negativo, no una excepcion inesperada.
- La interrupcion por teclado vuelve al menu o termina de manera limpia.
- La demostracion de `fork()` informa claramente cuando no se ejecuta en Linux.

## Estrategia de pruebas

La implementacion seguira ciclos TDD. Primero se escribira cada prueba y se
comprobara que falla por la ausencia del comportamiento; despues se agregara la
implementacion minima.

Las pruebas del repositorio utilizaran una base SQLite temporal y verificaran:

- Activacion de claves foraneas.
- Creacion y lectura completa de una captura.
- Filtro de listado por fecha.
- Actualizacion exclusiva de etiqueta y comentario.
- Eliminacion en cascada.
- Rollback ante una metrica invalida.

Las pruebas de concurrencia verificaran que se creen al menos dos hilos, que se
inicien antes de unirse, que los resultados se consoliden y que los errores
parciales se identifiquen. La demostracion de `fork()` se validara directamente
en Linux y se omitira de forma controlada fuera de ese sistema. La suite de
Semana 4 se ejecutara tambien en la distribucion Ubuntu disponible mediante WSL.

Las pruebas de integracion completas entre menu, controladores, modelos y base
de datos permanecen en Semana 5, tal como establece el orden original. Semana 4
dejara unidades probadas y evidencia ejecutable suficiente para que esa
integracion final no dependa de componentes simulados o pendientes.

## Criterios de finalizacion

La Semana 4 se considerara completa cuando RF-07 a RF-12 tengan implementacion
ejecutable, las capturas sean atomicas, el CRUD sea operable por consola, la
demostracion de hilos y proceso hijo produzca evidencia verificable, todas las
pruebas pasen en WSL y el README describa el procedimiento de validacion.
