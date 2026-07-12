# Semana 5 Integration and Evidence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar todos los modulos en el menu principal, completar pruebas y correcciones, redactar manuales y producir evidencias reproducibles y visuales hasta antes del articulo IEEE.

**Architecture:** `main.py` compone repositorio, controladores y Vista. Los Controladores coordinan los Modelos y entregan datos estructurados; la Vista formatea y navega; solo `model/repositorio.py` accede a SQLite. Las evidencias ejecutan la aplicacion real en WSL y conservan tanto logs como capturas de la terminal dedicada.

**Tech Stack:** Python 3 standard library, `unittest`, SQLite, `/proc`, comandos Linux, `threading.Thread`, `os.fork()`, PowerShell y Ubuntu WSL.

## Global Constraints

- Mantener la arquitectura MVC y los nombres de archivo documentados.
- No agregar dependencias externas, GUI, web ni motores de persistencia nuevos.
- No leer `/proc`, ejecutar comandos o abrir SQLite desde la Vista.
- No compartir conexiones SQLite entre hilos o procesos.
- No ejecutar `os.fork()` mientras existan hilos activos.
- Conservar RF-01 a RF-12 y RNF-01 a RNF-16.
- No redactar todavia el articulo IEEE, la presentacion ni el video.
- No incluir `docs/~$oyecto Integrador de SO.docx` en ningun commit.

---

### Task 1: Presentacion de todos los modulos

**Files:**
- Modify: `view/consola_view.py`
- Modify: `tests/unit/test_consola_view.py`

**Interfaces:**
- Consumes: diccionarios y listas devueltos por los seis Modelos.
- Produces: `format_disco_info(data) -> str`
- Produces: `format_red_info(data) -> str`
- Produces: `format_procesos_info(data, limite=20) -> str`
- Produces: `format_usuarios_info(data, ahora=None) -> str`
- Produces: `format_estado_general(data, errores=None) -> str`

- [ ] **Step 1: Write failing formatter tests**

```python
def test_format_disco_info_converts_bytes_to_gb():
    text = consola_view.format_disco_info([{
        "sistema_archivos": "/dev/sda1", "punto_montaje": "/",
        "espacio_total_bytes": 1073741824, "espacio_usado_bytes": 536870912,
        "espacio_libre_bytes": 536870912, "porcentaje_uso": 50.0,
    }])
    assert "1.00 GB" in text
    assert "/dev/sda1" in text
```

Add equivalent tests for network packets, process limiting, empty users and
session duration calculated from an injected `ahora`.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.unit.test_consola_view`

Expected: errors because the new formatter functions do not exist.

- [ ] **Step 3: Implement focused formatters**

Use ASCII table separators, two-decimal numeric values, text status labels and
`datetime` parsing for stored ISO session timestamps. Return strings only; do
not print from formatter functions.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.unit.test_consola_view`

Expected: all console-view tests pass.

### Task 2: Controller facade for live monitoring

**Files:**
- Modify: `controller/monitor_controller.py`
- Create: `tests/unit/test_monitor_controller.py`

**Interfaces:**
- Consumes: public collection functions from all six Models.
- Produces: `MonitorController.obtener_modulo(nombre: str) -> object`
- Produces: `MonitorController.obtener_estado_general() -> dict[str, object]`
- Produces: `MonitorController.demostrar_concurrencia() -> dict[str, object]`

- [ ] **Step 1: Write failing controller tests**

```python
def test_obtener_modulo_delegates_to_registered_collector():
    controller = MonitorController(collectors={"cpu": lambda: {"uso": 10}})
    assert controller.obtener_modulo("cpu") == {"uso": 10}

def test_unknown_module_is_controlled():
    with self.assertRaises(ModuloNoDisponibleError):
        MonitorController(collectors={}).obtener_modulo("desconocido")
```

Also test partial errors from `obtener_estado_general()` and that
`demostrar_concurrencia()` calls fork only after threaded collection returns.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.unit.test_monitor_controller`

Expected: import or attribute failures for the missing facade.

- [ ] **Step 3: Implement the facade**

Keep collectors injectable for deterministic tests. Return structured values
and controlled errors; do not format terminal output in the Controller.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.unit.test_monitor_controller`

