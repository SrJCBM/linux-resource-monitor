"""Modelo de usuarios conectados basado en who."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta


MESES_WHO = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


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


def normalizar_inicio_sesion(
    valor: object, ahora: datetime | None = None
) -> str | None:
    """Convierte fechas ISO o de ``who`` a ``YYYY-MM-DD HH:MM``."""
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto:
        return None

    try:
        return datetime.strptime(texto, "%Y-%m-%d %H:%M").strftime(
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        pass

    partes = texto.split()
    if len(partes) != 3 or partes[0] not in MESES_WHO:
        return None
    try:
        mes = MESES_WHO[partes[0]]
        dia = int(partes[1])
        hora, minuto = (int(parte) for parte in partes[2].split(":"))
        referencia = ahora or datetime.now()
        candidato = datetime(referencia.year, mes, dia, hora, minuto)
    except (TypeError, ValueError):
        return None

    if candidato > referencia + timedelta(days=1):
        candidato = candidato.replace(year=referencia.year - 1)
    return candidato.strftime("%Y-%m-%d %H:%M")


def parse_who_output(
    text: str, ahora: datetime | None = None
) -> list[dict[str, str]]:
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

        inicio_normalizado = normalizar_inicio_sesion(inicio_sesion, ahora)
        if inicio_normalizado is None:
            continue

        usuarios.append(
            {
                "nombre_usuario": parts[0],
                "terminal": parts[1],
                "inicio_sesion": inicio_normalizado,
            }
        )
    return usuarios


def obtener_usuarios() -> list[dict[str, str]]:
    """Obtiene usuarios conectados mediante who."""
    return parse_who_output(_run_command(["who"]))
