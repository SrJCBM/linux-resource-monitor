# Bilingual IEEE Article Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two equivalent 4--6 page IEEE conference articles, one in Spanish and one in English, grounded in the repository implementation and verified WSL evidence.

**Architecture:** Keep the uploaded IEEE template untouched and create a self-contained article workspace under `docs/articulo/`. Both `.tex` files share one BibTeX database and the same copied evidence figures; the Spanish paper establishes the technical narrative and the English paper recreates it with natural academic prose while preserving every result and citation.

**Tech Stack:** LaTeX `IEEEtran`, BibTeX, PNG figures, Pandoc structural validation, portable LaTeX compiler when available, Poppler PDF inspection.

## Global Constraints

- Each language version must contain 4--6 pages in IEEE conference format.
- Authors are Julio Cesar Blacio Machuca and Ariel Jose Llumiquinga Ñacato.
- Shared affiliation is Carrera de Ingenieria de Software, Universidad de las Fuerzas Armadas ESPE, Sangolqui, Ecuador.
- Email and ORCID fields are omitted because the authors have not supplied them.
- The uploaded `IEEE-conference-template-062824/` directory is a read-only source and must not be overwritten.
- Claims must be supported by the implementation, repository documentation, authoritative references, or `docs/evidencias/logs/`.
- The paper must not claim Windows-native support, PostgreSQL, JSON persistence, graphical interfaces, or unmeasured performance.
- Both language versions must use the same figures, result values, citation keys, and section order.
- No new Python application features or project dependencies are introduced.

---

## File Map

- Create `docs/articulo/monitor_recursos_linux_es.tex`: complete Spanish IEEE article.
- Create `docs/articulo/linux_resource_monitor_en.tex`: complete English IEEE article.
- Create `docs/articulo/referencias.bib`: authoritative shared bibliography.
- Create `docs/articulo/IEEEtran.cls`: exact copy of the uploaded IEEE class for self-contained compilation.
- Create `docs/articulo/figuras/arquitectura_actual.png`: architecture figure copied from verified evidence.
- Create `docs/articulo/figuras/evidencia_hilos_fork.png`: WSL concurrency evidence copied from verified evidence.
- Create `docs/articulo/README.md`: compilation, validation, file-purpose, and language-consistency instructions.
- Modify `README.md`: mark both article drafts as implemented and link the article workspace without marking presentation or video complete.

## Task 1: Curate Authoritative Sources and Article Assets

**Files:**
- Create: `docs/articulo/referencias.bib`
- Create: `docs/articulo/IEEEtran.cls`
- Create: `docs/articulo/figuras/arquitectura_actual.png`
- Create: `docs/articulo/figuras/evidencia_hilos_fork.png`

**Interfaces:**
- Consumes: uploaded `IEEE-conference-template-062824/IEEEtran.cls`, verified figures under `docs/evidencias/`, and primary documentation URLs.
- Produces: citation keys `silberschatz2019`, `linuxproc`, `pythonos`, `pythonthreading`, `pythonsubprocess`, `sqlitefk`, and `sqlitetransactions`; shared class and figures for both papers.

- [ ] **Step 1: Create the article directories and copy immutable assets**

Run from repository root:

```powershell
New-Item -ItemType Directory -Force -Path 'docs\articulo\figuras' | Out-Null
Copy-Item -LiteralPath 'IEEE-conference-template-062824\IEEEtran.cls' -Destination 'docs\articulo\IEEEtran.cls'
Copy-Item -LiteralPath 'docs\evidencias\arquitectura_actual.png' -Destination 'docs\articulo\figuras\arquitectura_actual.png'
Copy-Item -LiteralPath 'docs\evidencias\capturas\04_hilos_fork.png' -Destination 'docs\articulo\figuras\evidencia_hilos_fork.png'
```

Expected: four paths exist and the two copied PNG files have nonzero length.

- [ ] **Step 2: Write the shared bibliography**

Create `docs/articulo/referencias.bib` with these exact source records:

