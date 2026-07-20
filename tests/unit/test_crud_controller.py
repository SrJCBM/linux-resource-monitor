"""Pruebas de coordinacion del CRUD."""

from __future__ import annotations

import unittest
import sqlite3

from controller.crud_controller import CrudController, CrudOperationError


def _datos_completos() -> dict[str, object]:
    return {
        "cpu": {},
        "memoria": {},
        "discos": [],
        "red": [],
        "procesos": [],
        "usuarios": [],
    }


class RepositorioFalso:
    def __init__(self) -> None:
        self.creada: tuple[dict[str, object], str | None, str | None, str | None] | None = None
        self.eliminados: list[int] = []
        self.fechas_listadas: list[str | None] = []

    def crear_captura(self, datos, etiqueta=None, comentario=None, usuario_registro=None):
        self.creada = (datos, etiqueta, comentario, usuario_registro)
        return 7

    def listar_capturas(self, fecha=None):
        self.fechas_listadas.append(fecha)
        return [{"id_captura": 7, "fecha_hora": "2026-07-11", "etiqueta": "demo"}]

    def obtener_captura(self, id_captura):
        return {"id_captura": id_captura}

    def actualizar_captura(self, id_captura, etiqueta, comentario):
        return id_captura == 7

    def eliminar_captura(self, id_captura):
        self.eliminados.append(id_captura)
        return id_captura == 7


class CrudControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repositorio = RepositorioFalso()
        self.controlador = CrudController(
            self.repositorio,
            recolector=lambda: {
                "datos": _datos_completos(),
                "errores": {},
                "evidencias": [],
            },
        )

    def test_crear_captura_consolida_y_delega_al_repositorio(self) -> None:
        id_captura = self.controlador.crear_captura("demo", "prueba", "alumno")

        self.assertEqual(id_captura, 7)
        assert self.repositorio.creada is not None
        self.assertEqual(self.repositorio.creada[0], _datos_completos())
        self.assertEqual(self.repositorio.creada[1:], ("demo", "prueba", "alumno"))

    def test_operaciones_restantes_delegan_al_repositorio(self) -> None:
        self.assertEqual(len(self.controlador.listar_capturas()), 1)
        self.assertEqual(self.controlador.consultar_captura(7), {"id_captura": 7})
        self.assertTrue(self.controlador.actualizar_captura(7, "nueva", "nota"))
        self.assertTrue(self.controlador.eliminar_captura(7))

    def test_listar_rechaza_fechas_invalidas_antes_del_repositorio(self) -> None:
        for fecha in ("2026/07/18", "18-07-2026", "2026-02-30"):
            with self.subTest(fecha=fecha):
                with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
                    self.controlador.listar_capturas(fecha)

        self.assertEqual(self.repositorio.fechas_listadas, [])

    def test_listar_acepta_fecha_iso_real_y_filtro_ausente(self) -> None:
        self.controlador.listar_capturas("2026-07-18")
        self.controlador.listar_capturas(None)

        self.assertEqual(
            self.repositorio.fechas_listadas, ["2026-07-18", None]
        )

    def test_error_sql_se_convierte_en_error_controlado(self) -> None:
        class RepositorioConError(RepositorioFalso):
            def listar_capturas(self, fecha=None):
                raise sqlite3.OperationalError("base no disponible")

        controlador = CrudController(RepositorioConError(), recolector=self.controlador.recolector)

        with self.assertRaises(CrudOperationError):
            controlador.listar_capturas()


if __name__ == "__main__":
    unittest.main()
