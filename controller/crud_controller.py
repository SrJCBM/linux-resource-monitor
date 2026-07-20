"""Coordinacion de las operaciones CRUD de capturas."""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Callable
from datetime import datetime
from typing import Any

from controller.concurrencia_controller import recolectar_con_hilos
from controller.monitor_controller import consolidar_captura


class CrudOperationError(RuntimeError):
    """Indica un fallo controlado al acceder a las capturas persistidas."""


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
        return self._ejecutar_repositorio(
            lambda: self.repositorio.crear_captura(
                captura,
                etiqueta=etiqueta,
                comentario=comentario,
                usuario_registro=usuario_registro,
            )
        )

    def listar_capturas(self, fecha: str | None = None) -> list[dict[str, object]]:
        """Lista capturas tras validar una fecha real en formato YYYY-MM-DD."""
        if fecha is not None:
            fecha = fecha.strip()
            mensaje = "La fecha debe usar el formato YYYY-MM-DD y ser valida."
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
                raise ValueError(mensaje)
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError as error:
                raise ValueError(mensaje) from error
        return self._ejecutar_repositorio(lambda: self.repositorio.listar_capturas(fecha))

    def consultar_captura(self, id_captura: int) -> dict[str, object] | None:
        """Consulta una captura por su identificador SQLite estable."""
        return self._ejecutar_repositorio(lambda: self.repositorio.obtener_captura(id_captura))

    def actualizar_captura(
        self, id_captura: int, etiqueta: str | None, comentario: str | None
    ) -> bool:
        """Actualiza los metadatos de una captura identificada por su ID."""
        return self._ejecutar_repositorio(
            lambda: self.repositorio.actualizar_captura(id_captura, etiqueta, comentario)
        )

    def eliminar_captura(self, id_captura: int) -> bool:
        """Elimina una captura identificada por su ID estable."""
        return self._ejecutar_repositorio(lambda: self.repositorio.eliminar_captura(id_captura))

    @staticmethod
    def _ejecutar_repositorio(operacion: Callable[[], object]) -> object:
        try:
            return operacion()
        except sqlite3.Error as exc:
            raise CrudOperationError(f"No se pudo acceder a las capturas: {exc}") from exc