```bibtex
@book{silberschatz2019,
  author    = {Abraham Silberschatz and Peter B. Galvin and Greg Gagne},
  title     = {Operating System Concepts},
  edition   = {10},
  publisher = {John Wiley \& Sons},
  year      = {2019},
  isbn      = {978-1-119-45408-3}
}

@misc{linuxproc,
  author  = {{The Linux Kernel Documentation}},
  title   = {The /proc Filesystem},
  howpublished = {\url{https://docs.kernel.org/filesystems/proc.html}},
  note    = {Accessed: Jul. 17, 2026}
}

@misc{pythonos,
  author  = {{Python Software Foundation}},
  title   = {os --- Miscellaneous Operating System Interfaces},
  howpublished = {\url{https://docs.python.org/3/library/os.html}},
  note    = {Accessed: Jul. 17, 2026}
}

@misc{pythonthreading,
  author  = {{Python Software Foundation}},
  title   = {threading --- Thread-Based Parallelism},
  howpublished = {\url{https://docs.python.org/3/library/threading.html}},
  note    = {Accessed: Jul. 17, 2026}
}

@misc{pythonsubprocess,
  author  = {{Python Software Foundation}},
  title   = {subprocess --- Subprocess Management},
  howpublished = {\url{https://docs.python.org/3/library/subprocess.html}},
  note    = {Accessed: Jul. 17, 2026}
}

@misc{sqlitefk,
  author  = {{SQLite Project}},
  title   = {SQLite Foreign Key Support},
  howpublished = {\url{https://www.sqlite.org/foreignkeys.html}},
  note    = {Accessed: Jul. 17, 2026}
}

@misc{sqlitetransactions,
  author  = {{SQLite Project}},
  title   = {Transaction},
  howpublished = {\url{https://www.sqlite.org/lang_transaction.html}},
  note    = {Accessed: Jul. 17, 2026}
}
```

- [ ] **Step 3: Verify bibliography keys and copied assets**

Run:

```powershell
rg -n '^@(book|misc)\{' docs\articulo\referencias.bib
Get-FileHash 'IEEE-conference-template-062824\IEEEtran.cls','docs\articulo\IEEEtran.cls'
Get-Item 'docs\articulo\figuras\arquitectura_actual.png','docs\articulo\figuras\evidencia_hilos_fork.png' | Select-Object Name,Length
```

Expected: seven unique bibliography keys, identical hashes for both class files, and two nonempty PNG files.

- [ ] **Step 4: Commit source material**

```powershell
git add docs/articulo/referencias.bib docs/articulo/IEEEtran.cls docs/articulo/figuras
git commit -m "docs: add IEEE article sources and assets"
```

## Task 2: Write the Spanish IEEE Article

**Files:**
- Create: `docs/articulo/monitor_recursos_linux_es.tex`

**Interfaces:**
- Consumes: all seven bibliography keys and both shared figure paths from Task 1; architecture and evidence described in `docs/Semana1_Analisis_Arquitectura_BD.md` and `docs/evidencias/logs/`.
- Produces: canonical technical narrative and numeric results that the English article must match.

- [ ] **Step 1: Build the IEEE title, author block, abstract, and keywords**

Use `\documentclass[conference]{IEEEtran}`, `inputenc` with UTF-8, `fontenc` with T1, `cite`, `graphicx`, `booktabs`, `url`, and `hyperref`. Use the approved Spanish title and a shared two-author affiliation block without email placeholders.

The abstract must state the problem, the Linux/Python/MVC approach, direct `/proc` reading, explicit threads and `fork()`, SQLite CRUD, and the verified result of 56 passing WSL tests in 150--200 words. Keywords must be: `Linux`, `monitoreo de recursos`, `Python`, `concurrencia`, `SQLite`, and `sistema de archivos proc`.

- [ ] **Step 2: Write Introduction and Background**

Write `\section{Introduccion}` and `\section{Fundamentos y trabajos relacionados}`. Establish resource observability as an operating-system concern using `\cite{silberschatz2019}` and explain `/proc` as a kernel-data interface using `\cite{linuxproc}`. State the educational gap addressed: one terminal application demonstrating monitoring, process creation, thread concurrency, native commands, persistence, and CRUD without high-level monitoring dependencies.

- [ ] **Step 3: Write Methodology**

Create `\section{Metodologia}` with subsections for incremental five-week development, data sources and formulas, concurrency safety, and verification strategy. Include the CPU delta equation:

```latex
\begin{equation}
U_{CPU}=100\left(1-\frac{\Delta T_{idle}}{\Delta T_{total}}\right),
\end{equation}
```

