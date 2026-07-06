"""Modelo de usuarios conectados basado en who."""

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


def parse_who_output(text: str) -> list[dict[str, str]]:
    """Parsea usuario, terminal e inicio de sesion desde who."""
    usuarios: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        if len(parts) >= 5 and not parts[2][0].isdigit():
            inicio_sesion = f"{parts[2]} {parts[3]} {parts[4]}"
        else:
            inicio_sesion = f"{parts[2]} {parts[3]}"

        usuarios.append(
            {
                "nombre_usuario": parts[0],
                "terminal": parts[1],
                "inicio_sesion": inicio_sesion,
            }
        )
    return usuarios


def obtener_usuarios() -> list[dict[str, str]]:
    """Obtiene usuarios conectados mediante who."""
    return parse_who_output(_run_command(["who"]))
