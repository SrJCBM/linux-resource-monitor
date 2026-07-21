# Diseno de correcciones de incidencias y evidencias Ubuntu

## Objetivo

Corregir las incidencias observadas durante la validacion manual en Ubuntu,
conservar la integridad del modelo SQLite y actualizar los dos articulos IEEE
con evidencias visuales legibles extraidas de Estado general.pdf.

El cambio no agrega modulos ni dependencias de ejecucion. Se limita al flujo
CRUD, los contratos de usuarios y disco, las pruebas de regresion, las
capturas del articulo y la documentacion tecnica relacionada.

## Evidencia analizada

El PDF contiene ocho paginas de ejecucion manual en Ubuntu. Las capturas
confirman el funcionamiento de CPU, memoria, procesos, disco, red, usuarios,
CRUD, hilos y fork(). Tambien muestran estas incidencias:

1. Escribir si en minusculas cancela la eliminacion, mientras SI funciona.
2. El filtro acepta visualmente 2026/07/18, pero devuelve una lista vacia sin
   explicar que el formato es invalido.
3. Tras eliminar la unica captura, la siguiente recibe ID 2; el listado no
   ofrece una numeracion consecutiva independiente del identificador interno.
4. La consulta en vivo de usuarios muestra No disponible como duracion cuando
   who entrega una fecha como Jul 18 15:54.
5. El detalle persistido muestra los tamanos de disco como 0.00 GB, aunque la
   vista en vivo muestra valores distintos de cero.

## Causas raiz

### Confirmacion de eliminacion

view/menu_view.py compara la entrada con la cadena exacta SI. La comparacion
distingue mayusculas, minusculas y la variante acentuada.

### Filtro de fecha

CrudController.listar_capturas() delega cualquier texto al repositorio. La
consulta usa LIKE, por lo que una fecha con separadores incorrectos no produce
un error controlado: simplemente no coincide con ninguna fila.

### Identificadores y numeracion

capturas.id_captura usa AUTOINCREMENT. SQLite no reutiliza normalmente un
identificador eliminado. Renumerar filas existentes seria inseguro porque el
ID es una clave estable referenciada por seis familias de metricas.

La interfaz presenta solo el ID y no distingue entre la posicion visual de una
fila y su identificador persistente.

### Duracion de usuarios

usuarios_model.parse_who_output() conserva el formato abreviado de who cuando
LC_ALL=C, por ejemplo Jul 18 15:54. La Vista calcula la duracion solo con
fechas ISO, por lo que una consulta en vivo no puede interpretarlo. El
repositorio si normaliza el valor al persistirlo, lo que explica por que el
detalle historico funciona y la vista en vivo no.

### Disco persistido

El modelo de disco usa las claves espacio_*_bytes. SQLite almacena esos
valores convertidos a columnas espacio_*_gb. Al leer una captura, el
repositorio devuelve directamente los nombres de las columnas de la base,
pero format_disco_info() sigue esperando el contrato en bytes. El valor
ausente se formatea como cero.

## Diseno funcional

### Listado e identificadores

El listado mostrara:

    N. | ID | FECHA Y HORA | ETIQUETA

N. se recalcula desde 1 en cada listado y sirve solo como posicion visual. ID
sigue siendo la clave que se introduce para consultar, actualizar o eliminar.
Las capturas se muestran en orden cronologico ascendente, de la mas antigua a
la mas reciente; si coinciden en fecha y hora, el ID resuelve el orden.
Antes de esas tres operaciones, la Vista mostrara el listado actual; si esta
vacio, no solicitara un identificador.

No se renumeraran capturas existentes. Cuando una eliminacion deje la tabla
capturas completamente vacia, el repositorio reiniciara solo la secuencia de
esa tabla dentro de la misma transaccion. La siguiente captura volvera a ID 1.
Antes de insertar en un historial ya vacio, tambien se eliminara una secuencia
residual que pudiera proceder de una version o eliminacion anterior.
No se modificaran secuencias mientras permanezca al menos una captura.

### Confirmacion de borrado

La confirmacion aceptara SI, si, Si y si con tilde, despues de eliminar
espacios y normalizar la capitalizacion. Cualquier otro texto cancelara la
operacion. La accion seguira requiriendo una confirmacion explicita.

