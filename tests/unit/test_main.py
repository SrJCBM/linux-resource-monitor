"""Pruebas del punto de composicion de Semana 4."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from controller.crud_controller import CrudController
from main import crear_controlador


class MainTest(unittest.TestCase):
    def test_crear_controlador_inicializa_repositorio_en_ruta_indicada(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ruta = Path(temp_dir) / "monitor.sqlite3"

            controlador = crear_controlador(ruta)

            self.assertIsInstance(controlador, CrudController)
            self.assertTrue(ruta.exists())


if __name__ == "__main__":
    unittest.main()
