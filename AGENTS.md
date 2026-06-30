# AGENTS.md — Linux Resource Monitor

## 1. Purpose

This file defines the implementation rules that coding agents must follow when working in the `linux-resource-monitor` repository.

The project is an academic Operating Systems assignment: a Linux terminal application written in Python 3 that monitors system resources, demonstrates processes and threads, and stores monitoring captures through CRUD operations in SQLite.

## 2. Requirements priority

Use the following order of authority:

1. The professor's original project specification stored in `docs/`.
2. `docs/Semana1_Analisis_Arquitectura_BD.md`.
3. This `AGENTS.md`.
4. The current codebase.

If a lower-priority source conflicts with a higher-priority source, follow the higher-priority source and report the conflict before making a broad change.

Do not remove or weaken any mandatory requirement to simplify implementation.

## 3. Mandatory scope

The final application must include:

- Linux execution.
- Python 3.
- An interactive terminal interface.
- CPU monitoring.
- Memory and swap monitoring.
- Process monitoring.
- Connected-user monitoring.
- Mounted-filesystem monitoring.
- Network-interface monitoring.
- Direct reading from `/proc`.
- Native Linux commands executed with `subprocess`.
- At least one child process created explicitly with `os.fork()`.
- At least two concurrent threads created explicitly with `threading.Thread`.
- Complete CRUD operations.
- SQLite persistence.
- Installation and execution documentation.

The application only monitors and records information. It must not kill processes, change network configuration, free memory, modify filesystems, or require administrator privileges for ordinary use.

## 4. Current project stages

Respect the incremental schedule. Do not implement unrelated later-week features unless the user explicitly requests them.

- **Week 1:** requirements, architecture and database design.
- **Week 2:** CPU, memory and direct `/proc` reading.
- **Week 3:** disk, network, users and processes.
- **Week 4:** `os.fork()`, threads and CRUD.
- **Week 5:** integration, testing, corrections, article, presentation and video.

Before changing code, identify which week and requirement the task belongs to.

## 5. Repository and naming rules

The repository root is named:

```text
linux-resource-monitor
```

Use the existing Spanish module names defined by the architecture document:

- `model/cpu_model.py`
- `model/memoria_model.py`
- `model/procesos_model.py`
- `model/usuarios_model.py`
- `model/disco_model.py`
- `model/red_model.py`
- `model/repositorio.py`
- `view/consola_view.py`
- `view/menu_view.py`
- `controller/monitor_controller.py`
- `controller/concurrencia_controller.py`
- `controller/crud_controller.py`
- `database/conexion.py`
- `database/esquema.sql`

Do not rename these files or introduce a different architecture without an explicit request.

## 6. Architecture rules

Follow the documented MVC separation.

### Model

The Model may:

- Read files under `/proc`.
- Execute approved Linux commands through `subprocess`.
- Parse raw operating-system data.
- Return structured Python data.
- Access SQLite only through the repository component.

The Model must not:

- Print terminal screens.
- Ask the user for input.
- Contain menu navigation.
- Depend on the View.

### View

The View may:

- Show menus, tables, headings and messages.
- Format units, dates and percentages.
- Read keyboard input.
- Paginate or limit long lists.

The View must not:

- Read `/proc`.
- Execute Linux commands.
- Parse operating-system output.
- Run SQL.
- Access SQLite directly.
- Apply business rules.

### Controller

The Controller may:

- Coordinate Models and Views.
- Validate operation flow.
- Consolidate monitoring results.
- Coordinate threads and the child process.
- Call CRUD methods from the repository.

The Controller must not:

- Contain raw SQL.
- Parse command output.
- Duplicate Model logic.

## 7. General Python rules

- Use Python 3 and the standard library whenever possible.
- Do not add dependencies without explaining why they are necessary.
- Add type hints to public functions.
- Add concise docstrings to modules and non-obvious functions.
- Keep functions focused and small.
- Prefer pure parsing functions that accept text and return structured data.
- Use `pathlib.Path` for project paths when practical.
- Use context managers for files, pipes and SQLite connections.
- Do not use broad `except Exception` blocks unless the exception is logged and converted into a controlled application error.
- Do not expose normal users to stack traces.
- Keep user-facing text in Spanish unless the project team requests another language.
- Preserve existing functionality and avoid rewriting correct files unnecessarily.

