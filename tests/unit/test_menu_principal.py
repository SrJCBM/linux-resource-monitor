"""Pruebas de navegacion del menu principal integrado."""

from __future__ import annotations

import unittest

from view.menu_view import ejecutar_menu_principal


class MonitorFalso:
    def __init__(self) -> None:
        self.modulos: list[str] = []

    def obtener_estado_general(self):
        return {
            "datos": {
                "cpu": {"porcentaje_uso": 10.0},
                "memoria": {"mem_total_mb": 100.0, "mem_usada_mb": 20.0},
                "discos": [],
                "red": [],
                "procesos": [],
                "usuarios": [],
            },
            "errores": {},
            "evidencias": [],
        }

    def obtener_modulo(self, nombre):
        self.modulos.append(nombre)
        return {
            "cpu": {"porcentaje_uso": 10.0},
            "memoria": {"mem_total_mb": 100.0, "mem_usada_mb": 20.0},
            "procesos": [],
            "discos": [],
            "red": [],
            "usuarios": [],
        }[nombre]

    def demostrar_concurrencia(self):
        return {
            "recoleccion": {"evidencias": [{"hilo": "monitor-cpu"}], "errores": {}},
            "fork": {"parent_pid": 10, "child_pid": 11, "exit_status": 0},
        }


class CrudFalso:
    def crear_captura(self, etiqueta, comentario, usuario_registro=None):
        return 1

    def listar_capturas(self, fecha=None):
        return []

    def consultar_captura(self, id_captura):
        return None

    def actualizar_captura(self, id_captura, etiqueta, comentario):
        return False

    def eliminar_captura(self, id_captura):
        return False


class MenuPrincipalTest(unittest.TestCase):
    def test_menu_cpu_muestra_datos_y_permite_regresar(self) -> None:
        entradas = iter(["2", "", "0"])
        salidas: list[str] = []
        monitor = MonitorFalso()

        ejecutar_menu_principal(monitor, CrudFalso(), lambda _: next(entradas), salidas.append)

        self.assertEqual(monitor.modulos, ["cpu"])
        self.assertTrue(any("=== CPU ===" in salida for salida in salidas))

    def test_menu_dirige_los_seis_modulos_y_estado_general(self) -> None:
        entradas = iter(["1", "", "3", "", "4", "", "5", "", "6", "", "7", "", "0"])
        salidas: list[str] = []
        monitor = MonitorFalso()

        ejecutar_menu_principal(monitor, CrudFalso(), lambda _: next(entradas), salidas.append)

        self.assertEqual(monitor.modulos, ["memoria", "procesos", "discos", "red", "usuarios"])
        self.assertTrue(any("=== ESTADO GENERAL ===" in salida for salida in salidas))

    def test_menu_muestra_demostracion_concurrente_e_informa_opcion_invalida(self) -> None:
        entradas = iter(["99", "9", "", "0"])
        salidas: list[str] = []

        ejecutar_menu_principal(MonitorFalso(), CrudFalso(), lambda _: next(entradas), salidas.append)

        self.assertTrue(any("Opcion invalida" in salida for salida in salidas))
        self.assertTrue(any("PID padre: 10" in salida for salida in salidas))

    def test_menu_abre_historial_y_vuelve_al_principal(self) -> None:
        entradas = iter(["8", "0", "0"])
        salidas: list[str] = []

        ejecutar_menu_principal(MonitorFalso(), CrudFalso(), lambda _: next(entradas), salidas.append)

        self.assertGreaterEqual(sum("=== MENU PRINCIPAL ===" in salida for salida in salidas), 2)


if __name__ == "__main__":
    unittest.main()
