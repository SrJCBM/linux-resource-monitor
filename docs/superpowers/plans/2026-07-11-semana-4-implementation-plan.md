# Semana 4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar concurrencia explicita, `os.fork()` y CRUD completo de capturas mediante SQLite.

**Architecture:** Los modelos existentes conservan la recoleccion de recursos. Los controladores consolidan datos y coordinan concurrencia; `model/repositorio.py` encapsula SQL y guarda cada captura completa en una sola transaccion; la Vista solo gestiona presentacion y entrada.

**Tech Stack:** Python 3, biblioteca estandar, `unittest`, `sqlite3`, `threading`, `os.fork()` y WSL Ubuntu.

## Global Constraints

- Mantener MVC y los nombres de archivo documentados.
- Utilizar SQLite como unica persistencia de la primera version.
- Activar `PRAGMA foreign_keys = ON` en cada conexion.
- No compartir conexiones SQLite entre hilos ni procesos.
- No ejecutar `os.fork()` mientras haya hilos de monitoreo activos.
- No agregar dependencias ni funcionalidades de Semana 5.

---

### Task 1: Esquema y conexion SQLite

**Files:**
- Create: `database/__init__.py`
- Create: `database/conexion.py`
- Create: `database/esquema.sql`
- Create: `database/data/.gitkeep`
- Test: `tests/unit/test_conexion.py`

**Interfaces:**
- Produces: `abrir_conexion(ruta_bd: Path) -> sqlite3.Connection`
- Produces: `inicializar_base_datos(ruta_bd: Path) -> None`

- [ ] Escribir pruebas que comprueben la creacion de tablas y `PRAGMA foreign_keys`.
- [ ] Ejecutar `python -m unittest tests.unit.test_conexion` y confirmar fallo por modulo ausente.
- [ ] Copiar el esquema documentado, incluyendo `modelo_procesador`, y crear la conexion minima.
- [ ] Ejecutar nuevamente la prueba y confirmar que pasa.

### Task 2: Repositorio CRUD transaccional

**Files:**
- Create: `model/repositorio.py`
- Test: `tests/unit/test_repositorio.py`

**Interfaces:**
- Consumes: estructura consolidada con `cpu`, `memoria`, `discos`, `red`, `procesos` y `usuarios`.
- Produces: `RepositorioCapturas.crear_captura(datos, etiqueta=None, comentario=None, usuario_registro=None) -> int`
- Produces: `listar_capturas(fecha=None) -> list[dict[str, object]]`
- Produces: `obtener_captura(id_captura) -> dict[str, object] | None`
- Produces: `actualizar_captura(id_captura, etiqueta, comentario) -> bool`
- Produces: `eliminar_captura(id_captura) -> bool`

- [ ] Escribir una prueba de creacion y lectura completa con una base temporal.
- [ ] Confirmar que falla porque el repositorio no existe.
- [ ] Implementar inserciones parametrizadas y conversion de bytes de disco a GB.
- [ ] Escribir y ejecutar pruebas de listado, filtro, actualizacion y eliminacion en cascada.
- [ ] Escribir una prueba de rollback con datos incompletos y comprobar que no queda la captura padre.
- [ ] Ejecutar `python -m unittest tests.unit.test_repositorio` hasta obtener resultado limpio.

### Task 3: Consolidacion y hilos

**Files:**
- Create: `controller/__init__.py`
- Create: `controller/monitor_controller.py`
- Create: `controller/concurrencia_controller.py`
- Test: `tests/unit/test_concurrencia_controller.py`

**Interfaces:**
- Produces: `recolectar_con_hilos(tareas=None) -> dict[str, object]`
- Resultado: `{"datos": {...}, "errores": {...}, "evidencias": [...]}`
- Produces: `consolidar_captura(resultado) -> dict[str, object]`

- [ ] Escribir una prueba con tareas controladas que exija al menos dos objetos `Thread` y resultados por modulo.
- [ ] Confirmar el fallo por modulo ausente.
- [ ] Implementar ranuras aisladas, inicio de todos los hilos antes de `join()` y captura de excepciones.
- [ ] Agregar pruebas de error parcial y validacion de captura incompleta.
- [ ] Ejecutar las pruebas de concurrencia y luego toda la suite.

### Task 4: Demostracion de proceso hijo

**Files:**
- Modify: `controller/concurrencia_controller.py`
- Create: `tests/integration/__init__.py`
- Create: `tests/integration/test_fork_integration.py`

**Interfaces:**
- Produces: `demostrar_fork() -> dict[str, int | str]`

- [ ] Escribir una prueba Linux que valide PID padre, PID hijo, mensaje por pipe y estado de salida.
- [ ] Confirmar el fallo porque la funcion no existe.
- [ ] Implementar `os.pipe()`, `os.fork()`, cierre de descriptores y `os.waitpid()`.
- [ ] Agregar error controlado cuando `os.fork` no este disponible.
- [ ] Ejecutar la prueba en WSL y confirmar que el PID hijo difiere del padre.

### Task 5: Controlador y menu CRUD

**Files:**
- Create: `controller/crud_controller.py`
- Create: `view/menu_view.py`
- Test: `tests/unit/test_crud_controller.py`
- Test: `tests/unit/test_menu_view.py`

**Interfaces:**
- Produces: `CrudController` con crear, listar, consultar, actualizar y eliminar.
- Produces: `ejecutar_menu_crud(controller, input_fn=input, output_fn=print) -> None`

- [ ] Escribir pruebas del controlador usando colaboradores inyectados.
- [ ] Confirmar el fallo por clases ausentes.
- [ ] Implementar validacion de captura completa y delegacion al repositorio.
- [ ] Escribir pruebas de menu para opcion invalida y confirmacion de eliminacion.
- [ ] Implementar menu numerado accesible y mensajes en espanol.
- [ ] Ejecutar las pruebas nuevas y toda la suite.

### Task 6: Documentacion y verificacion

**Files:**
- Modify: `README.md`
- Modify: `docs/Semana1_Analisis_Arquitectura_BD.md`

- [ ] Marcar Semana 3 completa y Semana 4 completada cuando las verificaciones lo demuestren.
- [ ] Documentar comandos para CRUD, hilos y `fork()` en Ubuntu/WSL.
- [ ] Ejecutar `python -m unittest discover -s tests` con el Python local disponible.
- [ ] Ejecutar `python3 -m unittest discover -s tests` dentro de WSL Ubuntu.
- [ ] Ejecutar una captura CRUD real en una base temporal dentro de WSL.
- [ ] Revisar `git diff --check` y confirmar que no se versionaron bases de datos ni caches.