## 8. Structured data contracts

Models must return dictionaries or dataclasses, never preformatted terminal blocks.

Use stable, descriptive keys that match the architecture and database design. Examples include:

```python
{
    "procesadores_logicos": 8,
    "frecuencia_mhz": 2400.0,
    "carga_promedio_1m": 0.42,
    "carga_promedio_5m": 0.37,
    "carga_promedio_15m": 0.31,
    "porcentaje_uso": 28.75,
}
```

```python
{
    "mem_total_mb": 15938.25,
    "mem_usada_mb": 6420.10,
    "mem_libre_mb": 1120.00,
    "mem_disponible_mb": 9518.15,
    "swap_total_mb": 2048.00,
    "swap_usada_mb": 120.50,
}
```

Do not change field names in only one layer. Any contract change must update the relevant Model, Controller, View, database schema, tests and documentation together.

## 9. CPU rules

Use:

- `/proc/cpuinfo` for processor information and logical-processor data.
- `/proc/stat` for CPU-utilization percentage.
- `/proc/loadavg` for load averages only.

Never calculate CPU-utilization percentage from `/proc/loadavg`.

Calculate utilization from two `/proc/stat` samples separated by a short interval:

1. Read aggregate CPU counters.
2. Wait for a short configurable interval.
3. Read them again.
4. Calculate deltas for total and idle time.
5. Calculate the active percentage.

Do not label logical processors as physical cores. If physical-core detection is implemented, calculate it separately from unique `(physical id, core id)` pairs when available and provide a documented fallback for virtualized systems where those fields are absent.

## 10. Memory rules

Read memory values from `/proc/meminfo`.

Use these definitions consistently:

- Total memory: `MemTotal`.
- Free memory: `MemFree`.
- Available memory: `MemAvailable`.
- Used memory: `MemTotal - MemAvailable`.
- Total swap: `SwapTotal`.
- Used swap: `SwapTotal - SwapFree`.

Do not use “free” and “available” as synonyms.

The `free` command may be used for validation, but the required implementation must still read `/proc/meminfo`.

## 11. Process rules

Collect at least:

- PID.
- Process name.
- Process state.
- Owner username.

The process list may change while being read. A process disappearing during collection is an expected race condition and must be skipped or reported without terminating the application.

Do not require the collected process count to exactly equal a later `ps -ef` count; compare representative records and required fields because the process table changes continuously.

## 12. User-session rules

Use the `who` command through `subprocess`.

Collect:

- Username.
- Terminal.
- Login start time.

Calculate the displayed connection duration from the current time and the login start time. Keep the stored value named `inicio_sesion`; do not store a formatted duration as if it were a timestamp.

## 13. Disk rules

Use `df` through `subprocess`.

Prefer parseable output such as:

```text
df -P -B1
```

Parse byte values first and convert them for display. Do not parse localized human-readable units from `df -h` as the primary data source.

Collect one record per mounted filesystem:

- Filesystem.
- Mount point.
- Total bytes.
- Used bytes.
- Available bytes.
- Usage percentage.

The View may display GB with a maximum of two decimals.

## 14. Network rules

Use:

- `/proc/net/dev` for traffic counters.
- `ip` through `subprocess` for addresses and interface information.

Collect:

- Interface name.
- IP address.
- Bytes received.
- Bytes transmitted.
- Packets received.
- Packets transmitted.

The current schema stores one `direccion_ip` per interface record. For the initial version, use the primary IPv4 address when available; otherwise use the first available IPv6 address or `None`. Do not silently concatenate several addresses into an undocumented string.

If full multi-address persistence is later required, update the architecture and schema before changing the implementation.

## 15. Subprocess rules

Use `subprocess.run()` with an argument list.

Required practices:

- Do not use `shell=True`.
- Capture standard output and standard error.
- Use text mode.
- Set a reasonable timeout.
- Check the return code.
- Convert failures into controlled Model errors.
- Prefer `LC_ALL=C` for commands whose output is parsed, so parsing does not depend on system language.

Example pattern:

```python
subprocess.run(
    ["df", "-P", "-B1"],
    capture_output=True,
    text=True,
    timeout=5,
    check=False,
    env={**os.environ, "LC_ALL": "C"},
)
```

## 16. SQLite rules

SQLite is the only persistence engine required for the initial version.

