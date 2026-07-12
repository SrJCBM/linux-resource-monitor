"""Pruebas de recoleccion concurrente y consolidacion."""

from __future__ import annotations

import threading
import unittest

from controller.concurrencia_controller import recolectar_con_hilos
from controller.monitor_controller import CapturaIncompletaError, consolidar_captura


class ConcurrenciaControllerTest(unittest.TestCase):
    def test_recolectar_con_hilos_ejecuta_tareas_simultaneas(self) -> None:
        barrera = threading.Barrier(2, timeout=1)

        def tarea(nombre: str) -> str:
            barrera.wait()
            return nombre

        resultado = recolectar_con_hilos(
            {
                "cpu": lambda: tarea("cpu"),
                "memoria": lambda: tarea("memoria"),
            }
        )

        self.assertEqual(resultado["datos"], {"cpu": "cpu", "memoria": "memoria"})
        self.assertEqual(resultado["errores"], {})
        self.assertEqual(len(resultado["evidencias"]), 2)
        self.assertTrue(all(item["hilo"].startswith("monitor-") for item in resultado["evidencias"]))

    def test_recolectar_con_hilos_conserva_error_por_modulo(self) -> None:
        def fallar() -> None:
            raise RuntimeError("lectura no disponible")

        resultado = recolectar_con_hilos({"cpu": lambda: {"uso": 10}, "red": fallar})

        self.assertEqual(resultado["datos"], {"cpu": {"uso": 10}})
        self.assertIn("lectura no disponible", resultado["errores"]["red"])

    def test_consolidar_captura_rechaza_modulos_faltantes(self) -> None:
        with self.assertRaises(CapturaIncompletaError):
            consolidar_captura({"datos": {"cpu": {}}, "errores": {}, "evidencias": []})

    def test_consolidar_captura_acepta_los_seis_modulos(self) -> None:
        datos = {
            "cpu": {},
            "memoria": {},
            "discos": [],
            "red": [],
            "procesos": [],
            "usuarios": [],
        }

        captura = consolidar_captura(
            {"datos": datos, "errores": {}, "evidencias": []}
        )

        self.assertEqual(captura, datos)


if __name__ == "__main__":
    unittest.main()
