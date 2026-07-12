# Diseno de Semana 5: integracion, manuales y evidencias

## Objetivo

Integrar en una sola aplicacion de consola los modulos terminados durante las
semanas 2 a 4, completar las pruebas y correcciones necesarias, redactar los
manuales de instalacion y ejecucion, y producir evidencias reproducibles y
visuales. El articulo IEEE, la presentacion y el video quedan fuera de esta fase.

## Alcance

La entrega de esta fase incluye:

- Menu principal para acceder a todos los modulos.
- Estado general recolectado mediante hilos.
- Vistas de CPU, memoria, procesos, disco, red y usuarios.
- Acceso al historial y CRUD implementado en Semana 4.
- Demostracion visible de hilos y `os.fork()`.
- Navegacion, validacion, limitacion de listados y errores controlados.
- Pruebas unitarias e integrales con base SQLite temporal.
- Validacion real en Ubuntu mediante WSL.
- Manuales de instalacion y ejecucion.
- Logs reproducibles y capturas literales de Windows Terminal.
- Indice de evidencias relacionado con los requisitos del proyecto.

No se agregaran dependencias externas, interfaz grafica, servidor web, nuevos
motores de persistencia ni funciones que modifiquen el sistema operativo.

## Menu principal

La primera pantalla ejecutable de `main.py` mostrara:

```text
[1] Estado general
[2] CPU
[3] Memoria y swap
[4] Procesos
[5] Disco
[6] Red
[7] Usuarios conectados
[8] Historial y CRUD
[9] Demostracion de hilos y fork
[0] Salir
```

Todas las opciones funcionaran con teclado. Una opcion invalida mostrara un
mensaje y mantendra la aplicacion activa. Cada pantalla permitira volver al menu
principal. `Ctrl+C` se convertira en una cancelacion comprensible, sin mostrar
un traceback al usuario.

## Arquitectura y flujo

### Controlador

`controller/monitor_controller.py` expondra operaciones para obtener un modulo
individual y para solicitar el estado general concurrente. El Controlador
recibira datos estructurados de los Modelos y los enviara a la Vista. No
contendra parsers, SQL ni formato de terminal.

La opcion de estado general utilizara `recolectar_con_hilos()` y mostrara los
resultados disponibles junto con los errores parciales. Guardar una captura
seguira exigiendo los seis modulos completos y una transaccion atomica.

La demostracion de concurrencia ejecutara primero los hilos, esperara a que
todos terminen y solo entonces invocara `demostrar_fork()`. De esta manera no se
ejecutara `os.fork()` mientras haya hilos activos.

### Vista

`view/consola_view.py` formateara todos los modulos sin acceder al sistema
operativo. Las salidas usaran encabezados de texto simple, unidades y un maximo
de dos decimales. Los estados se comunicaran con las palabras `NORMAL`,
`ADVERTENCIA` y `CRITICO`, sin depender del color.

Los procesos se limitaran por paginas o bloques para no llenar la terminal. Los
sistemas de archivos, interfaces, usuarios y capturas se mostraran en tablas de
texto con anchos previsibles. La duracion de una sesion se calculara al mostrar
los datos a partir de `inicio_sesion`; no se almacenara como una columna nueva.

`view/menu_view.py` sera responsable de la navegacion principal y reutilizara el
menu CRUD existente. No leera `/proc`, no ejecutara comandos y no abrira SQLite.

### Punto de entrada

`main.py` sera el punto de composicion. Construira repositorio y controladores,
ejecutara el menu principal y convertira fallos esperados en mensajes breves. La
base predeterminada permanecera en `database/data/monitor.sqlite3` y seguira
ignorada por Git.

## Manejo de errores

- El fallo de un modulo individual se mostrara sin cerrar el menu.
- El estado general podra mostrar resultados parciales y nombrara los modulos
  que fallaron.
- Una captura incompleta no se guardara.
- Los identificadores y opciones invalidos podran corregirse.
- La eliminacion mantendra la confirmacion explicita `SI`.
- Los listados vacios mostraran un mensaje, no una tabla defectuosa.
- `os.fork()` indicara claramente cuando no se ejecuta en Linux.
- Los errores SQLite se convertiran en mensajes controlados en el limite del
  controlador o del punto de entrada.

