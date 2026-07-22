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
| ../evidencias/capturas/ | Capturas finales e indice completo de las opciones del programa. |

Las figuras antiguas de ejecucion se conservan en `figuras/` como material
historico. Las versiones actuales solo referencian la arquitectura y seis
capturas finales procedentes de `../evidencias/capturas/`.

## Evidencia funcional final

La ejecucion final documentada despues de incorporar tres pruebas de regresion
para casos limite produjo estos resultados exactos:

| Entorno | Resultado | Tiempo |
|---|---|---:|
| Windows | 71 pruebas correctas, 2 omitidas por ser exclusivas de Linux | 0.339 s |
| Ubuntu WSL | 71 pruebas correctas, 0 fallos y 0 omisiones | 0.615 s |

Las omisiones de Windows corresponden solamente a integraciones que requieren
Linux. La suite completa de Ubuntu complementa el recorrido manual realizado en
una instalacion limpia de Ubuntu sobre las nueve opciones del menu.

## Procedencia de las figuras

La figura de arquitectura representa el MVC y el flujo implementado en el
repositorio. La figura final de ambos articulos agrupa seis capturas tomadas en
una ejecucion manual del clon limpio sobre Ubuntu, sin modificar el contenido
mostrado por la terminal:

- `05`, `06` y `07` documentan el estado general: CPU, memoria, disco, red,
  procesos y usuarios conectados.
- `14` y `15` muestran el registro de las capturas 1 y 2, el listado cronologico
  ascendente y la actualizacion de la etiqueta del ID 1.
- `17` muestra seis hilos completados, cero errores, PID padre e hijo distintos
  y codigo de salida cero.

Las capturas individuales `08` a `13` permanecen en el indice de evidencias para
revisar por separado las opciones 2 a 7. La captura `16` conserva el texto del
filtro anterior a la correccion y se mantiene unicamente como antecedente; no se
usa en los PDF finales.

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

El 22 de julio de 2026 se compilaron ambos fuentes con Tectonic 0.16.9. Cada PDF
tiene 5 paginas Letter. El conteo se verifico con pdfinfo:

    pdfinfo monitor_recursos_linux_es.pdf | Select-String '^Pages:'
    pdfinfo linux_resource_monitor_en.pdf | Select-String '^Pages:'

Para repetir la revision visual, renderice todas las paginas en una carpeta
temporal:

    pdftoppm -png -r 144 monitor_recursos_linux_es.pdf "$env:TEMP\monitor_es_page"
    pdftoppm -png -r 144 linux_resource_monitor_en.pdf "$env:TEMP\monitor_en_page"

Se inspeccionaron las diez paginas resultantes, incluida la lamina final de seis
paneles con tres capturas de igual ancho por fila y leyendas alineadas. No se
observaron columnas cortadas, sobreimpresiones, desbordamientos de tablas,
referencias sin resolver ni texto de plantilla. La ultima pagina conserva la
lamina de evidencia centrada como flotante de doble columna de IEEEtran. Los
logs no registraron cajas
`Overfull`, citas indefinidas ni referencias indefinidas. Los archivos .log,
.blg, .aux, .bbl,
.out, renders PNG y binarios de herramientas son auxiliares locales y no forman
parte de los entregables versionados.
