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


if __name__ == "__main__":
    unittest.main()
