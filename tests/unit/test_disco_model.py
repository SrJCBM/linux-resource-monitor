import unittest
from pathlib import Path

from model import disco_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class DiscoModelTest(unittest.TestCase):
    def test_parse_df_output_returns_one_record_per_mount_point(self):
        text = (FIXTURES / "df_output.txt").read_text(encoding="utf-8")

        result = disco_model.parse_df_output(text)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["sistema_archivos"], "/dev/sda1")
        self.assertEqual(result[0]["punto_montaje"], "/")
        self.assertEqual(result[0]["espacio_total_bytes"], 1000000000)
        self.assertEqual(result[0]["espacio_usado_bytes"], 400000000)
        self.assertEqual(result[0]["espacio_libre_bytes"], 600000000)
        self.assertEqual(result[0]["porcentaje_uso"], 40.0)


if __name__ == "__main__":
    unittest.main()
