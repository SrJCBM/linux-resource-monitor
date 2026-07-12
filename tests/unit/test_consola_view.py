import unittest
from datetime import datetime

from view import consola_view


class ConsolaViewTest(unittest.TestCase):
    def test_format_cpu_info_includes_labels_units_and_status_text(self):
        result = consola_view.format_cpu_info(
            {
                "procesadores_logicos": 4,
                "modelo": "CPU de prueba",
                "frecuencia_mhz": 1800.0,
                "carga_promedio_1m": 0.42,
                "carga_promedio_5m": 0.37,
                "carga_promedio_15m": 0.31,
                "porcentaje_uso": 53.333,
            }
        )

        self.assertIn("CPU", result)
        self.assertIn("Procesadores logicos: 4", result)
        self.assertIn("Frecuencia: 1800.00 MHz", result)
        self.assertIn("Uso actual: 53.33 %", result)
        self.assertIn("Estado: NORMAL", result)

    def test_format_memoria_info_distinguishes_free_and_available_memory(self):
        result = consola_view.format_memoria_info(
            {
                "mem_total_mb": 8000.0,
                "mem_usada_mb": 3000.0,
                "mem_libre_mb": 1000.0,
                "mem_disponible_mb": 5000.0,
                "swap_total_mb": 2048.0,
                "swap_usada_mb": 1024.0,
            }
        )

        self.assertIn("MEMORIA", result)
        self.assertIn("Memoria libre: 1000.00 MB", result)
        self.assertIn("Memoria disponible: 5000.00 MB", result)
        self.assertIn("Swap usada: 1024.00 MB", result)
        self.assertIn("Estado: NORMAL", result)

    def test_format_disco_info_converts_bytes_to_gb(self):
        result = consola_view.format_disco_info(
            [
                {
                    "sistema_archivos": "/dev/sda1",
                    "punto_montaje": "/",
                    "espacio_total_bytes": 1073741824,
                    "espacio_usado_bytes": 536870912,
                    "espacio_libre_bytes": 536870912,
                    "porcentaje_uso": 50.0,
                }
            ]
        )

        self.assertIn("/dev/sda1", result)
        self.assertIn("1.00 GB", result)
        self.assertIn("50.00 %", result)
        self.assertIn("NORMAL", result)

    def test_format_red_info_includes_network_packets(self):
        result = consola_view.format_red_info(
            [
                {
                    "interfaz": "eth0",
                    "direccion_ip": "192.168.1.10",
                    "bytes_recibidos": 123456,
                    "bytes_enviados": 654321,
                    "paquetes_recibidos": 789,
                    "paquetes_enviados": 987,
                }
            ]
        )

        self.assertIn("eth0", result)
        self.assertIn("192.168.1.10", result)
        self.assertIn("789.00", result)
        self.assertIn("987.00", result)

    def test_format_procesos_info_limits_displayed_processes(self):
        result = consola_view.format_procesos_info(
            [
                {
                    "pid": 101,
                    "nombre_proceso": "init",
                    "estado": "S",
                    "usuario_propietario": "root",
                },
                {
                    "pid": 202,
                    "nombre_proceso": "python3",
                    "estado": "R",
                    "usuario_propietario": "jcbla",
                },
            ],
            limite=1,
        )

        self.assertIn("101", result)
        self.assertNotIn("202", result)
        self.assertIn("Mostrando 1 de 2 procesos", result)

    def test_format_usuarios_info_reports_when_no_users_are_connected(self):
        result = consola_view.format_usuarios_info([])

        self.assertIn("USUARIOS", result)
        self.assertIn("No hay usuarios conectados", result)

    def test_format_usuarios_info_calculates_duration_from_injected_time(self):
        result = consola_view.format_usuarios_info(
            [
                {
                    "nombre_usuario": "jcbla",
                    "terminal": "pts/0",
                    "inicio_sesion": "2026-07-11T08:30:00",
                }
            ],
            ahora=datetime(2026, 7, 11, 10, 45),
        )

        self.assertIn("2 h 15 min", result)

    def test_format_estado_general_includes_all_modules_and_warnings(self):
        result = consola_view.format_estado_general(
            {
                "cpu": {"porcentaje_uso": 10.0},
                "memoria": {"mem_total_mb": 100.0, "mem_usada_mb": 20.0},
                "discos": [],
                "red": [],
                "procesos": [],
                "usuarios": [],
            },
            errores={"red": "sin direccion IP"},
        )

        self.assertIn("ESTADO GENERAL", result)
        self.assertIn("=== CPU ===", result)
        self.assertIn("=== MEMORIA ===", result)
        self.assertIn("=== DISCO ===", result)
        self.assertIn("=== RED ===", result)
        self.assertIn("=== PROCESOS ===", result)
        self.assertIn("=== USUARIOS ===", result)
        self.assertIn("ADVERTENCIA: red: sin direccion IP", result)


if __name__ == "__main__":
    unittest.main()
