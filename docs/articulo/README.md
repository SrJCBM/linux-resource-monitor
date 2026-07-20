# Articulo IEEE bilingue

Esta carpeta contiene las dos versiones listas para usar del articulo cientifico
del proyecto Linux Resource Monitor. Ambas describen la misma implementacion,
usan las mismas cifras, figuras, tablas, citas y bibliografia, y conservan el
formato IEEE de conferencia.

## Archivos

| Archivo | Proposito |
|---|---|
| monitor_recursos_linux_es.tex | Fuente completa en espanol. |
| monitor_recursos_linux_es.pdf | PDF final en espanol, 5 paginas Letter. |
| linux_resource_monitor_en.tex | Fuente completa en ingles. |
| linux_resource_monitor_en.pdf | PDF final en ingles, 5 paginas Letter. |
| referencias.bib | Bibliografia BibTeX compartida. |
| IEEEtran.cls | Clase IEEE local para compilacion autocontenida. |
| figuras/arquitectura_actual.png | Arquitectura MVC y flujo del sistema. |
| figuras/evidencia_estado_general_ubuntu.png | Evidencia positiva del estado general en Ubuntu. |
| figuras/evidencia_crud_ubuntu.png | Evidencia diagnostica CRUD previa a las correcciones. |
| figuras/evidencia_concurrencia_ubuntu.png | Evidencia positiva de hilos y proceso hijo en Ubuntu. |

`figuras/evidencia_hilos_fork.png` se conserva como imagen historica, pero las
versiones actuales de los articulos no la referencian.

## Evidencia funcional final

La ejecucion final documentada despues de incorporar tres pruebas de regresion
para casos limite produjo estos resultados exactos:

| Entorno | Resultado | Tiempo |
|---|---|---:|
| Windows | 69 pruebas correctas, 2 omitidas por ser exclusivas de Linux | 0.261 s |
| Ubuntu WSL | 69 pruebas correctas, 0 fallos y 0 omisiones | 0.870 s |

Las omisiones de Windows corresponden solamente a integraciones que requieren
Linux. La suite completa de Ubuntu es la evidencia automatizada de las cinco
correcciones descritas en los articulos.

## Procedencia de las figuras

La figura de arquitectura representa el MVC y el flujo implementado en el
repositorio. Las tres capturas de Ubuntu se recortaron y reescalaron sin retocar
el contenido mostrado por la terminal en `Estado general.pdf`, creado el 18 de
julio de 2026 a partir de una validacion manual en Ubuntu:

- `evidencia_estado_general_ubuntu.png` procede de la pagina 1 y muestra CPU,
  memoria, disco y red; se usa como evidencia positiva de monitoreo.
- `evidencia_crud_ubuntu.png` combina recortes de las paginas 4, 5 y 7. Conserva
  el encabezado anterior `ID | ...` y el ID 2 posterior a una eliminacion, por
  lo que se rotula exclusivamente como evidencia diagnostica previa a las
  correcciones, no como prueba de la interfaz final.
- `evidencia_concurrencia_ubuntu.png` procede de la pagina 8 y muestra seis
  hilos, cero errores, PID padre e hijo y estado de salida cero; se usa como
  evidencia positiva de concurrencia.

## Compilacion con Tectonic

Ejecute los comandos desde docs/articulo/. Tectonic resuelve BibTeX y las
pasadas adicionales de referencias de forma automatica.

    tectonic -X compile monitor_recursos_linux_es.tex
    tectonic -X compile linux_resource_monitor_en.tex

La validacion final se realizo con Tectonic oficial 0.16.9. En el equipo de
trabajo se uso el binario portable:

    $tectonic = 'C:\Users\jcbla\AppData\Local\Temp\codex-tools\tectonic-0.16.9\tectonic.exe'
    & $tectonic -X compile --keep-logs monitor_recursos_linux_es.tex
    & $tectonic -X compile --keep-logs linux_resource_monitor_en.tex

## Compilacion con latexmk

Una instalacion TeX que incluya IEEEtran, booktabs, balance, hyperref y BibTeX
puede reproducir los PDF con:

    latexmk -pdf -interaction=nonstopmode -halt-on-error monitor_recursos_linux_es.tex
    latexmk -pdf -interaction=nonstopmode -halt-on-error linux_resource_monitor_en.tex

Para retirar auxiliares generados por latexmk sin eliminar los PDF:

    latexmk -c monitor_recursos_linux_es.tex
    latexmk -c linux_resource_monitor_en.tex

## Validacion estructural con Pandoc

Pandoc se usa como comprobacion de extraccion y no como compilador del formato
IEEE. Desde la raiz del repositorio:

    pandoc -f latex -t plain docs/articulo/monitor_recursos_linux_es.tex -o "$env:TEMP\monitor_es.txt"
    pandoc -f latex -t plain docs/articulo/linux_resource_monitor_en.tex -o "$env:TEMP\monitor_en.txt"

Pandoc puede advertir que conserva la ecuacion de utilizacion de CPU como TeX;
esa advertencia no impide la extraccion ni la compilacion con LaTeX.

Los marcadores de plantilla o edicion pueden comprobarse con:

    rg -n 'Conference Paper Title|Given Name|Identify applicable|TODO|TBD|placeholder' docs/articulo -g '*.tex'

El comando debe terminar sin coincidencias.

## Conteo y revision visual

El 20 de julio de 2026 se compilaron ambos fuentes con Tectonic 0.16.9. Cada PDF
tiene 5 paginas Letter. El conteo se verifico con pdfinfo:

    pdfinfo monitor_recursos_linux_es.pdf | Select-String '^Pages:'
    pdfinfo linux_resource_monitor_en.pdf | Select-String '^Pages:'

Para repetir la revision visual, renderice todas las paginas en una carpeta
temporal:

    pdftoppm -png -r 144 monitor_recursos_linux_es.pdf "$env:TEMP\monitor_es_page"
    pdftoppm -png -r 144 linux_resource_monitor_en.pdf "$env:TEMP\monitor_en_page"

Se inspeccionaron las diez paginas resultantes. No se observaron columnas
cortadas, sobreimpresiones, desbordamientos de tablas, referencias sin resolver,
texto de plantilla ni huecos anormales. Los logs no registraron cajas
`Overfull`, citas indefinidas ni referencias indefinidas. Los archivos .log,
.blg, .aux, .bbl,
.out, renders PNG y binarios de herramientas son auxiliares locales y no forman
parte de los entregables versionados.