### Fecha

El Controlador validara que un filtro no vacio use exactamente YYYY-MM-DD y
represente una fecha real. Una entrada como 2026/07/18, 2026-02-30 o
18-07-2026 generara un ValueError controlado. La Vista mostrara el mensaje y
mantendra activo el menu.

### Usuarios

El Modelo normalizara inicio_sesion a YYYY-MM-DD HH:MM al interpretar la
salida de who. Para formatos sin ano, usara el ano local actual y el ano
anterior cuando el resultado calculado quedaria en el futuro. La funcion de
normalizacion aceptara una referencia temporal inyectable para que las pruebas
sean deterministas.

El repositorio reutilizara esa misma normalizacion como defensa para datos que
no provengan del recolector normal.

### Disco

SQLite conservara sus columnas en GB, de acuerdo con el esquema aprobado. Al
reconstruir una captura, el repositorio convertira espacio_total_gb,
espacio_usado_gb y espacio_libre_gb al contrato estable
espacio_total_bytes, espacio_usado_bytes y espacio_libre_bytes. La Vista
recibira el mismo contrato tanto en vivo como desde el historial.

## Evidencias para los articulos

Se extraeran del PDF, sin alterar el contenido de terminal, tres imagenes:

- evidencia_estado_general_ubuntu.png: CPU, memoria, disco y red.
- evidencia_crud_ubuntu.png: registro, listado, actualizacion y eliminacion.
- evidencia_concurrencia_ubuntu.png: seis hilos, cero errores y proceso hijo
  con estado de salida cero.

Las imagenes se recortaran desde renders de alta resolucion y se guardaran en
docs/articulo/figuras/. No se incluiran las anotaciones que describen fallos ya
corregidos como si fueran evidencia positiva.

Los articulos en espanol e ingles mantendran las mismas figuras, resultados,
secciones, citas y afirmaciones. Se reemplazara la captura antigua de
concurrencia y se agregara evidencia de estado general y CRUD solo si cada PDF
permanece entre cuatro y seis paginas y las capturas son legibles.

## Pruebas

Se agregaran pruebas de regresion para:

- confirmacion de eliminacion en minusculas y con tilde;
- rechazo de filtros de fecha con formato o calendario invalidos;
- listado con numero consecutivo e ID persistente;
- ausencia de solicitud de ID cuando no hay capturas;
- reinicio de capturas cuando la tabla queda vacia;
- preservacion de IDs cuando aun existen capturas;
- normalizacion determinista de fechas abreviadas de who;
- duracion calculable en la vista en vivo;
- reconstruccion del contrato de disco en bytes despues de crear y consultar.

La suite completa se ejecutara en Windows y en Ubuntu WSL. Las pruebas
exclusivas de Linux deben pasar en WSL sin privilegios de administrador.

## Documentacion

Se actualizaran:

- README.md: comportamiento del historial, confirmacion y evidencias;
- docs/manual_ejecucion.md: formato de fecha, diferencia entre N. e ID,
  reinicio al vaciar el historial y confirmacion no sensible a mayusculas;
- docs/evidencias/README.md: procedencia y alcance de las nuevas capturas;
- docs/articulo/README.md: figuras, compilacion y conteo final;
- ambos archivos tex: resultados verificados y figuras equivalentes;
- docstrings y anotaciones publicas de los modulos modificados.

El esquema SQL y la arquitectura MVC no cambian. La documentacion no afirmara
que los IDs se renumeran mientras existan capturas ni que las capturas
constituyen una prueba de rendimiento.

## Criterios de aceptacion

- Una eliminacion confirmada con si, SI o si con tilde se ejecuta.
- Las fechas invalidas reciben un mensaje controlado y no consultan SQLite.
- Los listados comienzan su columna N. en 1 y conservan el ID real.
- Al vaciar el historial, la siguiente captura recibe ID 1.
- Con capturas restantes, ningun ID existente cambia.
- La duracion de usuarios se presenta en vivo con una fecha valida de who.
- El detalle historico de disco coincide, dentro de la precision de dos
  decimales, con los valores guardados.
- Ambas suites pasan y los dos PDF IEEE quedan entre cuatro y seis paginas sin
  cortes, superposiciones ni referencias sin resolver.
