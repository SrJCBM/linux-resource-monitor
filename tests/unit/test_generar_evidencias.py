"""Pruebas del generador de logs de evidencia."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.generar_evidencias import CasoEvidencia, generar_evidencias


class GenerarEvidenciasTest(unittest.TestCase):
    def test_guarda_comando_y_salida_exitosa_en_archivo_estable(self) -> None:
        caso = CasoEvidencia("prueba", ["python3", "-V"], "RF-01")

        def ejecutar(args, **kwargs):
            return subprocess.CompletedProcess(args, 0, "Python 3\n", "")

        with tempfile.TemporaryDirectory() as temp_dir:
            resultados = generar_evidencias([caso], Path(temp_dir), ejecutar)
            contenido = (Path(temp_dir) / "01_prueba.txt").read_text(encoding="utf-8")

        self.assertTrue(resultados[0]["exitoso"])
        self.assertIn("Command: python3 -V", contenido)
        self.assertIn("Return code: 0", contenido)
        self.assertIn("Python 3", contenido)
        self.assertFalse(contenido.endswith("\n\n"))

    def test_conserva_error_del_comando_sin_reportar_exito(self) -> None:
        caso = CasoEvidencia("fallo", ["false"], "RNF-06")

        def ejecutar(args, **kwargs):
            return subprocess.CompletedProcess(args, 1, "", "fallo controlado\n")

        with tempfile.TemporaryDirectory() as temp_dir:
            resultados = generar_evidencias([caso], Path(temp_dir), ejecutar)
            contenido = (Path(temp_dir) / "01_fallo.txt").read_text(encoding="utf-8")

        self.assertFalse(resultados[0]["exitoso"])
        self.assertIn("Return code: 1", contenido)
        self.assertIn("fallo controlado", contenido)


if __name__ == "__main__":
    unittest.main()
