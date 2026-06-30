import unittest
from pathlib import Path

from model import cpu_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class CpuModelTest(unittest.TestCase):
    def test_parse_cpuinfo_returns_logical_processors_and_frequency(self):
        cpuinfo = (FIXTURES / "proc_cpuinfo.txt").read_text(encoding="utf-8")

        result = cpu_model.parse_cpuinfo(cpuinfo)

        self.assertEqual(result["procesadores_logicos"], 4)
        self.assertEqual(result["modelo"], "Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz")
        self.assertEqual(result["frecuencia_mhz"], 1800.0)

    def test_parse_loadavg_returns_three_load_averages(self):
        loadavg = (FIXTURES / "proc_loadavg.txt").read_text(encoding="utf-8")

        result = cpu_model.parse_loadavg(loadavg)

        self.assertEqual(result["carga_promedio_1m"], 0.42)
        self.assertEqual(result["carga_promedio_5m"], 0.37)
        self.assertEqual(result["carga_promedio_15m"], 0.31)

    def test_calculate_cpu_usage_uses_proc_stat_deltas(self):
        first = (FIXTURES / "proc_stat_1.txt").read_text(encoding="utf-8")
        second = (FIXTURES / "proc_stat_2.txt").read_text(encoding="utf-8")

        first_sample = cpu_model.parse_cpu_stat(first)
        second_sample = cpu_model.parse_cpu_stat(second)
        usage = cpu_model.calculate_cpu_usage(first_sample, second_sample)

        self.assertAlmostEqual(usage, 53.33, places=2)

    def test_build_cpu_info_combines_proc_sources(self):
        cpuinfo = (FIXTURES / "proc_cpuinfo.txt").read_text(encoding="utf-8")
        loadavg = (FIXTURES / "proc_loadavg.txt").read_text(encoding="utf-8")
        stat_1 = (FIXTURES / "proc_stat_1.txt").read_text(encoding="utf-8")
        stat_2 = (FIXTURES / "proc_stat_2.txt").read_text(encoding="utf-8")

        result = cpu_model.build_cpu_info(cpuinfo, loadavg, stat_1, stat_2)

        self.assertEqual(result["procesadores_logicos"], 4)
        self.assertEqual(result["modelo"], "Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz")
        self.assertEqual(result["frecuencia_mhz"], 1800.0)
        self.assertEqual(result["carga_promedio_1m"], 0.42)
        self.assertAlmostEqual(result["porcentaje_uso"], 53.33, places=2)


if __name__ == "__main__":
    unittest.main()
