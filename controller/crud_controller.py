"""Coordinacion de las operaciones CRUD de capturas."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from controller.concurrencia_controller import recolectar_con_hilos
from controller.monitor_controller import consolidar_captura


class CrudController:
    """Conecta la recoleccion consolidada con el repositorio de capturas."""

    def __init__(
        self,
        repositorio: Any,
        recolector: Callable[[], dict[str, Any]] = recolectar_con_hilos,
    ) -> None:
        self.repositorio = repositorio
        self.recolector = recolector

    def crear_captura(
        self,
        etiqueta: str | None = None,
        comentario: str | None = None,
        usuario_registro: str | None = None,
    ) -> int:
        """Recolecta los seis modulos y persiste una captura completa."""
        captura = consolidar_captura(self.recolector())
        return self.repositorio.crear_captura(
            captura,
            etiqueta=etiqueta,
            comentario=comentario,
            usuario_registro=usuario_registro,
        )

    def listar_capturas(self, fecha: str | None = None) -> list[dict[str, object]]:
        return self.repositorio.listar_capturas(fecha)

    def consultar_captura(self, id_captura: int) -> dict[str, object] | None:
        return self.repositorio.obtener_captura(id_captura)

    def actualizar_captura(
        self, id_captura: int, etiqueta: str | None, comentario: str | None
    ) -> bool:
        return self.repositorio.actualizar_captura(id_captura, etiqueta, comentario)

    def eliminar_captura(self, id_captura: int) -> bool:
        return self.repositorio.eliminar_captura(id_captura)
