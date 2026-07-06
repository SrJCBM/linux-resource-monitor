"""Modelo de procesos basado en ps."""

from __future__ import annotations

import os
import subprocess


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


def parse_ps_output(text: str) -> list[dict[str, int | str]]:
    """Parsea PID, usuario, estado y nombre desde ps."""
    procesos: list[dict[str, int | str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue

        parts = line.split(maxsplit=3)
        if len(parts) != 4:
            continue

        pid, usuario, estado, nombre = parts
        procesos.append(
            {
                "pid": int(pid),
                "usuario_propietario": usuario,
                "estado": estado,
                "nombre_proceso": nombre,
            }
        )
    return procesos


def obtener_procesos() -> list[dict[str, int | str]]:
    """Obtiene procesos activos mediante ps."""
    return parse_ps_output(_run_command(["ps", "-eo", "pid=,user=,stat=,comm="]))