Define used memory as `MemTotal - MemAvailable` and used swap as `SwapTotal - SwapFree`. Explain fixture-based unit tests, temporary SQLite databases, Linux-only integration tests, and WSL execution.

- [ ] **Step 4: Write Architecture and Development**

Create `\section{Arquitectura y desarrollo de la solucion}` with subsections for MVC, monitoring modules, concurrency, and persistence. Insert `figuras/arquitectura_actual.png` as Fig. 1. Include a compact `booktabs` table mapping CPU, memory, processes, users, disk, and network to `/proc` or Linux commands. Cite the Python APIs and SQLite documentation using `pythonos`, `pythonthreading`, `pythonsubprocess`, `sqlitefk`, and `sqlitetransactions`.

- [ ] **Step 5: Write Results and Conclusions**

Create `\section{Resultados y validacion}` with a four-row results table:

```text
Suite completa | 56 pruebas | 0 fallos
Estado general | 6 modulos | 0 errores
CRUD SQLite | crear/listar/actualizar/eliminar | correcto
Concurrencia | 6 hilos + 1 hijo | exit status 0
```

Insert `figuras/evidencia_hilos_fork.png` as Fig. 2 only if the draft remains within six pages; otherwise retain the architecture figure and result table. Explain that the values are a verified execution snapshot, not a performance benchmark. End with `\section{Conclusiones}` covering requirement fulfillment, architectural separation, concurrency ordering, atomic persistence, limitations, and future portability or longer-duration sampling without claiming those features exist.

- [ ] **Step 6: Add references and run structural validation**

End with:

```latex
\bibliographystyle{IEEEtran}
\bibliography{referencias}
```

Run:

```powershell
pandoc -f latex -t plain 'docs\articulo\monitor_recursos_linux_es.tex' -o "$env:TEMP\monitor_es.txt"
rg -n 'Conference Paper Title|Given Name|Identify applicable|TODO|TBD|placeholder' docs\articulo\monitor_recursos_linux_es.tex
rg -n '\\section\{|\\cite\{|\\includegraphics' docs\articulo\monitor_recursos_linux_es.tex
```

Expected: Pandoc exits 0, the placeholder scan returns no matches, and all mandatory sections plus citations and figures are present.

- [ ] **Step 7: Commit the Spanish draft**

```powershell
git add docs/articulo/monitor_recursos_linux_es.tex
git commit -m "docs: draft Spanish IEEE article"
```

## Task 3: Write the English IEEE Article

**Files:**
- Create: `docs/articulo/linux_resource_monitor_en.tex`

**Interfaces:**
- Consumes: the canonical claims, figures, tables, equations, and citation keys from `monitor_recursos_linux_es.tex`.
- Produces: a complete English article with identical technical scope and evidence.

- [ ] **Step 1: Recreate front matter in natural academic English**

Use the approved English title and the exact same authors and affiliation. Write a 150--200 word abstract with the same six technical elements and the same 56-test result. Index terms must be: `Linux`, `resource monitoring`, `Python`, `concurrency`, `SQLite`, and `proc filesystem`.

- [ ] **Step 2: Write all English sections with equivalent claims**

Create visible sections `Introduction`, `Background and Related Work`, `Methodology`, `Solution Architecture and Development`, `Results and Validation`, and `Conclusions`. Preserve the CPU equation, memory formulas, six-module source table, four-row result table, two figure paths, and all seven citation keys. Keep literal Spanish code identifiers in monospace when they refer to actual module or field names.

- [ ] **Step 3: Validate language and structural parity**

Run:

```powershell
pandoc -f latex -t plain 'docs\articulo\linux_resource_monitor_en.tex' -o "$env:TEMP\monitor_en.txt"
rg -n 'Conference Paper Title|Given Name|Identify applicable|TODO|TBD|placeholder' docs\articulo\linux_resource_monitor_en.tex
rg -o '\\cite\{[^}]+\}' docs\articulo\monitor_recursos_linux_es.tex | Sort-Object -Unique
rg -o '\\cite\{[^}]+\}' docs\articulo\linux_resource_monitor_en.tex | Sort-Object -Unique
```

Expected: Pandoc exits 0, no template placeholders remain, and both citation-key sets are identical.

- [ ] **Step 4: Commit the English draft**

```powershell
git add docs/articulo/linux_resource_monitor_en.tex
git commit -m "docs: add English IEEE article version"
```

