"""Validacion y consolidacion de capturas de monitoreo."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from controller.concurrencia_controller import demostrar_fork, recolectar_con_hilos
from model.cpu_model import obtener_info_cpu
from model.disco_model import obtener_info_disco
from model.memoria_model import obtener_info_memoria
from model.procesos_model import obtener_procesos
from model.red_model import obtener_info_red
from model.usuarios_model import obtener_usuarios


MODULOS_OBLIGATORIOS = {"cpu", "memoria", "discos", "red", "procesos", "usuarios"}
Collector = Callable[[], object]
RecolectorConcurrente = Callable[[dict[str, Collector]], dict[str, object]]
DemostradorFork = Callable[[], dict[str, object]]


class CapturaIncompletaError(RuntimeError):
    """Indica que una captura no puede persistirse por datos faltantes."""


class ModuloNoDisponibleError(ValueError):
    """Indica que se solicito un modulo de monitoreo no registrado."""


def _collectors_predeterminados() -> dict[str, Collector]:
    """Devuelve los collectors publicos de los seis modulos del monitor."""
    return {
        "cpu": obtener_info_cpu,
        "memoria": obtener_info_memoria,
        "discos": obtener_info_disco,
        "red": obtener_info_red,
        "procesos": obtener_procesos,
        "usuarios": obtener_usuarios,
    }


class MonitorController:
    """Fachada que coordina la lectura estructurada de los modulos."""

    def __init__(
        self,
        collectors: Mapping[str, Collector] | None = None,
        *,
        recolectar_fn: RecolectorConcurrente = recolectar_con_hilos,
        demostrar_fork_fn: DemostradorFork = demostrar_fork,
    ) -> None:
        self._collectors = dict(collectors) if collectors is not None else _collectors_predeterminados()
        self._recolectar_fn = recolectar_fn
        self._demostrar_fork_fn = demostrar_fork_fn

    def obtener_modulo(self, nombre: str) -> object:
        """Obtiene datos sin formatear de un modulo registrado."""
        try:
            collector = self._collectors[nombre]
        except KeyError as exc:
            raise ModuloNoDisponibleError(
                f"El modulo de monitoreo '{nombre}' no esta disponible."
            ) from exc
        return collector()

    def obtener_estado_general(self) -> dict[str, object]:
        """Recolecta los modulos en hilos y conserva datos, errores y evidencias."""
        return self._recolectar_fn(self._collectors)

    def demostrar_concurrencia(self) -> dict[str, object]:
        """Recolecta primero con hilos y despues ejecuta la evidencia de fork."""
        recoleccion = self.obtener_estado_general()
        evidencia_fork = self._demostrar_fork_fn()
        return {"recoleccion": recoleccion, "fork": evidencia_fork}


def consolidar_captura(resultado: dict[str, Any]) -> dict[str, object]:
    """Valida un resultado concurrente y devuelve sus datos consolidados."""
    datos = resultado.get("datos", {})
    errores = resultado.get("errores", {})
    if not isinstance(datos, dict) or not isinstance(errores, dict):
        raise CapturaIncompletaError("El resultado de monitoreo no es valido.")

    faltantes = MODULOS_OBLIGATORIOS - datos.keys()
    if faltantes or errores:
        detalles = []
        if faltantes:
            detalles.append(f"faltan: {', '.join(sorted(faltantes))}")
        if errores:
            detalles.append(f"errores: {', '.join(sorted(errores))}")
        raise CapturaIncompletaError("Captura incompleta (" + "; ".join(detalles) + ").")

    return {nombre: datos[nombre] for nombre in MODULOS_OBLIGATORIOS}
