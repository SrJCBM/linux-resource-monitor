# Task 1 Report: Curate Authoritative Sources and Article Assets

## Status

Implemented and committed in the isolated `articulo-ieee` worktree.

## Deliverables

Created and committed:

- `docs/articulo/referencias.bib`
- `docs/articulo/IEEEtran.cls`
- `docs/articulo/figuras/arquitectura_actual.png`
- `docs/articulo/figuras/evidencia_hilos_fork.png`

The bibliography contains the seven required keys: `silberschatz2019`, `linuxproc`, `pythonos`, `pythonthreading`, `pythonsubprocess`, `sqlitefk`, and `sqlitetransactions`. The source records and access dates follow the task brief verbatim.

The class file was copied from `IEEE-conference-template-062824/IEEEtran.cls`. The two figures were copied from the verified evidence paths specified by the brief. The uploaded template directory was not modified or staged.

## Verification Evidence

Executed in the isolated worktree:

- Bibliography parser check: `7` unique required keys found.
- SHA-256 comparison: source and copied `IEEEtran.cls` match with hash `C972ACA108FDA004C3514D63658E02816DA2E54D9A1451E870B9BD970E003F55`.
- Figure size check: `arquitectura_actual.png` is `72190` bytes; `evidencia_hilos_fork.png` is `58009` bytes.
- Bibliography macro check: passed; all six URLs use single-backslash `\url{...}` and the publisher uses single-backslash `\&`.
- `git diff --check` on `docs/articulo/referencias.bib`: passed.
- `git diff --check` on the copied vendor class: reports upstream trailing whitespace and a blank line at EOF (exit code `2`; 155 trailing-whitespace lines were detected). This is expected because `IEEEtran.cls` was copied byte-for-byte from the supplied template; the vendor asset was not normalized or edited.
- Separate vendor integrity check: source and copied `IEEEtran.cls` have identical SHA-256 hashes.
- Commit-scope check: exactly the four requested `docs/articulo` paths were committed; the correction itself changes only the bibliography and this report outside the committed article assets.
- No test suite was run because this document-assets task explicitly uses asset and repository verification commands in place of TDD.

## Commit

- Original SHA: `877814c` (`docs: add IEEE article sources and assets`)
- Correction SHA: `929924c`.
- Correction subject: `docs: correct IEEE bibliography macros and verification report`

## Concerns

- The uploaded `IEEE-conference-template-062824/` directory remains untracked by design and was not modified or committed.
- Linux runtime behavior was not exercised; this task only curates static article sources and evidence assets.
- The vendor class intentionally retains its source whitespace because the task requires an immutable byte-for-byte copy.
