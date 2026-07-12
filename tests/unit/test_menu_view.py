"""Pruebas de navegacion del menu CRUD."""

from __future__ import annotations

import unittest

from view.menu_view import ejecutar_menu_crud


class ControladorFalso:
    def __init__(self) -> None:
        self.eliminados: list[int] = []

    def crear_captura(self, etiqueta, comentario, usuario_registro=None):
        return 1

    def listar_capturas(self, fecha=None):
        return []

    def consultar_captura(self, id_captura):
        return None

    def actualizar_captura(self, id_captura, etiqueta, comentario):
        return False

    def eliminar_captura(self, id_captura):
        self.eliminados.append(id_captura)
        return True


class ControladorConError(ControladorFalso):
    def crear_captura(self, etiqueta, comentario, usuario_registro=None):
        raise RuntimeError("captura incompleta")


class ControladorConDetalle(ControladorFalso):
    def consultar_captura(self, id_captura):
        return {
            "id_captura": id_captura,
            "fecha_hora": "2026-07-12 10:00:00",
            "etiqueta": "prueba",
            "comentario": "detalle",
            "cpu": {"modelo": "CPU prueba", "porcentaje_uso": 12.5},
            "memoria": {"mem_total_mb": 100.0, "mem_usada_mb": 25.0},
            "discos": [],
            "red": [],
            "procesos": [],
            "usuarios": [],
        }


class MenuViewTest(unittest.TestCase):
    def test_opcion_invalida_informa_y_permite_volver(self) -> None:
        entradas = iter(["99", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(ControladorFalso(), lambda _: next(entradas), salidas.append)

        self.assertTrue(any("Opcion invalida" in salida for salida in salidas))

    def test_eliminar_requiere_confirmacion_explicita(self) -> None:
        controlador = ControladorFalso()
        entradas = iter(["5", "7", "no", "5", "7", "SI", "0"])

        ejecutar_menu_crud(controlador, lambda _: next(entradas), lambda _: None)

        self.assertEqual(controlador.eliminados, [7])

    def test_error_al_crear_informa_y_permite_continuar(self) -> None:
        entradas = iter(["1", "", "", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(ControladorConError(), lambda _: next(entradas), salidas.append)

        self.assertTrue(any("captura incompleta" in salida for salida in salidas))
        self.assertTrue(any("HISTORIAL DE CAPTURAS" in salida for salida in salidas))

    def test_detalle_formatea_cpu_y_memoria_sin_diccionarios_crudos(self) -> None:
        entradas = iter(["3", "7", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(ControladorConDetalle(), lambda _: next(entradas), salidas.append)

        detalle = "\n".join(salidas)
        self.assertIn("=== CPU ===", detalle)
        self.assertIn("=== MEMORIA ===", detalle)
        self.assertNotIn("'porcentaje_uso'", detalle)


if __name__ == "__main__":
    unittest.main()
