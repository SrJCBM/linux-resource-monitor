import unittest

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


if __name__ == "__main__":
    unittest.main()
