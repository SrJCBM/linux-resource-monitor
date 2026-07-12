"""Pruebas de la fachada de monitoreo en el controlador."""

from __future__ import annotations

import unittest

from controller.monitor_controller import ModuloNoDisponibleError, MonitorController


class MonitorControllerTest(unittest.TestCase):
    def test_obtener_modulo_delega_en_el_collector_registrado(self) -> None:
        controller = MonitorController(collectors={"cpu": lambda: {"uso": 10}})

        self.assertEqual(controller.obtener_modulo("cpu"), {"uso": 10})

    def test_obtener_modulo_desconocido_es_un_error_controlado(self) -> None:
        with self.assertRaises(ModuloNoDisponibleError):
            MonitorController(collectors={}).obtener_modulo("desconocido")

    def test_obtener_estado_general_conserva_errores_parciales(self) -> None:
        esperado = {
            "datos": {"cpu": {"uso": 10}},
            "errores": {"red": "RuntimeError: interfaz no disponible"},
            "evidencias": [{"modulo": "cpu", "hilo": "monitor-cpu"}],
        }

        controller = MonitorController(
            collectors={"cpu": lambda: {"uso": 10}},
            recolectar_fn=lambda tareas: esperado,
        )

        self.assertEqual(controller.obtener_estado_general(), esperado)

    def test_demostrar_concurrencia_ejecuta_fork_despues_de_recolectar(self) -> None:
        eventos: list[str] = []
        recoleccion = {"datos": {}, "errores": {}, "evidencias": []}
        evidencia_fork = {"parent_pid": 10, "child_pid": 11, "exit_status": 0}

        def recolectar(tareas: object) -> dict[str, object]:
            eventos.append("recolectar")
            return recoleccion

        def demostrar_fork() -> dict[str, int]:
            self.assertEqual(eventos, ["recolectar"])
            eventos.append("fork")
            return evidencia_fork

        controller = MonitorController(
            collectors={"cpu": lambda: {"uso": 10}},
            recolectar_fn=recolectar,
            demostrar_fork_fn=demostrar_fork,
        )

        self.assertEqual(
            controller.demostrar_concurrencia(),
            {"recoleccion": recoleccion, "fork": evidencia_fork},
        )
        self.assertEqual(eventos, ["recolectar", "fork"])


if __name__ == "__main__":
    unittest.main()
