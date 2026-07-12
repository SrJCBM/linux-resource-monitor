"""Pruebas de la infraestructura SQLite."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from database.conexion import abrir_conexion, inicializar_base_datos


class ConexionTest(unittest.TestCase):
    def test_abrir_conexion_activa_claves_foraneas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ruta = Path(temp_dir) / "monitor.sqlite3"
            conexion = abrir_conexion(ruta)
            try:
                estado = conexion.execute("PRAGMA foreign_keys").fetchone()[0]
            finally:
                conexion.close()

        self.assertEqual(estado, 1)

    def test_inicializar_base_datos_crea_todas_las_tablas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ruta = Path(temp_dir) / "monitor.sqlite3"
            inicializar_base_datos(ruta)
            conexion = abrir_conexion(ruta)
            try:
                tablas = {
                    fila[0]
                    for fila in conexion.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
            finally:
                conexion.close()

        self.assertTrue(
            {
                "capturas",
                "cpu_metricas",
                "memoria_metricas",
                "disco_metricas",
                "procesos_metricas",
                "red_metricas",
                "usuarios_metricas",
            }.issubset(tablas)
        )


if __name__ == "__main__":
    unittest.main()
