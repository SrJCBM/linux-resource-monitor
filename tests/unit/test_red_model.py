import unittest
from pathlib import Path

from model import red_model


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class RedModelTest(unittest.TestCase):
    def test_parse_net_dev_returns_bytes_and_packets_per_interface(self):
        text = (FIXTURES / "proc_net_dev.txt").read_text(encoding="utf-8")

        result = red_model.parse_net_dev(text)

        self.assertEqual(result["eth0"]["bytes_recibidos"], 123456)
        self.assertEqual(result["eth0"]["paquetes_recibidos"], 789)
        self.assertEqual(result["eth0"]["bytes_enviados"], 654321)
        self.assertEqual(result["eth0"]["paquetes_enviados"], 987)

    def test_parse_ip_addr_prefers_primary_ipv4_address(self):
        text = (FIXTURES / "ip_output.txt").read_text(encoding="utf-8")

        result = red_model.parse_ip_addr(text)

        self.assertEqual(result["eth0"], "192.168.1.10")
        self.assertEqual(result["lo"], "127.0.0.1")

    def test_build_network_info_combines_traffic_and_addresses(self):
        net_dev = (FIXTURES / "proc_net_dev.txt").read_text(encoding="utf-8")
        ip_addr = (FIXTURES / "ip_output.txt").read_text(encoding="utf-8")

        result = red_model.build_network_info(net_dev, ip_addr)

        eth0 = next(item for item in result if item["interfaz"] == "eth0")
        self.assertEqual(eth0["direccion_ip"], "192.168.1.10")
        self.assertEqual(eth0["bytes_recibidos"], 123456)
        self.assertEqual(eth0["paquetes_enviados"], 987)


if __name__ == "__main__":
    unittest.main()
