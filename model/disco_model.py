"""Modelo de disco basado en el comando df."""

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


def parse_df_output(text: str) -> list[dict[str, int | float | str]]:
    """Parsea la salida de df -P -B1 y devuelve un registro por montaje."""
    registros: list[dict[str, int | float | str]] = []
    lines = [line for line in text.splitlines() if line.strip()]
    for line in lines[1:]:
        parts = line.split(maxsplit=5)
        if len(parts) != 6:
            continue

        sistema_archivos, total, usado, libre, porcentaje, punto_montaje = parts
        registros.append(
            {
                "sistema_archivos": sistema_archivos,
                "punto_montaje": punto_montaje,
                "espacio_total_bytes": int(total),
                "espacio_usado_bytes": int(usado),
                "espacio_libre_bytes": int(libre),
                "porcentaje_uso": float(porcentaje.rstrip("%")),
            }
        )
    return registros


def obtener_info_disco() -> list[dict[str, int | float | str]]:
    """Obtiene informacion de sistemas de archivos montados."""
    return parse_df_output(_run_command(["df", "-P", "-B1"]))