Expected: all monitor-controller tests pass.

### Task 3: Main menu integration

**Files:**
- Modify: `view/menu_view.py`
- Modify: `main.py`
- Create: `tests/unit/test_menu_principal.py`
- Modify: `tests/unit/test_main.py`

**Interfaces:**
- Consumes: `MonitorController`, `CrudController` and console formatters.
- Produces: `ejecutar_menu_principal(monitor, crud, input_fn=input, output_fn=print) -> None`
- Produces: `crear_aplicacion(ruta_bd=RUTA_BD_PREDETERMINADA) -> tuple[MonitorController, CrudController]`

- [ ] **Step 1: Write failing navigation tests**

```python
def test_menu_cpu_displays_formatted_data_and_returns():
    inputs = iter(["2", "", "0"])
    outputs = []
    ejecutar_menu_principal(monitor_fake, crud_fake, lambda _: next(inputs), outputs.append)
    assert any("=== CPU ===" in item for item in outputs)
```

Add cases for options 1 through 9, invalid input, returning to the main menu and
clean exit. Inject all collaborators; tests must not read the live OS.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.unit.test_menu_principal tests.unit.test_main`

Expected: failure because the main-menu function and application composition do
not exist.

- [ ] **Step 3: Implement menu and composition root**

Use the approved numbered menu. Route options 1-7 through `MonitorController`,
option 8 through `ejecutar_menu_crud`, option 9 through the concurrency
demonstration, and option 0 to exit. Convert expected exceptions into Spanish
messages and keep the menu active.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.unit.test_menu_principal tests.unit.test_main`

Expected: all navigation and composition tests pass.

### Task 4: CRUD presentation and error corrections

**Files:**
- Modify: `view/menu_view.py`
- Modify: `controller/crud_controller.py`
- Modify: `tests/unit/test_menu_view.py`
- Modify: `tests/unit/test_crud_controller.py`

**Interfaces:**
- Preserves: RF-09 create, RF-10 read/filter, RF-11 metadata update and RF-12 delete.
- Produces controlled user messages for collection and SQLite failures.

- [ ] **Step 1: Write failing regression tests**

Add tests proving an incomplete capture, repository error or invalid identifier
returns to the CRUD menu without a traceback. Add a detail-view test proving CPU
and memory values are formatted rather than displayed as raw dictionaries.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.unit.test_menu_view tests.unit.test_crud_controller`

Expected: failures for unhandled errors or raw detail output.

- [ ] **Step 3: Implement controlled boundaries**

Introduce one controller-level CRUD error if required and reuse console
formatters for historical detail. Keep SQL confined to the repository.

- [ ] **Step 4: Verify GREEN and regression suite**

Run: `python -m unittest discover -s tests`

Expected on Windows: all tests pass with only Linux-specific tests skipped.

### Task 5: End-to-end integration tests

**Files:**
- Create: `tests/integration/test_aplicacion_integration.py`
- Modify: `tests/integration/test_fork_integration.py` only if a correction is required.

**Interfaces:**
- Uses: temporary SQLite database and real Linux collectors when on Linux.
- Verifies: full capture, read, update, delete, cascade and concurrency evidence.

- [ ] **Step 1: Write the integration test**

The test must use `tempfile.TemporaryDirectory`, skip live Linux checks outside
Linux, save one complete capture, read it, update metadata, delete it and assert
zero remaining records.

- [ ] **Step 2: Verify RED or expose integration gaps**

Run in WSL: `python3 -m unittest tests.integration.test_aplicacion_integration`

Expected before corrections: at least one failure if the integrated flow is not
yet complete; otherwise document that the new test exercises a previously
untested cross-layer path.

- [ ] **Step 3: Apply only corrections demonstrated by failures**

Keep fixes scoped to the owning Model, Controller, View or repository.

- [ ] **Step 4: Verify all environments**

Run local: `python -m unittest discover -s tests`

Run WSL: `python3 -m unittest discover -s tests`

Expected: clean suite in WSL and only explicit Linux skips on Windows.

### Task 6: Installation and execution manuals

**Files:**
- Create: `docs/manual_instalacion.md`
- Create: `docs/manual_ejecucion.md`
- Modify: `README.md`

- [ ] **Step 1: Write installation manual**

Document Ubuntu/WSL prerequisites, clone, virtual environment, standard-library
requirements, checks for `ps`, `who`, `df` and `ip`, test command and expected
database location.

- [ ] **Step 2: Write execution manual**

Document every menu option, CRUD workflow, confirmation rules, evidence option,
database reset procedure and controlled troubleshooting without `sudo`.

- [ ] **Step 3: Synchronize README**

Link both manuals and describe the final integrated `python3 main.py` entrypoint.
Do not mark the IEEE, presentation or video complete.

- [ ] **Step 4: Audit commands**

Execute every command shown in both manuals in WSL or replace it with a verified
equivalent.

### Task 7: Reproducible evidence logs

**Files:**
- Create: `scripts/generar_evidencias.py`
- Create: `docs/evidencias/README.md`
- Create: `docs/evidencias/logs/.gitkeep`
- Test: `tests/unit/test_generar_evidencias.py`

**Interfaces:**
- Produces: one UTF-8 log per evidence case using commands executed in WSL.
- Does not write into source-code or database directories.

- [ ] **Step 1: Write failing evidence-runner tests**

Test command construction, deterministic filenames and failure reporting with
an injected subprocess runner.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.unit.test_generar_evidencias`

