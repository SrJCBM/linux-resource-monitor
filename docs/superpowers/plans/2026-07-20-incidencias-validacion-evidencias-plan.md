# Ubuntu Incident Corrections and Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Correct the five Ubuntu validation incidents, preserve safe SQLite identifiers, add regression coverage, and refresh both IEEE articles with legible evidence extracted from the supplied PDF.

**Architecture:** Models continue returning stable dictionaries and lists, the Controller validates business input before repository access, the View formats and guides keyboard interaction, and SQLite remains the only persistence engine. Database columns keep their approved units while the repository reconstructs the live Model contract on reads.

**Tech Stack:** Python 3 standard library, unittest, SQLite, Linux who/df/proc interfaces, LaTeX IEEEtran, Tectonic, Poppler, and temporary Pillow-based cropping from the supplied PDF.

## Global Constraints

- Preserve MVC and the existing Spanish module names.
- Add no application runtime dependency.
- Keep SQLite columns and database/esquema.sql unchanged.
- Do not renumber existing capture IDs while rows remain.
- Reset only the capturas sequence and only when capturas becomes empty.
- Keep both article versions equivalent in claims, figures, tables, citations, and result values.
- Keep each final IEEE PDF between four and six pages.
- Do not commit the uploaded IEEE template directory or temporary PDF renders.
- Follow test-driven development: every production behavior change begins with a failing regression test.
- Run the complete suite on Windows and Ubuntu WSL before completion.

---

## Task 1: Normalize Live User Login Times

**Files:**
- Modify: model/usuarios_model.py
- Modify: model/repositorio.py
- Test: tests/unit/test_usuarios_model.py
- Test: tests/unit/test_consola_view.py
- Test: tests/unit/test_repositorio.py

**Interfaces:**
- Produces: normalizar_inicio_sesion(valor: object, ahora: datetime | None = None) -> str | None
- Produces: parse_who_output(text: str, ahora: datetime | None = None) -> list[dict[str, str]]
- Consumes: format_usuarios_info() already accepts ISO-compatible inicio_sesion values.

- [ ] **Step 1: Add failing parser and live-duration tests**

Add deterministic cases:

    def test_parse_who_output_normalizes_month_name_for_live_duration(self):
        text = "ariel seat0 Jul 18 15:54\n"
        result = usuarios_model.parse_who_output(
            text, ahora=datetime(2026, 7, 18, 17, 11)
        )
        self.assertEqual(result[0]["inicio_sesion"], "2026-07-18 15:54")

    def test_parse_who_output_uses_previous_year_for_future_candidate(self):
        text = "ariel seat0 Dec 31 23:59\n"
        result = usuarios_model.parse_who_output(
            text, ahora=datetime(2026, 1, 1, 0, 10)
        )
        self.assertEqual(result[0]["inicio_sesion"], "2025-12-31 23:59")

Add a View assertion that the normalized first value renders as 1 h 17 min at
2026-07-18 17:11.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

    python -m unittest tests.unit.test_usuarios_model tests.unit.test_consola_view

Expected: the month-name parser test fails because parse_who_output currently
returns Jul 18 15:54 and does not accept ahora.

- [ ] **Step 3: Implement one shared normalization function**

In model/usuarios_model.py:

    MESES_WHO = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
                 "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                 "Nov": 11, "Dec": 12}

    def normalizar_inicio_sesion(
        valor: object, ahora: datetime | None = None
    ) -> str | None:
        if valor is None:
            return None
        texto = str(valor).strip()
        if not texto:
            return None

        try:
            return datetime.strptime(texto, "%Y-%m-%d %H:%M").strftime(
                "%Y-%m-%d %H:%M"
            )
        except ValueError:
            pass

        partes = texto.split()
        if len(partes) != 3 or partes[0] not in MESES_WHO:
            return None
        try:
            mes = MESES_WHO[partes[0]]
            dia = int(partes[1])
            hora, minuto = (int(parte) for parte in partes[2].split(":"))
            referencia = ahora or datetime.now()
            candidato = datetime(referencia.year, mes, dia, hora, minuto)
        except (TypeError, ValueError):
            return None

        if candidato > referencia + timedelta(days=1):
            candidato = candidato.replace(year=referencia.year - 1)
        return candidato.strftime("%Y-%m-%d %H:%M")

