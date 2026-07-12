"""Flujo integral del monitor con recursos reales de Linux."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from controller.crud_controller import CrudController
from controller.monitor_controller import MonitorController
from model.repositorio import RepositorioCapturas


@unittest.skipUnless(os.name == "posix" and hasattr(os, "fork"), "Requiere Linux con os.fork()")
class AplicacionIntegrationTest(unittest.TestCase):
    def test_recolecta_persiste_actualiza_elimina_y_demuestra_fork(self) -> None:
        monitor = MonitorController()
        with tempfile.TemporaryDirectory() as temp_dir:
            repositorio = RepositorioCapturas(Path(temp_dir) / "monitor.sqlite3")
            crud = CrudController(repositorio, recolector=monitor.obtener_estado_general)

            id_captura = crud.crear_captura("integracion", "prueba Linux")
            captura = crud.consultar_captura(id_captura)
            actualizado = crud.actualizar_captura(id_captura, "actualizada", "CRUD completo")
            demostracion = monitor.demostrar_concurrencia()
            eliminado = crud.eliminar_captura(id_captura)

            self.assertIsNotNone(captura)
            assert captura is not None
            self.assertEqual(captura["cpu"]["procesadores_logicos"], os.cpu_count())
            self.assertIn("mem_total_mb", captura["memoria"])
            self.assertTrue(actualizado)
            self.assertEqual(demostracion["fork"]["exit_status"], 0)
            self.assertNotEqual(
                demostracion["fork"]["parent_pid"], demostracion["fork"]["child_pid"]
            )
            self.assertTrue(eliminado)
            self.assertEqual(repositorio.listar_capturas(), [])


if __name__ == "__main__":
    unittest.main()
