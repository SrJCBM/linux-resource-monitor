# Proposed Repository Structure

This structure expands the Week 1 MVC design without changing its responsibilities.

```text
linux-resource-monitor/
│
├── AGENTS.md
│   └── Permanent implementation instructions for Codex and other coding agents.
│
├── README.md
│   └── General repository overview, setup, execution and project status.
│
├── .gitignore
│   └── Excludes virtual environments, caches, runtime databases, logs and IDE files.
│
├── requirements.txt
│   └── External Python dependencies. Keep empty if only the standard library is used.
│
├── main.py
│   └── Application entry point. Creates the controllers and starts the main menu.
│
├── model/
│   ├── __init__.py
│   ├── cpu_model.py
│   ├── memoria_model.py
│   ├── procesos_model.py
│   ├── usuarios_model.py
│   ├── disco_model.py
│   ├── red_model.py
│   └── repositorio.py
│
├── view/
│   ├── __init__.py
│   ├── consola_view.py
│   └── menu_view.py
│
├── controller/
│   ├── __init__.py
│   ├── monitor_controller.py
│   ├── concurrencia_controller.py
│   └── crud_controller.py
│
├── database/
│   ├── __init__.py
│   ├── conexion.py
│   ├── esquema.sql
│   └── data/
│       └── .gitkeep
│
├── docs/
│   ├── Proyecto_Integrador_SO.docx
│   ├── Semana1_Analisis_Arquitectura_BD.md
│   ├── ESTRUCTURA_PROYECTO.md
│   ├── manual_instalacion.md
│   ├── manual_ejecucion.md
│   ├── articulo/
│   │   └── README.md
│   ├── presentacion/
│   │   └── README.md
│   └── evidencias/
│       └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_cpu_model.py
│   │   ├── test_memoria_model.py
│   │   ├── test_procesos_model.py
│   │   ├── test_usuarios_model.py
│   │   ├── test_disco_model.py
│   │   ├── test_red_model.py
│   │   └── test_repositorio.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_linux_integration.py
│   └── fixtures/
│       ├── proc_cpuinfo.txt
│       ├── proc_stat_1.txt
│       ├── proc_stat_2.txt
│       ├── proc_loadavg.txt
│       ├── proc_meminfo.txt
│       ├── proc_net_dev.txt
│       ├── ps_output.txt
│       ├── who_output.txt
│       ├── df_output.txt
│       └── ip_output.txt
│
└── logs/
    └── .gitkeep
```

## Folder responsibilities

### `model/`

Contains system-data and persistence logic.

- Reads `/proc`.
- Executes native commands through `subprocess`.
- Parses raw output.
- Returns dictionaries or dataclasses.
- Provides CRUD methods through `repositorio.py`.

It must not display menus or ask the user for input.

### `view/`

Contains terminal presentation.

- Main and secondary menus.
- Tables and headings.
- Input prompts.
- Pagination.
- Success, warning and error messages.
- Unit and date formatting.

It must not access `/proc`, run commands or query SQLite.

### `controller/`

Coordinates the application.

- Requests data from Models.
- Sends results to Views.
- Consolidates monitoring captures.
- Coordinates `threading.Thread`.
- Coordinates the `os.fork()` demonstration.
- Validates CRUD operation flow.

It must not contain raw SQL or operating-system parsers.

### `database/`

Contains SQLite-specific infrastructure.

- `conexion.py`: opens connections and enables foreign keys.
- `esquema.sql`: creates all tables.
- `data/`: stores runtime database files.

Files under `database/data/` should normally be ignored except `.gitkeep`.

### `docs/`

Contains academic and user documentation.

The original professor specification and the Week 1 design should remain here so Codex can read them before implementation.

### `tests/unit/`

Contains deterministic tests for parsers, controllers and repository operations.

Use fixture text instead of relying only on the computer's live `/proc` contents.

### `tests/integration/`

Contains Linux-only tests that access the real `/proc` filesystem or native commands.

These tests must not require administrator privileges.

### `tests/fixtures/`

Contains stable samples of `/proc` files and command output.

CPU utilization requires two separate `/proc/stat` samples.

### `logs/`

May contain runtime demonstration logs, such as parent PID, child PID and thread timestamps.

Generated log files should be ignored by Git.

## Recommended `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
.venv/
venv/
env/

# Test and tooling caches
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Runtime databases
*.db
*.sqlite
*.sqlite3
!database/data/.gitkeep

# Logs
*.log
!logs/.gitkeep

# Environment files
.env
.env.*

# IDEs
.vscode/
.idea/

# Operating systems
.DS_Store
Thumbs.db
```

## Incremental creation by week

### Week 1

Create:

- `README.md`
- `AGENTS.md`
- `docs/`
- `database/esquema.sql`
- Empty package folders if desired

Do not add placeholder implementations that pretend to work.

### Week 2

Implement and test:

- `model/cpu_model.py`
- `model/memoria_model.py`
- Relevant fixture and unit-test files
- Initial terminal presentation for CPU and memory

### Week 3

Implement and test:

- `model/disco_model.py`
- `model/red_model.py`
- `model/procesos_model.py`
- `model/usuarios_model.py`
- Corresponding fixtures and tests

### Week 4

Implement and test:

- `controller/concurrencia_controller.py`
- `model/repositorio.py`
- `database/conexion.py`
- CRUD controller and menus
- SQLite repository tests
- Fork and thread evidence

### Week 5

Complete:

- Integration tests
- Installation and execution manuals
- Evidence
- Article
- Presentation
- Final corrections

## Notes

- `__init__.py` files keep directories importable as Python packages.
- Avoid adding a large generic `utils/` folder. Place behavior in the layer that owns it.
- Add a small helper module only when the same focused behavior is genuinely reused.
- Keep generated databases, logs, screenshots and videos out of source-code folders.