The function must accept None, strict ISO minute text, and month-name text.
Month-name candidates more than one day in the future use the previous year.
parse_who_output normalizes before appending each dictionary.

Import this function in model/repositorio.py and remove its duplicate
MESES_WHO and _normalizar_inicio_sesion implementation. Persistence uses the
same helper as a defensive boundary.

- [ ] **Step 4: Run user and repository tests and verify GREEN**

Run:

    python -m unittest tests.unit.test_usuarios_model tests.unit.test_consola_view tests.unit.test_repositorio

Expected: all selected tests pass and live month-name sessions are ISO.

- [ ] **Step 5: Commit**

    git add model/usuarios_model.py model/repositorio.py tests/unit/test_usuarios_model.py tests/unit/test_consola_view.py tests/unit/test_repositorio.py
    git commit -m "fix: normalize live user session times"

## Task 2: Reconstruct Persisted Disk Metrics

**Files:**
- Modify: model/repositorio.py
- Test: tests/unit/test_repositorio.py
- Test: tests/unit/test_menu_view.py

**Interfaces:**
- Consumes: SQLite rows with espacio_total_gb, espacio_usado_gb, and espacio_libre_gb.
- Produces: disk dictionaries with espacio_total_bytes, espacio_usado_bytes, and espacio_libre_bytes, matching model/disco_model.py.

- [ ] **Step 1: Change the round-trip expectation to the stable byte contract**

In test_crear_y_obtener_captura_completa replace the direct GB assertion with:

    disco = captura["discos"][0]
    self.assertEqual(disco["espacio_total_bytes"], 1073741824)
    self.assertEqual(disco["espacio_usado_bytes"], 536870912)
    self.assertEqual(disco["espacio_libre_bytes"], 536870912)
    self.assertNotIn("espacio_total_gb", disco)

Add a menu-detail assertion that the persisted disk record renders 1.00 GB
total and 0.50 GB used rather than 0.00 GB.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

    python -m unittest tests.unit.test_repositorio tests.unit.test_menu_view

Expected: the repository assertion fails because the returned row still uses
espacio_total_gb.

- [ ] **Step 3: Add repository reconstruction**

Add a focused helper:

    def _reconstruir_disco(fila: dict[str, Any]) -> dict[str, Any]:
        resultado = dict(fila)
        resultado["espacio_total_bytes"] = round(
            float(resultado.pop("espacio_total_gb")) * BYTES_POR_GB
        )
        resultado["espacio_usado_bytes"] = round(
            float(resultado.pop("espacio_usado_gb")) * BYTES_POR_GB
        )
        resultado["espacio_libre_bytes"] = round(
            float(resultado.pop("espacio_libre_gb")) * BYTES_POR_GB
        )
        resultado.pop("id_disco_metrica", None)
        return resultado

Use it only for disco_metricas in obtener_captura(). Keep the database schema
and write conversion unchanged.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run:

    python -m unittest tests.unit.test_repositorio tests.unit.test_menu_view

Expected: all selected tests pass and the detail formatter receives bytes.

- [ ] **Step 5: Commit**

    git add model/repositorio.py tests/unit/test_repositorio.py tests/unit/test_menu_view.py
    git commit -m "fix: restore persisted disk data contract"

## Task 3: Validate CRUD Input and Improve Capture Numbering

**Files:**
- Modify: controller/crud_controller.py
- Modify: model/repositorio.py
- Modify: view/menu_view.py
- Test: tests/unit/test_crud_controller.py
- Test: tests/unit/test_menu_view.py
- Test: tests/unit/test_repositorio.py

**Interfaces:**
- Produces: CrudController.listar_capturas(fecha) rejects non-ISO or impossible dates with ValueError.
- Produces: numbered display N. | ID | FECHA Y HORA | ETIQUETA.
- Produces: RepositorioCapturas.eliminar_captura() resets sqlite_sequence for capturas only when no captures remain.

- [ ] **Step 1: Add failing controller date tests**

