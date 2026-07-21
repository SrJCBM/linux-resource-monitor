# Manual de ejecucion

## Inicio

Desde la raiz del repositorio y dentro de Linux o WSL, ejecute:

```bash
python3 main.py
```

La aplicacion muestra un menu principal operable solo con teclado:

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

Despues de consultar un modulo, presione Enter para volver al menu principal.
Una opcion invalida muestra un mensaje de error y permite intentarlo otra vez.

## Monitoreo de recursos

La opcion `1` obtiene el estado general mediante hilos y muestra los resultados
de CPU, memoria, disco, red, procesos y usuarios. Si una fuente falla, se
presenta una advertencia del modulo afectado sin ocultar los resultados que si
se obtuvieron.

Las opciones `2` a `7` muestran cada modulo por separado. Los valores numericos
se presentan con un maximo de dos decimales y los estados de uso se expresan
como `NORMAL`, `ADVERTENCIA` o `CRITICO`; no es necesario usar colores.

Los procesos y sistemas de archivos se limitan en pantalla para mantener la
terminal legible. El numero mostrado indica cuantos registros se ven del total.

En usuarios conectados, la columna de duracion se calcula al presentar la
informacion a partir de `inicio_sesion`; no modifica la sesion ni almacena una
duracion adicional. La fecha que entrega `who` se normaliza a
`YYYY-MM-DD HH:MM` antes de calcular la diferencia con la hora actual, tanto en
la consulta en vivo como al recuperar una captura.

## Historial y CRUD

Seleccione `8` para abrir el historial de capturas.

1. `Registrar captura`: solicita etiqueta y comentario opcionales, recolecta los
   seis modulos y guarda la captura completa en una transaccion SQLite.
2. `Listar capturas`: muestra orden, identificador, fecha y etiqueta en orden
   cronologico ascendente, desde la captura mas antigua hasta la mas reciente.
   Puede filtrar por una fecha real con formato exacto `YYYY-MM-DD`.
3. `Consultar detalle`: solicita un identificador y presenta los valores
   almacenados de la captura.
4. `Actualizar metadatos`: modifica solo etiqueta y comentario; las metricas no
   se editan.
5. `Eliminar captura`: solicita el identificador y exige escribir la palabra
   explicita `SI` antes de eliminarla. La confirmacion no distingue mayusculas
   y minusculas y admite `SI`, `si`, `Si` y `sí`. Cualquier otra
   respuesta cancela la operacion. La eliminacion borra tambien las metricas
   asociadas.
6. `Volver`: regresa al menu principal.

El encabezado del listado distingue ambos valores:

```text
N. | ID | FECHA Y HORA | ETIQUETA
```

`N.` es solo el orden consecutivo de presentacion. `ID` es la clave estable de
SQLite que debe introducirse para consultar, actualizar o eliminar. Mientras
quede al menos una captura, sus IDs no se renumeran al eliminar otra. Cuando el
historial esta completamente vacio, el repositorio limpia cualquier secuencia
`AUTOINCREMENT` residual antes de insertar; por ello, la proxima captura vuelve
a recibir el ID 1 incluso si la base vacia provenia de una ejecucion anterior.

El filtro de fecha valida el formato y el calendario. Entradas como
`2026/07/18`, `18-07-2026` o `2026-02-30` producen un mensaje controlado y el
menu permanece activo; no se interpretan como una busqueda sin resultados.

En el detalle historico, las metricas de disco conservan el mismo contrato que
la consulta en vivo: `espacio_total_bytes`, `espacio_usado_bytes` y
`espacio_libre_bytes`. El repositorio reconstruye esos valores en bytes desde
las columnas persistidas en GB antes de que la Vista los presente.

Una captura no se guarda si falta un modulo obligatorio o si ocurre un error en
la transaccion. La aplicacion informa el problema sin mostrar una traza tecnica.

## Demostracion de concurrencia

Seleccione `9` para mostrar evidencia de hilos y proceso hijo. Primero se
terminan los hilos de monitoreo. Despues se ejecuta `os.fork()` y se muestran el
PID padre, PID hijo y codigo de salida. Esta opcion requiere Linux; no funciona
en Windows sin WSL.

## Cierre y recuperacion

Seleccione `0` para cerrar normalmente. Tambien puede usar `Ctrl+C`; la
aplicacion mostrara un mensaje de cancelacion comprensible.

Para borrar todo el historial local y comenzar de nuevo, cierre la aplicacion y
ejecute:

```bash
rm -f database/data/monitor.sqlite3
```

Este comando elimina solamente el historial local del monitor. No borra datos
del sistema operativo ni modifica procesos, red, memoria o disco.

## Problemas comunes

| Mensaje o situacion | Accion recomendada |
|---|---|
| `/proc` no disponible | Ejecute en Linux o WSL 2, no en Windows nativo. |
| `ip` o `who` no encontrado | Instale las herramientas base de su distribucion o pruebe en Ubuntu. |
| No hay usuarios conectados | Es valido: `who` puede no registrar una sesion interactiva. |
| No hay direccion IP en una interfaz | Es valido para interfaces sin configuracion de red. |
| La demostracion de fork falla | Compruebe que usa Linux y que no ejecuto la opcion desde un entorno no compatible. |
| La base de datos esta bloqueada | Cierre otras instancias del monitor y vuelva a intentar. |
