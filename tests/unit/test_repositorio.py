"""Pruebas del repositorio transaccional de capturas."""

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from database.conexion import abrir_conexion
from model.repositorio import RepositorioCapturas


def _captura_completa() -> dict[str, object]:
    return {
        "cpu": {
            "modelo": "CPU de prueba",
            "procesadores_logicos": 4,
            "frecuencia_mhz": 1800.0,
            "carga_promedio_1m": 0.42,
            "carga_promedio_5m": 0.37,
            "carga_promedio_15m": 0.31,
            "porcentaje_uso": 25.0,
        },
        "memoria": {
            "mem_total_mb": 8000.0,
            "mem_usada_mb": 3000.0,
            "mem_libre_mb": 1000.0,
            "mem_disponible_mb": 5000.0,
            "swap_total_mb": 2048.0,
            "swap_usada_mb": 512.0,
        },
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
        "procesos": [
            {
                "pid": 1,
                "nombre_proceso": "init",
                "estado": "S",
                "usuario_propietario": "root",
            }
        ],
        "red": [
            {
                "interfaz": "eth0",
                "direccion_ip": "192.168.1.10",
                "bytes_recibidos": 100,
                "bytes_enviados": 200,
                "paquetes_recibidos": 3,
                "paquetes_enviados": 4,
            }
        ],
        "usuarios": [
            {
                "nombre_usuario": "alumno",
                "terminal": "pts/0",
                "inicio_sesion": "2026-07-11 08:30",
            }
        ],
    }


class RepositorioCapturasTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ruta = Path(self.temp_dir.name) / "monitor.sqlite3"
        self.repositorio = RepositorioCapturas(self.ruta)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_crear_y_obtener_captura_completa(self) -> None:
        id_captura = self.repositorio.crear_captura(
            _captura_completa(),
            etiqueta="inicio",
            comentario="captura de prueba",
            usuario_registro="alumno",
        )

        captura = self.repositorio.obtener_captura(id_captura)

        self.assertIsNotNone(captura)
        assert captura is not None
        self.assertEqual(captura["etiqueta"], "inicio")
        self.assertEqual(captura["cpu"]["modelo"], "CPU de prueba")
        disco = captura["discos"][0]
        self.assertEqual(disco["espacio_total_bytes"], 1073741824)
        self.assertEqual(disco["espacio_usado_bytes"], 536870912)
        self.assertEqual(disco["espacio_libre_bytes"], 536870912)
        self.assertNotIn("espacio_total_gb", disco)
        self.assertEqual(captura["red"][0]["paquetes_enviados"], 4)
        self.assertEqual(captura["usuarios"][0]["inicio_sesion"], "2026-07-11 08:30")

    def test_listar_actualizar_y_eliminar_captura(self) -> None:
        id_captura = self.repositorio.crear_captura(_captura_completa())

        listado = self.repositorio.listar_capturas()
        actualizado = self.repositorio.actualizar_captura(
            id_captura, "despues", "metadatos actualizados"
        )
        eliminado = self.repositorio.eliminar_captura(id_captura)

        self.assertEqual(len(listado), 1)
        self.assertTrue(actualizado)
        self.assertTrue(eliminado)
        self.assertIsNone(self.repositorio.obtener_captura(id_captura))

        conexion = abrir_conexion(self.ruta)
        try:
            hijos = conexion.execute(
                "SELECT COUNT(*) FROM procesos_metricas WHERE id_captura = ?",
                (id_captura,),
            ).fetchone()[0]
        finally:
            conexion.close()
        self.assertEqual(hijos, 0)

    def test_listar_por_fecha(self) -> None:
        id_captura = self.repositorio.crear_captura(_captura_completa())
        conexion = abrir_conexion(self.ruta)
        try:
            conexion.execute(
                "UPDATE capturas SET fecha_hora = ? WHERE id_captura = ?",
                ("2026-07-11 10:00:00", id_captura),
            )
            conexion.commit()
        finally:
            conexion.close()

        self.assertEqual(len(self.repositorio.listar_capturas("2026-07-11")), 1)
        self.assertEqual(self.repositorio.listar_capturas("2026-07-10"), [])

    def test_error_en_metrica_revierte_toda_la_captura(self) -> None:
        datos = _captura_completa()
        datos["cpu"] = {"modelo": "incompleta"}

        with self.assertRaises((KeyError, TypeError)):
            self.repositorio.crear_captura(datos)

        self.assertEqual(self.repositorio.listar_capturas(), [])

    def test_normaliza_inicio_sesion_sin_anio_antes_de_persistir(self) -> None:
        datos = _captura_completa()
        datos["usuarios"] = [
            {
                "nombre_usuario": "alumno",
                "terminal": "pts/0",
                "inicio_sesion": "Jul 6 18:29",
            }
        ]

        id_captura = self.repositorio.crear_captura(datos)
        captura = self.repositorio.obtener_captura(id_captura)

        assert captura is not None
        inicio = captura["usuarios"][0]["inicio_sesion"]
        datetime.strptime(inicio, "%Y-%m-%d %H:%M")


if __name__ == "__main__":
    unittest.main()