Add tests asserting that 2026/07/18, 18-07-2026, and 2026-02-30 raise
ValueError and never invoke the fake repository. Keep 2026-07-18 and None as
accepted values.

- [ ] **Step 2: Add failing menu behavior tests**

Cover these independent cases:

    entradas = iter(["5", "7", "si", "0"])
    self.assertEqual(controlador.eliminados, [7])

    entradas = iter(["5", "7", "sí", "0"])
    self.assertEqual(controlador.eliminados, [7])

Assert _mostrar_listado output begins with:

    N. | ID | FECHA Y HORA | ETIQUETA
    1 | 9 | 2026-07-18 10:00:00 | antes
    2 | 4 | 2026-07-18 11:00:00 | despues

For consult, update, and delete, assert the current list is shown before the
ID prompt. When the fake returns an empty list, assert the menu emits No hay
capturas almacenadas and consumes no ID input.

- [ ] **Step 3: Add failing sequence tests**

Add one test that creates ID 1, deletes it, creates again, and expects ID 1.
Add another that creates IDs 1 and 2, deletes ID 1, creates again, and expects
ID 3 while ID 2 remains unchanged.

- [ ] **Step 4: Run focused tests and verify RED**

Run:

    python -m unittest tests.unit.test_crud_controller tests.unit.test_menu_view tests.unit.test_repositorio

Expected failures: invalid dates reach the repository, lowercase si cancels,
the list lacks N., and an empty table creates ID 2.

- [ ] **Step 5: Implement strict date validation**

Use a compiled regular expression and datetime.strptime in
CrudController.listar_capturas():

    if fecha is not None:
        fecha = fecha.strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
            raise ValueError(
                "La fecha debe usar el formato YYYY-MM-DD y ser valida."
            )
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError(
                "La fecha debe usar el formato YYYY-MM-DD y ser valida."
            ) from error

Raise the same controlled message for either syntax or calendar errors:

    ValueError("La fecha debe usar el formato YYYY-MM-DD y ser valida.")

Do not call the repository when validation fails.

- [ ] **Step 6: Implement menu guidance and confirmation normalization**

Add `_mostrar_capturas_disponibles()` in MenuView. It calls
`controlador.listar_capturas()`, emits `No hay capturas almacenadas.` and
returns False for an empty result, otherwise calls `_mostrar_listado()` and
returns True. Call it before consult, update, and delete; return to the CRUD
submenu without asking for an ID when it returns False. Keep ID as the
operation key.

Enumerate `_mostrar_listado()` rows from 1 independently of `id_captura`.
Normalize confirmation with `unicodedata.normalize("NFD", value.casefold())`
and remove combining marks so all common capitalization and accent variants of
`si` become `si`; accept only that normalized token, while any other input
cancels.

- [ ] **Step 7: Reset the parent sequence only when empty**

Inside the same deletion transaction:

    if cursor.rowcount > 0:
        hay_capturas = conexion.execute(
            "SELECT 1 FROM capturas LIMIT 1"
        ).fetchone()
        if hay_capturas is None:
            conexion.execute(
                "DELETE FROM sqlite_sequence WHERE name = ?", ("capturas",)
            )

Do not update existing IDs or child rows.

- [ ] **Step 8: Run focused tests and verify GREEN**

Run:

    python -m unittest tests.unit.test_crud_controller tests.unit.test_menu_view tests.unit.test_repositorio

Expected: all selected tests pass.

- [ ] **Step 9: Commit**

    git add controller/crud_controller.py model/repositorio.py view/menu_view.py tests/unit/test_crud_controller.py tests/unit/test_menu_view.py tests/unit/test_repositorio.py
    git commit -m "fix: validate and clarify capture history"

## Task 4: Update Code and User Documentation

**Files:**
- Modify: README.md
- Modify: docs/manual_ejecucion.md
- Modify: docs/evidencias/README.md
- Modify: model/usuarios_model.py
- Modify: model/repositorio.py
- Modify: controller/crud_controller.py
- Modify: view/menu_view.py

**Interfaces:**
- Consumes: final behavior from Tasks 1 through 3.
- Produces: accurate public docstrings and reviewer instructions.

- [ ] **Step 1: Update public docstrings**

