import unittest
from pathlib import Path

from model import memoria_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class MemoriaModelTest(unittest.TestCase):
    def test_parse_meminfo_distinguishes_free_available_and_used_memory(self):
        meminfo = (FIXTURES / "proc_meminfo.txt").read_text(encoding="utf-8")

        result = memoria_model.parse_meminfo(meminfo)

        self.assertEqual(result["mem_total_mb"], 8000.0)
        self.assertEqual(result["mem_libre_mb"], 1000.0)
        self.assertEqual(result["mem_disponible_mb"], 5000.0)
        self.assertEqual(result["mem_usada_mb"], 3000.0)

    def test_parse_meminfo_calculates_used_swap_from_total_minus_free(self):
        meminfo = (FIXTURES / "proc_meminfo.txt").read_text(encoding="utf-8")

        result = memoria_model.parse_meminfo(meminfo)

        self.assertEqual(result["swap_total_mb"], 2048.0)
        self.assertEqual(result["swap_usada_mb"], 1024.0)


if __name__ == "__main__":
    unittest.main()