## Estrategia de pruebas

La implementacion seguira TDD. Cada comportamiento nuevo tendra una prueba que
falle antes de escribir el codigo de produccion.

Las pruebas unitarias cubriran:

- Formato de disco, red, procesos y usuarios.
- Calculo de duracion de sesiones.
- Navegacion por todas las opciones del menu principal.
- Entrada invalida, retorno al menu y salida.
- Presentacion de errores parciales.
- Ejecucion ordenada de hilos y `fork()`.

Las pruebas integrales cubriran:

- Flujo menu-Controlador-Modelo con colaboradores controlados.
- Creacion, consulta, actualizacion y eliminacion en una base temporal.
- Eliminacion en cascada y rollback.
- Recoleccion real de los seis modulos en WSL.
- Demostracion real de `os.fork()` en WSL.

La suite completa se ejecutara primero con el Python local disponible y despues
con `python3 -m unittest discover -s tests` dentro de Ubuntu WSL.

## Manuales

`docs/manual_instalacion.md` explicara requisitos, clonacion, entorno virtual,
instalacion sin dependencias externas, comprobacion de comandos Linux y pruebas
iniciales.

`docs/manual_ejecucion.md` explicara el menu, cada modulo, CRUD, ubicacion de la
base, validaciones, cierre de la aplicacion y soluciones para errores comunes.

Los dos manuales se escribiran para un compañero que clone el repositorio por
primera vez en Ubuntu, WSL o una maquina virtual.

## Evidencias reproducibles

`docs/evidencias/README.md` sera el indice central. Cada evidencia indicara:

- Requisito demostrado.
- Comando exacto.
- Resultado esperado.
- Archivo de log.
- Captura asociada.

Los logs se generaran desde WSL y no se editaran para alterar resultados. Se
incluiran, como minimo:

1. Suite completa de pruebas.
2. Estado general y seis modulos.
3. CRUD completo sobre una base temporal.
4. Evidencia de nombres y tiempos de hilos.
5. PID padre, PID hijo, parentesco y codigo de salida de `fork()`.

Los datos variables como PID, carga, direcciones IP y numero de procesos se
presentaran como resultados del entorno de prueba, no como valores universales.

## Capturas literales

Las imagenes mostraran una ventana real de Windows Terminal ejecutando Ubuntu
WSL. El procedimiento abrira una sesion dedicada con un titulo reconocible,
ejecutara cada comando de evidencia y conservara la salida visible para captura.

La automatizacion solo intentara capturar el rectangulo de la ventana dedicada;
no capturara el escritorio completo. Si Windows impide identificar la ventana
de forma segura, el proceso se detendra y el manual indicara usar
`Win+Shift+S` seleccionando exclusivamente la terminal. Nunca se tomara una
captura de pantalla completa como alternativa automatica.

Las imagenes se guardaran bajo `docs/evidencias/capturas/` y los logs bajo
`docs/evidencias/logs/`. No se incluiran nombres de usuario, rutas privadas o
otras ventanas fuera de lo necesario para demostrar el proyecto.

## Correcciones y sincronizacion

Al finalizar se revisaran `README.md`, los manuales, la estructura documentada y
el estado de Semana 5. Solo se marcara esta fase parcial como completada cuando
integracion, pruebas, manuales y evidencias existan y hayan sido verificadas. El
articulo, la presentacion y el video permaneceran expresamente pendientes.

El archivo temporal de Word `docs/~$oyecto Integrador de SO.docx` no forma parte
del proyecto y no se incluira en commits.

## Criterios de aceptacion

- `python3 main.py` permite usar todos los modulos y volver al menu principal.
- CPU, memoria, procesos, disco, red y usuarios tienen presentacion legible.
- Historial y CRUD funcionan desde el menu integrado.
- Hilos y `fork()` tienen salida visible y evidencia reproducible.
- Ningun fallo esperado muestra un traceback al usuario.
- Las pruebas pasan en Windows y WSL segun sus condiciones de plataforma.
- Los manuales permiten instalar y ejecutar desde un clon nuevo.
- Logs y capturas se relacionan claramente con RF-01 a RF-12.
- No se redacta todavia el articulo IEEE.
