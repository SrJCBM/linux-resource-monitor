"""Creacion de conexiones y esquema SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


ESQUEMA_SQL = Path(__file__).with_name("esquema.sql")


def abrir_conexion(ruta_bd: Path) -> sqlite3.Connection:
    """Abre una conexion independiente con claves foraneas activadas."""
    ruta_bd = Path(ruta_bd)
    ruta_bd.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta_bd)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_datos(ruta_bd: Path) -> None:
    """Crea las tablas definidas por el esquema del proyecto."""
    script = ESQUEMA_SQL.read_text(encoding="utf-8")
    conexion = abrir_conexion(ruta_bd)
    try:
        conexion.executescript(script)
        conexion.commit()
    finally:
        conexion.close()
