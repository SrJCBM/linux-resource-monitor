# Indice de evidencias

Los logs de esta carpeta se generan con resultados reales de Ubuntu WSL. No se
deben editar para cambiar un resultado; si un caso falla, se conserva el codigo
de salida y el error para poder corregirlo y repetir la ejecucion.

## Procedencia de la validacion manual

El archivo fuente `Estado general.pdf` fue creado el 2026-07-18 y contiene ocho
paginas de capturas obtenidas durante una validacion manual en Ubuntu. Su alcance
incluye CPU, memoria, procesos, disco, red, usuarios, CRUD, hilos y `fork()`.

Se planifica extraer, sin modificar el contenido de la terminal, estas tres
figuras para los articulos IEEE:

- `docs/articulo/figuras/evidencia_estado_general_ubuntu.png`: CPU, memoria,
  disco y red.
- `docs/articulo/figuras/evidencia_crud_ubuntu.png`: registro, listado,
  actualizacion y eliminacion.
- `docs/articulo/figuras/evidencia_concurrencia_ubuntu.png`: seis hilos, cero
  errores, PID padre e hijo y estado de salida cero.

Estas imagenes estan planificadas y no se consideran disponibles hasta que sean
extraidas y verificadas. Las anotaciones del PDF que describen formatos
invalidos, cancelaciones inesperadas, IDs o valores incorrectos sirven para
diagnosticar fallos; no se presentan como evidencia positiva de funcionamiento.

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