Document the accepted who formats and ISO output, the strict date validation,
the disk GB-to-byte reconstruction boundary, the numbered list versus stable
ID, and sequence reset only for an empty history.

- [ ] **Step 2: Update README and execution manual**

Document:

- exact YYYY-MM-DD filtering and controlled invalid-date errors;
- N. as display order and ID as the CRUD key;
- stable IDs while rows remain;
- reset to ID 1 only after the history becomes empty;
- case-insensitive explicit SI confirmation;
- live session duration and persisted disk detail behavior.

- [ ] **Step 3: Update evidence documentation**

Add the source PDF date, Ubuntu manual-validation scope, the three derived
image filenames, and a statement that annotated failure screenshots are not
presented as positive evidence.

- [ ] **Step 4: Verify documentation consistency**

Run:

    rg -n "YYYY-MM-DD|N\. \| ID|AUTOINCREMENT|confirm|duracion|disco" README.md docs/manual_ejecucion.md docs/evidencias/README.md
    rg -n "TODO|TBD|placeholder" README.md docs/manual_ejecucion.md docs/evidencias/README.md
    git diff --check

Expected: required behaviors are documented, no editorial placeholders, and
no whitespace errors.

- [ ] **Step 5: Commit**

    git add README.md docs/manual_ejecucion.md docs/evidencias/README.md model/usuarios_model.py model/repositorio.py controller/crud_controller.py view/menu_view.py
    git commit -m "docs: explain corrected validation behavior"

## Task 5: Extract and Verify Ubuntu Evidence Images

**Files:**
- Create: docs/articulo/figuras/evidencia_estado_general_ubuntu.png
- Create: docs/articulo/figuras/evidencia_crud_ubuntu.png
- Create: docs/articulo/figuras/evidencia_concurrencia_ubuntu.png

**Interfaces:**
- Consumes: C:/Users/jcbla/Downloads/Estado general.pdf
- Produces: three PNG figures cropped from 300 DPI renders without changing terminal content.

- [ ] **Step 1: Render the eight PDF pages at 300 DPI**

Use bundled Poppler and write intermediates under the system temporary
directory:

    pdftoppm -png -r 300 "C:/Users/jcbla/Downloads/Estado general.pdf" "%TEMP%/estado-general-300/pagina"

Expected: eight nonempty PNG files.

- [ ] **Step 2: Crop positive evidence only**

Use the bundled Python/Pillow runtime and these 300-DPI crop boxes, derived
from the inspected 144-DPI renders:

    general = crop(page1, (292, 396, 2188, 2229))
    registro = crop(page4, (446, 1438, 1188, 1913))
    eliminacion = crop(page5, (594, 1094, 1469, 1563))
    actualizacion = crop(page7, (594, 1813, 2188, 2521))
    listado = crop(page7, (446, 2667, 1385, 3400))
    concurrencia = crop(page8, (296, 396, 1708, 1458))

Save `general` and `concurrencia` directly using `optimize=True`. Build the
CRUD figure on a white canvas with two rows: `registro` beside `eliminacion`,
then `actualizacion` beside `listado`. Preserve each crop's aspect ratio,
normalize only row heights with LANCZOS resampling, use 30 px outer padding,
24 px gaps, and 42 px label bands containing `Registro`, `Eliminacion`,
`Actualizacion`, and `Listado final`. Use Pillow's bundled default font and
black text. Do not retouch terminal pixels, omit output lines, or cover any
part of a crop.

- [ ] **Step 3: Inspect all three PNG files**

Open each image at original detail and verify:

- text is readable at expected IEEE width;
- no Word headings or failure annotations are included;
- no terminal border or final output line is clipped;
- the concurrency crop shows 6 completed threads, 0 errors, different parent
  and child PIDs, and exit status 0.

- [ ] **Step 4: Commit**

    git add docs/articulo/figuras/evidencia_estado_general_ubuntu.png docs/articulo/figuras/evidencia_crud_ubuntu.png docs/articulo/figuras/evidencia_concurrencia_ubuntu.png
    git commit -m "docs: add Ubuntu execution evidence"

## Task 6: Refresh and Validate Both IEEE Articles

