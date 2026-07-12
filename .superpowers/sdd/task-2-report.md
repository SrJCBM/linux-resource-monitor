# Informe de Tarea 2 - Fachada de monitoreo

## Estado

DONE

## Alcance realizado

- Se implemento `MonitorController` en `controller/monitor_controller.py`.
- Se agregaron pruebas unitarias en `tests/unit/test_monitor_controller.py`.
- El controlador registra los seis collectors publicos por defecto y acepta
  collectors, funcion de recoleccion concurrente y funcion de fork inyectables.
- `obtener_modulo()` delega y devuelve datos estructurados sin formatear.
- `obtener_estado_general()` preserva el contrato `datos`, `errores` y
  `evidencias` de `recolectar_con_hilos()`.
- `demostrar_concurrencia()` recolecta primero con hilos y solo entonces llama
  a `demostrar_fork()`, evitando el uso de `fork()` con hilos activos.

## TDD y pruebas

1. RED: `python -m unittest tests.unit.test_monitor_controller`
   fallo inicialmente con `ImportError` porque no existian `MonitorController`
   ni `ModuloNoDisponibleError`.
2. GREEN: `python -m unittest tests.unit.test_monitor_controller`
   paso con 4 pruebas.
3. Regresion unitaria: `python -m unittest discover -s tests/unit`
   paso con 43 pruebas.

Las pruebas nuevas cubren delegacion a un collector, modulo desconocido como
error controlado, conservacion de errores parciales y orden de ejecucion entre
recoleccion por hilos y fork.

## Preocupaciones

- La demostracion real de `os.fork()` no se ejecuto en este entorno Windows.
  La prueba verifica el orden de orquestacion mediante inyeccion; la ejecucion
  real debe validarse en Ubuntu, WSL u otra distribucion Linux.