Expected: import failure because the script module does not exist.

- [ ] **Step 3: Implement evidence runner**

Generate logs for test suite, live resources, CRUD transaction, threads and
fork. Preserve command, timestamp, return code, stdout and stderr. Never replace
a failed log with fabricated success output.

- [ ] **Step 4: Generate real logs in WSL**

Run the evidence runner and inspect every file. The evidence index must map logs
to RF-01 through RF-12 and relevant RNF entries.

### Task 8: Architecture and terminal screenshots

**Files:**
- Create: `docs/evidencias/arquitectura_actual.mmd`
- Create: `docs/evidencias/arquitectura_actual.png`
- Create: `scripts/generar_diagrama_arquitectura.ps1`
- Create: `scripts/capturar_ventana_terminal.ps1`
- Create: `docs/evidencias/capturas/.gitkeep`

- [ ] **Step 1: Create layered architecture source**

Use separate left-to-right lanes for live monitoring, CRUD persistence and fork
evidence. Route arrows through Controller nodes so no View-to-Model or
Model-to-Database shortcut appears.

- [ ] **Step 2: Render and inspect PNG**

Render a high-resolution PNG, inspect it at full size and revise until labels
are legible and arrows do not overlap nodes or each other incoherently.

- [ ] **Step 3: Implement safe terminal-window capture**

The PowerShell script must identify a dedicated Windows Terminal window by its
title and capture only its rectangle. If it cannot identify exactly one target,
it must stop with an error and instruct the user to use `Win+Shift+S`; it must
never fall back to full-screen capture.

- [ ] **Step 4: Capture evidence cases**

Open the dedicated WSL evidence session, run each indexed command and save PNGs
under `docs/evidencias/capturas/`. Inspect each image for readable output and
private information before retaining it.

### Task 9: Final synchronization and evidence audit

**Files:**
- Modify: `README.md`
- Modify: `docs/ESTRUCTURA_PROYECTO.md`
- Modify: `docs/evidencias/README.md`

- [ ] **Step 1: Cross-check requirements**

Map RF-01 through RF-12 and RNF-01 through RNF-16 to implementation, tests and
evidence. Record any unresolved item instead of marking it complete.

- [ ] **Step 2: Run final verification**

Run `git diff --check`, local tests, WSL tests, manual smoke flow and evidence
generation. Confirm no runtime database, cache, temporary Word file or private
desktop capture is staged.

- [ ] **Step 3: Update project status**

Mark integration, tests, corrections, manuals and evidence complete only after
the verification output confirms them. Keep article, presentation and video
pending.
