# Linux Resource Monitor

A Python-based Linux resource monitor using `/proc`, native system commands, threads, processes and SQLite.

## Overview

**Linux Resource Monitor** is an academic Operating Systems project that collects and presents information about the current state of a Linux system. It provides an interactive terminal interface and stores monitoring captures so they can be created, consulted, updated and deleted.

The application is designed for monitoring and registration only. It does not terminate processes, modify network settings, free memory or alter mounted filesystems.

## Project status

| Stage | Scope | Status |
|---|---|---|
| Week 1 | Requirements, architecture and database design | Completed |
| Week 2 | CPU, memory and `/proc` implementation | In progress |
| Week 3 | Disk, network, users and processes | Pending |
| Week 4 | `os.fork()`, threads and CRUD | Pending |
| Week 5 | Integration, tests and final deliverables | Pending |

> The repository is currently in the Week 2 implementation phase. CPU and memory parsing from `/proc` have initial unit-tested implementations; the remaining modules will become operational as each week is completed.

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

When the initial executable version is available:

```bash
python3 main.py
```

The application is Linux-specific because it uses `/proc` and `os.fork()`.

## Tests

Run the test suite with:

```bash
python3 -m unittest discover -s tests
```

Unit tests should use stored sample outputs. Linux integration tests should be kept separate because live system information changes continuously.

## Database

SQLite is the persistence engine selected for the first version.

The database stores:

- Capture metadata.
- CPU metrics.
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
- Scientific article material.
- Presentation material.
- Demonstration evidence.

## Academic deliverables

The final project includes:

- Source code published on GitHub.
- Installation and execution manuals.
- A 4–6 page IEEE-style scientific article.
- A 5–10 minute demonstration video.
- A presentation of no more than 10 slides.
- A technical defense by all team members.

## Team

- `[Student 1]`
- `[Student 2]`

Replace the placeholders with the team members' names before final delivery.
