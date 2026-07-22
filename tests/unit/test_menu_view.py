"""Pruebas de navegacion del menu CRUD."""

from __future__ import annotations

import unittest

from view.menu_view import _mostrar_listado, ejecutar_menu_crud


class ControladorFalso:
    def __init__(self) -> None:
        self.eliminados: list[int] = []

    def crear_captura(self, etiqueta, comentario, usuario_registro=None):
        return 1

    def listar_capturas(self, fecha=None):
        return [
            {
                "id_captura": 7,
                "fecha_hora": "2026-07-12 10:00:00",
                "etiqueta": "prueba",
            }
        ]

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


class ControladorConErrorAlListar(ControladorFalso):
    def listar_capturas(self, fecha=None):
        raise RuntimeError("base no disponible")


class ControladorSinCapturas(ControladorFalso):
    def listar_capturas(self, fecha=None):
        return []


class ControladorConDetalle(ControladorFalso):
    def consultar_captura(self, id_captura):
        return {
            "id_captura": id_captura,
            "fecha_hora": "2026-07-12 10:00:00",
            "etiqueta": "prueba",
            "comentario": "detalle",
            "cpu": {"modelo": "CPU prueba", "porcentaje_uso": 12.5},
            "memoria": {"mem_total_mb": 100.0, "mem_usada_mb": 25.0},
            "discos": [
                {
                    "sistema_archivos": "/dev/sda1",
                    "punto_montaje": "/",
                    "espacio_total_bytes": 1073741824,
                    "espacio_usado_bytes": 536870912,
                    "espacio_libre_bytes": 536870912,
                    "porcentaje_uso": 50.0,
                }
            ],
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

    def test_eliminar_acepta_si_sin_importar_mayusculas_o_tilde(self) -> None:
        for confirmacion in ("si", "Si", "sí", "SÍ"):
            with self.subTest(confirmacion=confirmacion):
                controlador = ControladorFalso()
                entradas = iter(["5", "7", confirmacion, "0"])

                ejecutar_menu_crud(
                    controlador, lambda _: next(entradas), lambda _: None
                )

                self.assertEqual(controlador.eliminados, [7])

    def test_listado_separa_numero_visual_del_identificador(self) -> None:
        salidas: list[str] = []

        _mostrar_listado(
            [
                {
                    "id_captura": 9,
                    "fecha_hora": "2026-07-18 10:00:00",
                    "etiqueta": "antes",
                },
                {
                    "id_captura": 4,
                    "fecha_hora": "2026-07-18 11:00:00",
                    "etiqueta": "despues",
                },
            ],
            salidas.append,
        )

        self.assertEqual(
            salidas,
            [
                "N. | ID | FECHA Y HORA | ETIQUETA",
                "1 | 9 | 2026-07-18 10:00:00 | antes",
                "2 | 4 | 2026-07-18 11:00:00 | despues",
            ],
        )

    def test_operaciones_muestran_capturas_antes_de_pedir_id(self) -> None:
        casos = {
            "3": (ControladorConDetalle(), ["3", "7", "0"]),
            "4": (ControladorFalso(), ["4", "7", "", "", "0"]),
            "5": (ControladorFalso(), ["5", "7", "no", "0"]),
        }
        for opcion, (controlador, valores) in casos.items():
            with self.subTest(opcion=opcion):
                entradas = iter(valores)
                eventos: list[tuple[str, str]] = []

                ejecutar_menu_crud(
                    controlador,
                    lambda prompt: (
                        eventos.append(("entrada", prompt)), next(entradas)
                    )[1],
                    lambda salida: eventos.append(("salida", salida)),
                )

                indice_listado = next(
                    (
                        indice
                        for indice, evento in enumerate(eventos)
                        if evento == (
                            "salida", "N. | ID | FECHA Y HORA | ETIQUETA"
                        )
                    ),
                    None,
                )
                indice_id = next(
                    (
                        indice
                        for indice, evento in enumerate(eventos)
                        if evento == ("entrada", "Identificador de captura: ")
                    ),
                    None,
                )
                self.assertIsNotNone(indice_listado)
                self.assertIsNotNone(indice_id)
                assert indice_listado is not None and indice_id is not None
                self.assertLess(indice_listado, indice_id)

    def test_mensajes_sin_capturas_distinguen_historial_y_filtro(self) -> None:
        for opcion in ("3", "4", "5"):
            with self.subTest(opcion=opcion):
                entradas = iter([opcion, "0", "0"])
                solicitudes: list[str] = []
                salidas: list[str] = []

                ejecutar_menu_crud(
                    ControladorSinCapturas(),
                    lambda prompt: (
                        solicitudes.append(prompt), next(entradas)
                    )[1],
                    salidas.append,
                )

                self.assertNotIn("Identificador de captura: ", solicitudes)
                self.assertIn("No hay capturas almacenadas.", salidas)

        entradas = iter(["2", "2026-07-30", "0"])
        salidas_filtro: list[str] = []

        ejecutar_menu_crud(
            ControladorSinCapturas(), lambda _: next(entradas), salidas_filtro.append
        )

        self.assertIn("No hay capturas para la fecha indicada.", salidas_filtro)
        self.assertNotIn("No hay capturas almacenadas.", salidas_filtro)

    def test_error_al_crear_informa_y_permite_continuar(self) -> None:
        entradas = iter(["1", "", "", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(ControladorConError(), lambda _: next(entradas), salidas.append)

        self.assertTrue(any("captura incompleta" in salida for salida in salidas))
        self.assertTrue(any("HISTORIAL DE CAPTURAS" in salida for salida in salidas))

    def test_error_al_listar_informa_y_permite_continuar(self) -> None:
        entradas = iter(["2", "", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(
            ControladorConErrorAlListar(), lambda _: next(entradas), salidas.append
        )

        self.assertTrue(any("base no disponible" in salida for salida in salidas))
        self.assertGreaterEqual(
            sum("HISTORIAL DE CAPTURAS" in salida for salida in salidas), 2
        )

    def test_detalle_formatea_cpu_y_memoria_sin_diccionarios_crudos(self) -> None:
        entradas = iter(["3", "7", "0"])
        salidas: list[str] = []

        ejecutar_menu_crud(ControladorConDetalle(), lambda _: next(entradas), salidas.append)

        detalle = "\n".join(salidas)
        self.assertIn("=== CPU ===", detalle)
        self.assertIn("=== MEMORIA ===", detalle)
        self.assertIn("1.00 GB", detalle)
        self.assertIn("0.50 GB", detalle)
        self.assertNotIn("'porcentaje_uso'", detalle)


if __name__ == "__main__":
    unittest.main()
