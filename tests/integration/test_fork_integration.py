"""Validacion real de la demostracion obligatoria con os.fork()."""

from __future__ import annotations

import os
import unittest

from controller.concurrencia_controller import demostrar_fork


@unittest.skipUnless(hasattr(os, "fork"), "os.fork() requiere Linux")
class ForkIntegrationTest(unittest.TestCase):
    def test_demostrar_fork_comunica_pids_y_recolecta_hijo(self) -> None:
        resultado = demostrar_fork()

        self.assertEqual(resultado["parent_pid"], os.getpid())
        self.assertNotEqual(resultado["child_pid"], resultado["parent_pid"])
        self.assertEqual(resultado["child_parent_pid"], resultado["parent_pid"])
        self.assertEqual(resultado["mensaje"], "monitoreo hijo completado")
        self.assertEqual(resultado["exit_status"], 0)


if __name__ == "__main__":
    unittest.main()
