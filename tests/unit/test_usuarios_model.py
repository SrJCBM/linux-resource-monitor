import unittest
from datetime import datetime
from pathlib import Path

from model import usuarios_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class UsuariosModelTest(unittest.TestCase):
    def test_parse_who_output_returns_login_start_without_duration_formatting(self):
        text = (FIXTURES / "who_output.txt").read_text(encoding="utf-8")

        result = usuarios_model.parse_who_output(text)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["nombre_usuario"], "jcbla")
        self.assertEqual(result[0]["terminal"], "pts/0")
        self.assertEqual(result[0]["inicio_sesion"], "2026-07-06 09:15")

    def test_parse_who_output_normalizes_month_name_for_live_duration(self):
        text = "ariel seat0 Jul 18 15:54\n"

        result = usuarios_model.parse_who_output(
            text, ahora=datetime(2026, 7, 18, 17, 11)
        )

        self.assertEqual(result[0]["inicio_sesion"], "2026-07-18 15:54")

    def test_parse_who_output_uses_previous_year_for_future_candidate(self):
        text = "ariel seat0 Dec 31 23:59\n"

        result = usuarios_model.parse_who_output(
            text, ahora=datetime(2026, 1, 1, 0, 10)
        )

        self.assertEqual(result[0]["inicio_sesion"], "2025-12-31 23:59")


if __name__ == "__main__":
    unittest.main()