## Task 4: Compile, Render, and Correct Both Papers

**Files:**
- Modify: `docs/articulo/monitor_recursos_linux_es.tex`
- Modify: `docs/articulo/linux_resource_monitor_en.tex`
- Create: `docs/articulo/README.md`

**Interfaces:**
- Consumes: both complete LaTeX sources, shared bibliography, class, and figures.
- Produces: structurally validated sources, visually checked PDFs when compilation tooling is available, and reproducible build instructions.

- [ ] **Step 1: Detect a LaTeX compiler without changing project dependencies**

Run:

```powershell
Get-Command latexmk,pdflatex,bibtex,tectonic -ErrorAction SilentlyContinue | Select-Object Name,Source
wsl.exe -d Ubuntu -- bash -lc 'for c in latexmk pdflatex bibtex tectonic; do command -v "$c" || true; done'
```

Expected on the current machine: no installed compiler. Use a portable compiler in a temporary tools directory if one can be obtained from an official release; do not commit the binary or add it to project requirements.

- [ ] **Step 2: Compile each language version**

With `latexmk` available, run from `docs/articulo/`:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error monitor_recursos_linux_es.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error linux_resource_monitor_en.tex
```

With `tectonic` available, run:

```powershell
tectonic -X compile monitor_recursos_linux_es.tex
tectonic -X compile linux_resource_monitor_en.tex
```

Expected: two nonempty PDFs and no unresolved-control-sequence errors. If the compiler does not run BibTeX automatically, execute `bibtex` and repeat the LaTeX pass twice.

- [ ] **Step 3: Inspect page count and every rendered page**

Run:

```powershell
pdfinfo docs\articulo\monitor_recursos_linux_es.pdf | Select-String '^Pages:'
pdfinfo docs\articulo\linux_resource_monitor_en.pdf | Select-String '^Pages:'
pdftoppm -png -r 144 docs\articulo\monitor_recursos_linux_es.pdf "$env:TEMP\monitor_es_page"
pdftoppm -png -r 144 docs\articulo\linux_resource_monitor_en.pdf "$env:TEMP\monitor_en_page"
```

Expected: each PDF has 4, 5, or 6 pages. Inspect every PNG for clipped columns, unreadable figures, table overflow, bad references, mixed-language text, and large blank areas. Correct the `.tex` files and repeat compilation until both pass.

- [ ] **Step 4: Write reproducible article instructions**

Create `docs/articulo/README.md` documenting both source files, shared assets, `latexmk` commands, Pandoc fallback checks, and the verified page count. State explicitly if PDF compilation could not be performed and do not claim visual QA in that case.

- [ ] **Step 5: Commit verified article output**

Commit source and README. Commit PDFs only if the team wants final compiled deliverables versioned; otherwise leave LaTeX auxiliary files ignored and deliver source-only output.

```powershell
git add docs/articulo/monitor_recursos_linux_es.tex docs/articulo/linux_resource_monitor_en.tex docs/articulo/README.md
git commit -m "docs: validate bilingual IEEE article drafts"
```

## Task 5: Synchronize Repository Status and Run Final Review

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: final validated article files and page-count results from Task 4.
- Produces: accurate Week 5 status without marking presentation or video complete.

- [ ] **Step 1: Update the repository documentation status**

Add links to both article sources under the documentation section. Change the Week 5 note to state that bilingual IEEE article drafts are available, while presentation and demonstration video remain pending.

- [ ] **Step 2: Run final consistency checks**

Run:

```powershell
git diff --check
rg -n '56 pruebas|56 tests|6 modulos|six modules|exit status 0|codigo de salida cero' docs\articulo -g '*.tex'
rg -n 'Presentacion|Presentation|video' README.md docs\articulo\README.md
python -m unittest discover -s tests
wsl.exe -d Ubuntu -- bash -lc "cd '/mnt/c/Users/jcbla/Desktop/ESPE/Sexto Semestre/Sistemas Operativos/3P/linux-resource-monitor' && python3 -m unittest discover -s tests"
```

Expected: no whitespace errors, matching bilingual result claims, presentation/video still marked pending, 56 Windows tests with two Linux-only skips, and 56 passing WSL tests.

- [ ] **Step 3: Commit documentation synchronization**

```powershell
git add README.md docs/articulo
git commit -m "docs: publish bilingual IEEE article drafts"
```
