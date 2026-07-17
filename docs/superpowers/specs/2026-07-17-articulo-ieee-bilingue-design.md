# Diseno del articulo IEEE bilingue

## Objetivo

Redactar dos versiones completas y equivalentes del articulo cientifico del
proyecto Linux Resource Monitor: una en espanol y otra en ingles. Cada version
debe respetar la plantilla IEEE de conferencia proporcionada, ocupar entre
cuatro y seis paginas y describir solamente decisiones, implementaciones y
resultados comprobables en el repositorio.

## Autores y afiliacion

- Julio Cesar Blacio Machuca.
- Ariel Jose Llumiquinga Ñacato.
- Carrera de Ingenieria de Software, Universidad de las Fuerzas Armadas ESPE,
  Sangolqui, Ecuador.

Los correos electronicos y ORCID se omiten mientras no sean proporcionados por
los autores. El apellido `Ñacato` se conservara con su grafia correcta mediante
una codificacion LaTeX compatible con la plantilla.

## Entregables

Los archivos de trabajo se ubicaran en `docs/articulo/`:

- `monitor_recursos_linux_es.tex`: version completa en espanol.
- `linux_resource_monitor_en.tex`: version completa en ingles.
- `referencias.bib`: bibliografia compartida por ambas versiones.
- `figuras/`: copias de las figuras seleccionadas para el articulo.
- Una copia local de `IEEEtran.cls` si es necesaria para compilar los archivos
  desde la carpeta del articulo.

La carpeta original `IEEE-conference-template-062824/` se conserva como fuente
sin sobrescribir su contenido.

## Titulos

Version en espanol:

> Diseno e implementacion de un monitor de recursos para Linux con Python,
> concurrencia y persistencia SQLite

Version en ingles:

> Design and Implementation of a Linux Resource Monitor Using Python,
> Concurrency, and SQLite Persistence

## Estructura editorial

Ambas versiones conservaran la misma jerarquia y orden:

1. Resumen o Abstract.
2. Palabras clave o Index Terms.
3. Introduccion.
4. Fundamentos y trabajos relacionados.
5. Metodologia.
6. Arquitectura y desarrollo de la solucion.
7. Resultados y validacion.
8. Conclusiones.
9. Referencias.

Los nombres visibles deben cumplir el contenido minimo exigido por la
especificacion del profesor. La arquitectura y el desarrollo se mantienen en
una seccion explicitamente identificable, aunque se dividan en subsecciones
para explicar MVC, fuentes Linux, concurrencia y persistencia.

## Contenido tecnico

El articulo describira los siguientes elementos ya implementados:

- Aplicacion de consola en Python 3 para Linux.
- Lectura directa de `/proc/cpuinfo`, `/proc/stat`, `/proc/loadavg`,
  `/proc/meminfo` y `/proc/net/dev`.
- Uso de `ps`, `who`, `df` e `ip` mediante `subprocess` sin `shell=True`.
- Modulos de CPU, memoria y swap, procesos, usuarios, disco y red.
- Arquitectura Modelo-Vista-Controlador.
- Recoleccion concurrente con seis instancias explicitas de
  `threading.Thread`.
- Proceso hijo con `os.fork()`, comunicacion mediante pipe y recoleccion con
  `os.waitpid()` despues de finalizar los hilos.
- Persistencia SQLite encapsulada en repositorio, claves foraneas activas y
  transaccion atomica para cada captura completa.
- Operaciones CRUD sobre capturas y metadatos.
- Interfaz por teclado con validaciones, limites de listados y mensajes que no
  dependen exclusivamente del color.

## Resultados admisibles

Los resultados se obtendran de `docs/evidencias/logs/` y de la suite ejecutada
en WSL. La version inicial del articulo podra afirmar:

- 56 pruebas ejecutadas correctamente en Ubuntu WSL, sin fallos.
- Recoleccion de los seis modulos con un diccionario de errores vacio en la
  evidencia de estado general.
- Creacion, consulta, actualizacion y eliminacion correctas de una captura en
  una base SQLite temporal, con cero registros restantes al finalizar.
- Finalizacion de los seis hilos de monitoreo y ejecucion del proceso hijo con
  codigo de salida cero.

No se convertiran tiempos casuales de una corrida en resultados de rendimiento
generalizables. No se afirmara compatibilidad con Windows nativo, PostgreSQL,
JSON, interfaces graficas ni privilegios administrativos.

## Figuras y tablas

Se utilizaran como maximo dos figuras para conservar el limite de paginas:

- Diagrama `arquitectura_actual.png`, con la separacion MVC, concurrencia y
  persistencia.
- Una captura de evidencia de WSL, preferentemente la suite completa o la
  demostracion de hilos y `fork()`.

Se incluira una tabla compacta de trazabilidad que relacione fuente Linux,
modulo y dato obtenido, y una tabla de resultados verificados si el espacio lo
permite. Las leyendas y referencias cruzadas se traduciran en cada version.

## Bibliografia

La bibliografia compartida priorizara fuentes primarias y autoritativas:

- Documentacion del kernel Linux y paginas del manual de `/proc`.
- Documentacion oficial de Python para `os.fork`, `threading` y `subprocess`.
- Documentacion oficial de SQLite sobre transacciones y claves foraneas.
- Una referencia academica de sistemas operativos para contextualizar procesos,
  hilos y administracion de recursos, si se dispone de una edicion verificable.

No se conservaran referencias de ejemplo de la plantilla ni citas sin fuente
verificable.

## Equivalencia entre idiomas

La version espanola sera la referencia conceptual inicial. La version inglesa
mantendra las mismas afirmaciones, cifras, figuras, tablas y claves
bibliograficas, pero empleara redaccion academica natural. Los nombres internos
de modulos y campos de la aplicacion se conservaran en espanol cuando sean
identificadores literales del codigo.

## Validacion

Antes de entregar el borrador se comprobara:

- Ausencia de texto instructivo y marcadores de la plantilla IEEE.
- Presencia de todos los autores y secciones obligatorias.
- Igualdad de cifras, tablas, figuras y referencias entre versiones.
- Compilacion de ambos archivos con la clase `IEEEtran` cuando exista una
  herramienta LaTeX disponible.
- Conteo de cuatro a seis paginas para cada PDF generado.
- Ausencia de errores de referencias, figuras cortadas y desbordamientos
  visibles.
- Extraccion a texto para detectar bloques vacios, contenido mezclado entre
  idiomas y marcadores pendientes.

Si no existe compilador LaTeX local o en WSL, se documentara la limitacion sin
presentar la revision visual como completada.

## Fuera de alcance

- Presentacion de diapositivas.
- Guion o grabacion del video.
- Resultados de rendimiento no medidos.
- Cambios funcionales al monitor para producir resultados mas favorables.
- Publicacion externa del articulo.
