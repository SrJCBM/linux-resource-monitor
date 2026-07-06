"""Modelo de red basado en /proc/net/dev e ip."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


PROC_NET_DEV = Path("/proc/net/dev")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _run_command(args: list[str], timeout: int = 5) -> str:
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env={**os.environ, "LC_ALL": "C"},
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error ejecutando {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def parse_net_dev(text: str) -> dict[str, dict[str, int]]:
    """Parsea contadores de trafico desde /proc/net/dev."""
    interfaces: dict[str, dict[str, int]] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue

        interfaz, values_text = line.split(":", 1)
        values = values_text.split()
        if len(values) < 16:
            continue

        interfaces[interfaz.strip()] = {
            "bytes_recibidos": int(values[0]),
            "paquetes_recibidos": int(values[1]),
            "bytes_enviados": int(values[8]),
            "paquetes_enviados": int(values[9]),
        }
    return interfaces


def parse_ip_addr(text: str) -> dict[str, str]:
    """Devuelve una direccion primaria por interfaz, prefiriendo IPv4."""
    ipv4: dict[str, str] = {}
    ipv6: dict[str, str] = {}
    current_interface: str | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if stripped[0].isdigit() and ": " in stripped:
            _, rest = stripped.split(": ", 1)
            current_interface = rest.split(":", 1)[0].split("@", 1)[0]
            continue

        if current_interface is None:
            continue

        if stripped.startswith("inet ") and current_interface not in ipv4:
            ipv4[current_interface] = stripped.split()[1].split("/", 1)[0]
        elif stripped.startswith("inet6 ") and current_interface not in ipv6:
            ipv6[current_interface] = stripped.split()[1].split("/", 1)[0]

    return {**ipv6, **ipv4}


def build_network_info(net_dev_text: str, ip_addr_text: str) -> list[dict[str, int | str | None]]:
    """Combina trafico e IP primaria por interfaz."""
    traffic = parse_net_dev(net_dev_text)
    addresses = parse_ip_addr(ip_addr_text)
    result: list[dict[str, int | str | None]] = []

    for interfaz, counters in traffic.items():
        result.append(
            {
                "interfaz": interfaz,
                "direccion_ip": addresses.get(interfaz),
                **counters,
            }
        )
    return result


def obtener_info_red() -> list[dict[str, int | str | None]]:
    """Obtiene informacion de red desde /proc/net/dev e ip."""
    return build_network_info(_read_text(PROC_NET_DEV), _run_command(["ip", "addr", "show"]))
