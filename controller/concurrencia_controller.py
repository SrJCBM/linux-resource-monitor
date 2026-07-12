"""Coordinacion explicita de hilos y procesos del monitor."""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from model.cpu_model import PROC_LOADAVG, obtener_info_cpu, parse_loadavg
from model.disco_model import obtener_info_disco
from model.memoria_model import obtener_info_memoria
from model.procesos_model import obtener_procesos
from model.red_model import obtener_info_red
from model.usuarios_model import obtener_usuarios


TareaMonitoreo = Callable[[], object]


def _tareas_predeterminadas() -> dict[str, TareaMonitoreo]:
    return {
        "cpu": obtener_info_cpu,
        "memoria": obtener_info_memoria,
        "discos": obtener_info_disco,
        "red": obtener_info_red,
        "procesos": obtener_procesos,
        "usuarios": obtener_usuarios,
    }


def recolectar_con_hilos(
    tareas: dict[str, TareaMonitoreo] | None = None,
) -> dict[str, Any]:
    """Ejecuta tareas independientes y devuelve datos, errores y evidencias."""
    tareas_activas = tareas if tareas is not None else _tareas_predeterminadas()
    datos: dict[str, object] = {}
    errores: dict[str, str] = {}
    evidencias: list[dict[str, str]] = []
    bloqueo = threading.Lock()

    def ejecutar(nombre: str, tarea: TareaMonitoreo) -> None:
        inicio = datetime.now(timezone.utc).isoformat()
        error: str | None = None
        try:
            resultado = tarea()
            with bloqueo:
                datos[nombre] = resultado
        except Exception as exc:  # Se convierte en un error controlado por modulo.
            error = f"{type(exc).__name__}: {exc}"
            with bloqueo:
                errores[nombre] = error
        finally:
            fin = datetime.now(timezone.utc).isoformat()
            evidencia = {
                "modulo": nombre,
                "hilo": threading.current_thread().name,
                "inicio": inicio,
                "fin": fin,
            }
            if error is not None:
                evidencia["error"] = error
            with bloqueo:
                evidencias.append(evidencia)

    hilos = [
        threading.Thread(
            target=ejecutar,
            args=(nombre, tarea),
            name=f"monitor-{nombre}",
        )
        for nombre, tarea in tareas_activas.items()
    ]

    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()

    return {"datos": datos, "errores": errores, "evidencias": evidencias}


def demostrar_fork() -> dict[str, int | float | str]:
    """Crea un hijo Linux, recibe una metrica por pipe y lo recolecta."""
    fork_fn = getattr(os, "fork", None)
    if fork_fn is None:
        raise RuntimeError("La demostracion con os.fork() requiere Linux.")

    otros_hilos = [
        hilo
        for hilo in threading.enumerate()
        if hilo is not threading.current_thread() and hilo.is_alive()
    ]
    if otros_hilos:
        raise RuntimeError("No se puede ejecutar os.fork() mientras existan hilos activos.")

    descriptor_lectura, descriptor_escritura = os.pipe()
    parent_pid = os.getpid()
    child_pid = fork_fn()

    if child_pid == 0:
        os.close(descriptor_lectura)
        exit_status = 0
        try:
            carga = parse_loadavg(PROC_LOADAVG.read_text(encoding="utf-8"))
            mensaje = {
                "child_pid": os.getpid(),
                "child_parent_pid": os.getppid(),
                "mensaje": "monitoreo hijo completado",
                "carga_promedio_1m": carga["carga_promedio_1m"],
            }
            with os.fdopen(descriptor_escritura, "w", encoding="utf-8") as pipe:
                json.dump(mensaje, pipe)
        except (OSError, ValueError, TypeError):
            exit_status = 1
        finally:
            os._exit(exit_status)

    os.close(descriptor_escritura)
    with os.fdopen(descriptor_lectura, "r", encoding="utf-8") as pipe:
        contenido = pipe.read()
    _, estado = os.waitpid(child_pid, 0)
    exit_status = os.waitstatus_to_exitcode(estado)
    if exit_status != 0 or not contenido:
        raise RuntimeError(f"El proceso hijo termino con codigo {exit_status}.")

    resultado = json.loads(contenido)
    return {"parent_pid": parent_pid, "exit_status": exit_status, **resultado}
