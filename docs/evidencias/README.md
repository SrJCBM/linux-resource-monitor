# Indice de evidencias

Los logs de esta carpeta se generan con resultados reales de Ubuntu WSL. No se
deben editar para cambiar un resultado; si un caso falla, se conserva el codigo
de salida y el error para poder corregirlo y repetir la ejecucion.

## Procedencia de la validacion manual

El archivo fuente `Estado general.pdf` fue creado el 2026-07-18 y contiene ocho
paginas de capturas obtenidas durante una validacion manual en Ubuntu. Su alcance
incluye CPU, memoria, procesos, disco, red, usuarios, CRUD, hilos y `fork()`.

Se extrajeron y verificaron, sin modificar el contenido de la terminal, estas
tres figuras para los articulos IEEE:

- `docs/articulo/figuras/evidencia_estado_general_ubuntu.png`: CPU, memoria,
  disco y red.
- `docs/articulo/figuras/evidencia_crud_ubuntu.png`: secuencia diagnostica de
  registro, listado, actualizacion y eliminacion anterior a las correcciones.
- `docs/articulo/figuras/evidencia_concurrencia_ubuntu.png`: seis hilos, cero
  errores, PID padre e hijo y estado de salida cero.

Las figuras de estado general y concurrencia son evidencia positiva de ejecucion
en Ubuntu. La figura CRUD conserva el encabezado y el comportamiento de IDs
observados antes de corregirlos, por lo que los articulos la identifican como
evidencia diagnostica y no como representacion de la interfaz final. Las
anotaciones del PDF que describen formatos invalidos, cancelaciones inesperadas,
IDs o valores incorrectos no se presentan como evidencia positiva.

## Generar logs

Desde Ubuntu WSL, en la raiz del repositorio:

```bash
python3 scripts/generar_evidencias.py
```

El comando crea o reemplaza los archivos de `logs/` con la salida actual del
equipo. Cada archivo contiene fecha UTC, comando, codigo de salida, salida
estandar y salida de error.

| Log | Requisitos demostrados | Contenido esperado |
|---|---|---|
| `01_suite_completa.txt` | RNF-01, RNF-06, RNF-09 | Todas las pruebas de Linux pasan. |
| `02_estado_general.txt` | RF-01 a RF-06, RF-08 | Seis modulos recolectados, errores parciales si existen y conteos reales. |
| `03_crud_sqlite.txt` | RF-09 a RF-12, RNF-03, RNF-13, RNF-14 | Identificador creado, actualizacion, eliminacion y cero capturas restantes. |
| `04_hilos_y_fork.txt` | RF-07, RF-08, RNF-07 | Evidencias de hilos, PID padre/hijo, pipe y salida correcta. |

## Capturas manuales de Ubuntu

Las opciones 1 a 9 del menu principal se validaron manualmente el 2026-07-22
en un clon ejecutado directamente en Ubuntu. La opcion de estado general ocupa
tres imagenes para conservar la legibilidad de todos los modulos.

| Captura | Opcion y contenido |
|---|---|
| `05_opcion_1_estado_general_cpu_memoria.png` | Opcion 1: fecha de actualizacion, CPU y memoria. |
| `06_opcion_1_estado_general_disco_red.png` | Opcion 1: disco y red. |
| `07_opcion_1_estado_general_procesos_usuarios.png` | Opcion 1: procesos y usuarios conectados. |
| `08_opcion_2_cpu.png` | Opcion 2: CPU. |
| `09_opcion_3_memoria_swap.png` | Opcion 3: memoria y swap. |
| `10_opcion_4_procesos.png` | Opcion 4: procesos. |
| `11_opcion_5_disco.png` | Opcion 5: sistemas de archivos montados. |
| `12_opcion_6_red.png` | Opcion 6: interfaces y contadores de red. |
| `13_opcion_7_usuarios_conectados.png` | Opcion 7: sesiones y duracion de conexion. |
| `14_opcion_8_crud_registro_capturas.png` | Opcion 8: registro consecutivo de las capturas 1 y 2. |
| `15_opcion_8_crud_listado_actualizacion.png` | Opcion 8: orden ascendente y actualizacion de metadatos. |
| `16_opcion_8_crud_eliminacion_filtro.png` | Opcion 8: eliminacion confirmada y filtro valido sin coincidencias. |
| `17_opcion_9_concurrencia_hilos_fork.png` | Opcion 9: seis hilos, PID padre/hijo y salida cero. |

La captura `16_opcion_8_crud_eliminacion_filtro.png` se obtuvo antes de ajustar
el texto del resultado filtrado. Evidencia la eliminacion y una consulta sin
coincidencias, pero no se usa para demostrar la redaccion final del mensaje.

## Capturas de Windows Terminal

Las capturas literales se guardan en `capturas/`. Deben mostrar solo la ventana
dedicada de Windows Terminal ejecutando los mismos comandos de los logs.

Antes de conservar una imagen, compruebe que no expone otras ventanas, nombres
de usuario no necesarios, rutas privadas o datos ajenos al proyecto. Si la
captura automatica no identifica una unica ventana dedicada, use `Win+Shift+S`
y seleccione exclusivamente la terminal.

| Captura sugerida | Comando o log asociado |
|---|---|
| `01_pruebas_wsl.png` | `01_suite_completa.txt` |
| `02_estado_general.png` | `02_estado_general.txt` |
| `03_crud.png` | `03_crud_sqlite.txt` |
| `04_hilos_fork.png` | `04_hilos_y_fork.txt` |

La arquitectura del sistema se documenta en `arquitectura_actual.png`.

## Captura automatica segura

Abra una ventana dedicada de Windows Terminal para cada caso. Muestre el log
correspondiente desde WSL y deje la ventana visible. Use rutas absolutas y
entre comillas: asi funciona tambien cuando la ruta contiene espacios.

```powershell
wt.exe -w new wsl.exe -d Ubuntu -- bash "<ruta-en-wsl>/scripts/mostrar_evidencia.sh" "<ruta-en-wsl>/docs/evidencias/logs/01_suite_completa.txt"
```

Identifique la ventana dedicada por su PID exacto y capturela desde otra consola
PowerShell:

```powershell
Get-Process WindowsTerminal | Select-Object Id,MainWindowTitle
powershell.exe -ExecutionPolicy Bypass -File scripts/capturar_ventana_terminal.ps1 `
  -ProcessId <pid-de-la-terminal-dedicada> `
  -Salida "docs/evidencias/capturas/01_pruebas_wsl.png"
```

El script falla si el PID no identifica exactamente una ventana y recorta el
marco transparente de Windows Terminal. No existe una alternativa automatica
de pantalla completa. En ese caso, use `Win+Shift+S` y seleccione solo el
rectangulo de Windows Terminal.