**Files:**
- Modify: docs/articulo/monitor_recursos_linux_es.tex
- Modify: docs/articulo/linux_resource_monitor_en.tex
- Modify: docs/articulo/README.md
- Modify: docs/articulo/monitor_recursos_linux_es.pdf
- Modify: docs/articulo/linux_resource_monitor_en.pdf

**Interfaces:**
- Consumes: corrected behavior, final Windows/WSL test counts, and three figures from Task 5.
- Produces: equivalent four-to-six-page Spanish and English IEEE sources and PDFs.

- [ ] **Step 1: Run the complete suites and capture exact evidence**

Run:

    python -m unittest discover -s tests
    wsl.exe -d Ubuntu -- bash -lc "cd '/mnt/c/Users/jcbla/Desktop/ESPE/Sexto Semestre/Sistemas Operativos/3P/linux-resource-monitor' && python3 -m unittest discover -s tests"

Record exact counts, skips, failures, and runtimes. Only the WSL passing count
is used as the Linux result in the articles.

- [ ] **Step 2: Update both article narratives in parallel**

Describe the five observed incidents and their corrections as validation
results, not as new features. Use the exact WSL test count in both abstracts,
result tables, and validation prose. Explain stable IDs plus display numbering
and empty-history reset without claiming general renumbering.

Keep citation keys and technical claims identical between languages.

- [ ] **Step 3: Add equivalent figures**

Retain the architecture figure. Replace the old concurrency image with
evidencia_concurrencia_ubuntu.png and add the general-state and CRUD evidence
with translated captions. Use figure or figure* based on legibility and page
flow; do not add a new LaTeX package unless the existing toolchain requires it.

- [ ] **Step 4: Compile both PDFs**

From docs/articulo run:

    tectonic -X compile --keep-logs monitor_recursos_linux_es.tex
    tectonic -X compile --keep-logs linux_resource_monitor_en.tex

Expected: both commands exit 0, BibTeX resolves, and both PDFs contain four,
five, or six Letter pages.

- [ ] **Step 5: Render and inspect every final page**

Render at 144 DPI with pdftoppm. Inspect every page for clipping, overlapping,
unreadable evidence, mixed-language captions, table overflow, blank columns,
and unresolved references. Correct and repeat until all pages pass.

Scan logs for Overfull, undefined citations, and undefined references. Update
docs/articulo/README.md with compiler version, page counts, figure provenance,
and final test counts.

- [ ] **Step 6: Verify bilingual parity**

Compare section counts, figure paths, citation keys, result numbers, and the
five corrected behaviors. Run Pandoc extraction and placeholder scans on both
sources.

- [ ] **Step 7: Commit**

    git add docs/articulo
    git commit -m "docs: refresh IEEE articles with Ubuntu validation"

## Task 7: Final Integrated Verification

**Files:**
- Verify only; modify files only to correct discovered regressions.

**Interfaces:**
- Consumes: all prior task outputs.
- Produces: merge-ready branch with fresh functional and visual evidence.

- [ ] **Step 1: Run final Windows and WSL suites**

    python -m unittest discover -s tests
    wsl.exe -d Ubuntu -- bash -lc "cd '/mnt/c/Users/jcbla/Desktop/ESPE/Sexto Semestre/Sistemas Operativos/3P/linux-resource-monitor' && python3 -m unittest discover -s tests"

Expected: zero failures in both environments; Windows may skip only explicit
Linux integration cases.

- [ ] **Step 2: Run repository hygiene checks**

    git diff --check main...HEAD -- . ":(exclude)docs/articulo/IEEEtran.cls"
    git status --short
    git ls-files "*.db" "*.sqlite" "*.sqlite3" "*.aux" "*.blg" "*.log"

Expected: no tracked runtime databases or LaTeX auxiliaries. The uploaded
IEEE-conference-template-062824 directory may remain untracked and untouched.

- [ ] **Step 3: Verify deliverables exist**

Confirm both tex files, both four-to-six-page PDFs, three new PNG evidence
files, manuals, evidence README, and article README.

- [ ] **Step 4: Request whole-branch review**

Generate a review package from the merge base with main through HEAD. Resolve
every Critical or Important finding, rerun covering tests, and re-review before
finishing the branch.
