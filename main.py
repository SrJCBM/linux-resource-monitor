"""Punto de entrada ejecutable para el CRUD de Semana 4."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from controller.crud_controller import CrudController
from controller.monitor_controller import MonitorController
from model.repositorio import RepositorioCapturas
from view.menu_view import ejecutar_menu_principal


RUTA_BD_PREDETERMINADA = Path(__file__).parent / "database" / "data" / "monitor.sqlite3"


def crear_controlador(ruta_bd: Path = RUTA_BD_PREDETERMINADA) -> CrudController:
    """Compone el controlador CRUD con el repositorio SQLite."""
    return CrudController(RepositorioCapturas(ruta_bd))


def crear_aplicacion(
    ruta_bd: Path = RUTA_BD_PREDETERMINADA,
) -> tuple[MonitorController, CrudController]:
    """Compone los controladores del menu principal integrado."""
    return MonitorController(), crear_controlador(ruta_bd)


def main() -> int:
    """Ejecuta el menu integrado del monitor."""
    try:
        monitor, crud = crear_aplicacion()
        ejecutar_menu_principal(monitor, crud)
    except KeyboardInterrupt:
        print("\nOperacion cancelada por el usuario.")
    except (OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
