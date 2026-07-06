import unittest
from pathlib import Path

from model import procesos_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class ProcesosModelTest(unittest.TestCase):
    def test_parse_ps_output_returns_pid_user_state_and_name(self):
        text = (FIXTURES / "ps_output.txt").read_text(encoding="utf-8")

        result = procesos_model.parse_ps_output(text)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["pid"], 2345)
        self.assertEqual(result[1]["usuario_propietario"], "jcbla")
        self.assertEqual(result[1]["estado"], "Sl")
        self.assertEqual(result[1]["nombre_proceso"], "python3")


if __name__ == "__main__":
    unittest.main()
