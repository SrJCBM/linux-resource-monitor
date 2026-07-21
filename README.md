# Linux Resource Monitor

A Python-based Linux resource monitor using `/proc`, native system commands, threads, processes and SQLite.

## Overview

**Linux Resource Monitor** is an academic Operating Systems project that collects and presents information about the current state of a Linux system. It provides an interactive terminal interface and stores monitoring captures so they can be created, consulted, updated and deleted.

The application is designed for monitoring and registration only. It does not terminate processes, modify network settings, free memory or alter mounted filesystems.

## Project status

| Stage | Scope | Status |
|---|---|---|
| Week 1 | Requirements, architecture and database design | Completed |
| Week 2 | CPU, memory and `/proc` implementation | Completed |
| Week 3 | Disk, network, users and processes | Completed |
| Week 4 | `os.fork()`, threads and CRUD | Completed |
| Week 5 | Integration, tests, manuals and evidence | In progress |

> Week 5 integration, test coverage, manuals and execution evidence are in progress. The bilingual IEEE article drafts are complete and validated at four pages each; the presentation and demonstration video remain pending deliverables.

## Quick start for reviewers

These steps are intended for someone cloning the repository for the first time on Ubuntu, WSL or another Linux distribution.

```bash
git clone <repository-url>
cd linux-resource-monitor
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
```

The tested implementation covers all six monitoring modules, concurrent collection, the Linux `fork()` demonstration, SQLite CRUD and the integrated terminal menu. The bilingual IEEE article drafts are complete and validated at four pages each. The presentation and demonstration video remain pending Week 5 deliverables.

## Week 2 and Week 3 validation guide

Use this section when another team member clones the repository in Ubuntu, WSL or a Linux virtual machine.

### 1. Run all automated tests

```bash
python3 -m unittest discover -s tests
```

Expected result: all unit tests should pass. These tests use fixtures stored in `tests/fixtures/`, so they are deterministic and do not depend on the current machine state.

### 2. Test Week 2: CPU and memory

Run live CPU and memory readings:

```bash
python3 -c "from model.cpu_model import obtener_info_cpu; print(obtener_info_cpu())"
python3 -c "from model.memoria_model import obtener_info_memoria; print(obtener_info_memoria())"
```

Expected CPU keys:

- `procesadores_logicos`
- `modelo`
- `frecuencia_mhz`
- `carga_promedio_1m`
- `carga_promedio_5m`
- `carga_promedio_15m`
- `porcentaje_uso`

Expected memory keys:

- `mem_total_mb`
- `mem_usada_mb`
- `mem_libre_mb`
- `mem_disponible_mb`
- `swap_total_mb`
- `swap_usada_mb`

Useful Linux comparison commands:

```bash
lscpu
cat /proc/loadavg
cat /proc/stat | head -n 1
cat /proc/meminfo | head
free -m
```

Validation notes:

- `porcentaje_uso` must be between `0.0` and `100.0`.
- `procesadores_logicos` should match the logical CPU count reported by `lscpu`.
- `mem_usada_mb` should follow `MemTotal - MemAvailable`, not `MemTotal - MemFree`.
- `mem_libre_mb` and `mem_disponible_mb` are different values and should not be treated as synonyms.

### 3. Test Week 3: disk, network, users and processes

Run live readings for the Week 3 modules:

```bash
python3 -c "from model.disco_model import obtener_info_disco; print(obtener_info_disco())"
python3 -c "from model.red_model import obtener_info_red; print(obtener_info_red())"
python3 -c "from model.usuarios_model import obtener_usuarios; print(obtener_usuarios())"
python3 -c "from model.procesos_model import obtener_procesos; print(obtener_procesos()[:5])"
```

Expected disk keys:

- `sistema_archivos`
- `punto_montaje`
- `espacio_total_bytes`
- `espacio_usado_bytes`
- `espacio_libre_bytes`
- `porcentaje_uso`

Expected network keys:

- `interfaz`
- `direccion_ip`
- `bytes_recibidos`
- `bytes_enviados`
- `paquetes_recibidos`
- `paquetes_enviados`

Expected user-session keys:

- `nombre_usuario`
- `terminal`
- `inicio_sesion`

Expected process keys:

- `pid`
- `usuario_propietario`
- `estado`
- `nombre_proceso`

Useful Linux comparison commands:

```bash
df -P -B1
cat /proc/net/dev
ip addr show
who
ps -eo pid=,user=,stat=,comm= | head
```

Validation notes:

- Disk records should be one row per mounted filesystem.
- Network traffic counters should match `/proc/net/dev`; IP addresses should come from `ip addr show`.
- The users command may return an empty list if no interactive sessions are registered by `who`.
- The process list changes constantly; compare representative records, not the exact total process count.
- None of these checks should require `sudo`.

## Week 4 validation guide

Run these checks in Ubuntu, WSL or another Linux distribution.

### 1. Validate threads

```bash
python3 -c "from controller.concurrencia_controller import recolectar_con_hilos; r=recolectar_con_hilos(); print(r['errores']); print(*r['evidencias'], sep='\n')"
```

Expected result: `errores` is empty and six evidence records show thread names beginning with `monitor-`, along with start and finish timestamps.

### 2. Validate `os.fork()`

```bash
python3 -c "from controller.concurrencia_controller import demostrar_fork; print(demostrar_fork())"
```

Expected result: `parent_pid` and `child_pid` are different, `child_parent_pid` matches `parent_pid`, and `exit_status` is `0`.

### 3. Test SQLite CRUD from the console

```bash
python3 main.py
```

Use the numbered menu to:

1. Register a complete monitoring capture.
2. List captures and optionally filter by an exact, real `YYYY-MM-DD` date.
3. Consult a capture by identifier.
4. Update only its label and comment.
5. Delete it by typing the explicit word `SI` when confirmation is requested.

The date filter rejects values such as `2026/07/18`, `18-07-2026` and
`2026-02-30` with a controlled message, then keeps the menu active. In capture
lists, `N.` is the consecutive display order and `ID` is the stable SQLite key
used for consult, update and delete operations. Captures are ordered
chronologically from oldest to newest:

```text
N. | ID | FECHA Y HORA | ETIQUETA
1  | 9  | 2026-07-18 10:00:00 | antes
2  | 4  | 2026-07-18 11:00:00 | despues
```

Deleting a row never renumbers the IDs that remain. When the capture history is
completely empty, the repository clears any residual `AUTOINCREMENT` sequence
before insertion so the next capture uses ID 1. Deletion confirmation is
case-insensitive and also
accepts the accented form of the same explicit word (`SI`, `si`, `Si` or
`sí`); any other response cancels the operation.

Live `who` timestamps are normalized to `YYYY-MM-DD HH:MM` before the View
calculates connection duration from the current time. Historical disk details
use the same byte-based contract as live disk data: the repository reconstructs
`espacio_total_bytes`, `espacio_usado_bytes` and `espacio_libre_bytes` from the
persisted GB values before the View formats them.

The default database is created at `database/data/monitor.sqlite3`. It is a runtime file and must not be committed.

### 4. Run all Week 2-4 tests

```bash
python3 -m unittest discover -s tests
```

On Windows PowerShell with Ubuntu WSL, the equivalent command is:

```powershell
wsl.exe -d Ubuntu --cd "<repository-path-in-wsl>" -- python3 -m unittest discover -s tests
```

## Main requirements

The final application must display:

- CPU information, load average and utilization.
- Total, used, free and available memory.
- Swap usage.
- Active processes with PID, name, state and owner.
- Connected users and connection duration.
- Mounted filesystems and storage usage.
- Network interfaces, addresses and traffic counters.
- Stored monitoring captures with full CRUD operations.

It must also demonstrate:

- Direct access to the Linux `/proc` virtual filesystem.
- Linux commands executed through `subprocess`.
- At least one child process created with `os.fork()`.
- At least two concurrent threads created with `threading.Thread`.
- SQLite persistence.

## Technologies

- Linux
- Python 3
- Visual Studio Code
- SQLite
- Git and GitHub

The implementation prioritizes the Python standard library.

## Data sources

| Module | Main source |
|---|---|
| CPU | `/proc/cpuinfo`, `/proc/stat`, `/proc/loadavg` |
| Memory | `/proc/meminfo` |
| Processes | `ps` and/or `/proc/[pid]/` |
| Users | `who` |
| Disk | `df` |
| Network | `/proc/net/dev`, `ip` |

The `free` and `lscpu` commands may be used to validate selected values, while the mandatory `/proc` readings remain part of the implementation.

## Architecture

The application follows an MVC-oriented organization:

- **Model:** obtains and parses operating-system information and provides SQLite repository operations.
- **View:** displays terminal menus, tables and messages and receives keyboard input.
- **Controller:** coordinates data collection, concurrency, validation, CRUD flow and presentation.

The first version is an interactive terminal application. A graphical or web interface is outside the mandatory scope.

## Repository structure

