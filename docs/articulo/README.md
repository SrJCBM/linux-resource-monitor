# Articulo IEEE bilingue

Esta carpeta contiene las dos versiones listas para usar del articulo cientifico
del proyecto Linux Resource Monitor. Ambas describen la misma implementacion,
usan las mismas cifras, figuras, tablas, citas y bibliografia, y conservan el
formato IEEE de conferencia.

## Archivos

| Archivo | Proposito |
|---|---|
| monitor_recursos_linux_es.tex | Fuente completa en espanol. |
| monitor_recursos_linux_es.pdf | PDF final en espanol, 4 paginas. |
| linux_resource_monitor_en.tex | Fuente completa en ingles. |
| linux_resource_monitor_en.pdf | PDF final en ingles, 4 paginas. |
| referencias.bib | Bibliografia BibTeX compartida. |
| IEEEtran.cls | Clase IEEE local para compilacion autocontenida. |
| figuras/arquitectura_actual.png | Arquitectura MVC y flujo del sistema. |
| figuras/evidencia_hilos_fork.png | Evidencia WSL de hilos y proceso hijo. |

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

El 17 de julio de 2026 se compilaron ambos fuentes con Tectonic 0.16.9. Cada PDF
tiene 4 paginas Letter. El conteo se verifico con pdfinfo:

    pdfinfo monitor_recursos_linux_es.pdf | Select-String '^Pages:'
    pdfinfo linux_resource_monitor_en.pdf | Select-String '^Pages:'

Para repetir la revision visual, renderice todas las paginas en una carpeta
temporal:

    pdftoppm -png -r 144 monitor_recursos_linux_es.pdf "$env:TEMP\monitor_es_page"
    pdftoppm -png -r 144 linux_resource_monitor_en.pdf "$env:TEMP\monitor_en_page"

Se inspeccionaron las ocho paginas resultantes. No se observaron columnas
cortadas, sobreimpresiones, desbordamientos de tablas, referencias sin resolver,
texto de plantilla ni huecos anormales. Los archivos .log, .blg, .aux, .bbl,
.out, renders PNG y binarios de herramientas son auxiliares locales y no forman
parte de los entregables versionados.
