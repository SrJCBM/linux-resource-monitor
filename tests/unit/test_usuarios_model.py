import unittest
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

    def test_parse_who_output_preserves_time_when_lc_all_c_uses_month_name(self):
        text = "jcbla    pts/1        Jul  6 18:29\n"

        result = usuarios_model.parse_who_output(text)

        self.assertEqual(result[0]["inicio_sesion"], "Jul 6 18:29")


if __name__ == "__main__":
    unittest.main()