```text
linux-resource-monitor/
├── AGENTS.md
├── README.md
├── .gitignore
├── requirements.txt
├── main.py
├── model/
├── view/
├── controller/
├── database/
├── docs/
└── tests/
```

See `docs/ESTRUCTURA_PROYECTO.md` for the complete proposed tree and the responsibility of each folder.

## Installation

### Requirements

- A Linux distribution such as Ubuntu Desktop, Ubuntu Server or an equivalent distribution.
- Python 3.
- Git.
- Native commands `ps`, `who`, `df`, `free` and `ip`.

### Clone the repository

```bash
git clone <repository-url>
cd linux-resource-monitor
```

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

The initial version is expected to rely mainly on the Python standard library. `requirements.txt` may therefore remain empty until a justified dependency is added.

## Execution

```bash
python3 main.py
```

The entry point opens the integrated terminal menu for live monitoring, capture history and the concurrency demonstration. The application is Linux-specific because live capture uses `/proc`, Linux commands and `os.fork()`.

Installation and usage details are available in the Spanish manuals:

- [Installation manual](docs/manual_instalacion.md)
- [Execution manual](docs/manual_ejecucion.md)
- [Evidence index](docs/evidencias/README.md)

## Tests

Run the test suite with:

```bash
python3 -m unittest discover -s tests
```

Unit tests should use stored sample outputs. Linux integration tests should be kept separate because live system information changes continuously.

Recommended checks before moving to Week 5:

- Run all unit tests with `python3 -m unittest discover -s tests`.
- Complete the Week 2, Week 3 and Week 4 validation guides above in Ubuntu, WSL or a Linux virtual machine.
- Confirm the project does not require administrator privileges.

## Database

SQLite is the persistence engine selected for the first version.

The database stores:

- Capture metadata.
- CPU metrics, including the processor model reported by `/proc/cpuinfo`.
- Memory metrics.
- Disk metrics per mounted filesystem.
- Process metrics.
- Network metrics.
- Connected-user metrics.

Foreign keys and cascade deletion must be enabled. Runtime database files should be stored in `database/data/` and excluded from Git unless a demonstration database is intentionally approved.

## Terminal usability

The interface is expected to:

- Work entirely with the keyboard.
- Use numbered and consistent menus.
- Validate incorrect input.
- Request confirmation before deletion.
- Display units, timestamps and clear messages.
- Paginate or limit long lists.
- Remain understandable without colors or special terminal characters.

## Development workflow

Recommended branches:

```text
main
develop
feature/cpu-monitor
feature/memory-monitor
feature/disk-monitor
feature/network-monitor
feature/process-monitor
feature/user-monitor
feature/concurrency
feature/crud
```

Recommended commit prefixes:

```text
docs:
feat:
fix:
test:
refactor:
chore:
```

Examples:

```text
docs: add week 1 architecture
feat: implement proc meminfo parser
test: add memory parser fixtures
fix: handle disappearing processes
```

Use pull requests to integrate completed work into `develop`, then merge stable milestones into `main`.

## Documentation

Project documentation is stored under `docs/`:

- Original professor specification.
- Week 1 requirements, architecture and database design.
- Installation manual.
- Execution manual.
- Complete bilingual IEEE article drafts, validated at four pages each:
  - [Spanish LaTeX source](docs/articulo/monitor_recursos_linux_es.tex) and [final Spanish PDF](docs/articulo/monitor_recursos_linux_es.pdf).
  - [English LaTeX source](docs/articulo/linux_resource_monitor_en.tex) and [final English PDF](docs/articulo/linux_resource_monitor_en.pdf).
- Presentation material.
- Demonstration evidence.

The Ubuntu manual-validation source is the eight-page `Estado general.pdf`,
created on 2026-07-18. Three verified article figures were extracted without
altering terminal output: `evidencia_estado_general_ubuntu.png`,
`evidencia_crud_ubuntu.png` and `evidencia_concurrencia_ubuntu.png`. The general
state and concurrency figures are positive execution evidence. The CRUD figure
records the pre-correction validation sequence and is labeled as diagnostic
evidence in the articles; its old header and ID behavior do not represent the
corrected interface. Explanatory failure annotations from the PDF are omitted.

## Academic deliverables

The final project includes:

- Source code published on GitHub.
- Installation and execution manuals.
- A 4–6 page IEEE-style scientific article.
- A 5–10 minute demonstration video.
- A presentation of no more than 10 slides.
- A technical defense by all team members.

## Team

- Julio Cesar Blacio Machuca
- Ariel Jose Llumiquinga Ñacato