Every connection must enable:

```sql
PRAGMA foreign_keys = ON;
```

Additional rules:

- Use parameterized SQL queries.
- Use one transaction to save a capture and all of its related metrics.
- Roll back the entire operation if any required insert fails.
- Use `ON DELETE CASCADE` for child metrics.
- Do not share a connection across processes.
- Do not share one connection among worker threads.
- Prefer performing database writes in the main flow after monitoring results have been consolidated.
- Store generated database files under `database/data/`.
- Do not commit runtime `.db`, `.sqlite` or `.sqlite3` files unless a specific demonstration database is explicitly approved.

## 17. Concurrency rules

The project must visibly demonstrate both mechanisms required by the professor.

### Threads

- Instantiate at least two `threading.Thread` objects explicitly.
- Use them for independent monitoring tasks.
- Start the threads before joining them.
- Collect exceptions from worker threads and report partial failures clearly.
- Protect shared result structures with a lock or use one isolated result slot per thread.
- Do not write to SQLite from monitoring worker threads.

### Child process

- Create at least one child with `os.fork()`.
- Keep the demonstration isolated and meaningful.
- Record parent and child PIDs in logs or output.
- Reap the child with `os.waitpid()` to prevent zombie processes.
- Do not call `os.fork()` while worker threads are active.
- Do not reuse an inherited SQLite connection in the child.
- If data must return to the parent, use an OS pipe or another explicit, documented IPC mechanism.

Do not replace the mandatory `threading.Thread` or `os.fork()` demonstrations with higher-level abstractions that hide the required mechanisms.

## 18. Terminal usability and accessibility

The interface must:

- Be fully operable with the keyboard.
- Use numbered menus.
- Provide options to return, go to the main menu and exit.
- Validate invalid input without terminating.
- Request explicit confirmation before deletion.
- Show progress, success, warning and error messages.
- Show units and timestamps.
- Use at most two decimals for displayed metrics.
- Paginate or limit long process and capture lists.
- Remain understandable without colors.
- Use text labels such as `NORMAL`, `ADVERTENCIA` and `CRÍTICO` when visual indicators are present.
- Avoid requiring Unicode box-drawing support.

Colors and progress bars may supplement information but must never be the only way to communicate it.

## 19. Error handling

Handle at least:

- Missing `/proc` files.
- Permission errors.
- Command not found.
- Command timeout.
- Nonzero command exit status.
- Unexpected or incomplete command output.
- Processes disappearing while being read.
- No connected users.
- No IP address on an interface.
- SQLite errors.
- Invalid menu input.
- Keyboard interruption.

A failure in one monitoring module should not automatically discard all other successfully collected live results. A database capture, however, must be atomic: either all required records are committed or none are.

## 20. Testing rules

Use tests that do not depend only on the current computer.

- Keep unit tests under `tests/unit/`.
- Keep Linux integration tests under `tests/integration/`.
- Store sample `/proc` and command outputs under `tests/fixtures/`.
- Test parsers with fixture text.
- Test SQLite CRUD with a temporary database.
- Test cascade deletion.
- Skip Linux-only integration tests explicitly when the environment is not Linux.
- Avoid requiring root privileges.
- Use the standard-library `unittest` framework unless the team intentionally adopts another test dependency.

Relevant tests must be run after each implementation change.

## 21. Documentation synchronization

When a technical decision changes, update all affected documentation.

At minimum, keep these files synchronized:

- `README.md`
- `docs/Semana1_Analisis_Arquitectura_BD.md`
- `database/esquema.sql`
- Installation and execution manuals
- Tests that define expected behavior

Do not let generated code silently contradict the Week 1 design.

## 22. Agent workflow

Before editing:

1. Read the professor's specification.
2. Read `docs/Semana1_Analisis_Arquitectura_BD.md`.
3. Inspect the existing code and tests.
4. Identify the affected requirement and project week.
5. State a brief implementation plan.
6. Make the smallest coherent change.
7. Run relevant tests or explain why they could not run.
8. Summarize modified files, behavior and remaining risks.

Do not:

- Generate the entire project when only one module was requested.
- Implement a web or graphical application.
- Add unrelated features.
- overwrite documentation with a shorter generic version.
- invent completed tests or execution results.
- claim Linux behavior was verified when it was not executed on Linux.
