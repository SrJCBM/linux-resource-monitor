"""Modelo de usuarios conectados basado en who."""

from __future__ import annotations

import os
import subprocess
from datetime import datetime


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
    """Normaliza fechas ISO o de ``who`` e infiere el ano no futuro.

    ``None`` se conserva para sesiones sin fecha. Los demas valores deben ser
    texto ISO o texto abreviado ``Mon DD HH:MM``; un formato invalido genera un
    error para que la persistencia pueda rechazar una captura inconsistente.
    """
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise TypeError("inicio_sesion debe ser texto o None.")
    texto = valor.strip()
    if not texto:
        raise ValueError("inicio_sesion no puede estar vacio.")

    try:
        return datetime.strptime(texto, "%Y-%m-%d %H:%M").strftime(
            "%Y-%m-%d %H:%M"
        )
    except ValueError:
        pass

    partes = texto.split()
    if len(partes) != 3 or partes[0] not in MESES_WHO:
        raise ValueError(f"Formato de inicio_sesion no reconocido: {valor}")
    try:
        mes = MESES_WHO[partes[0]]
        dia = int(partes[1])
        hora, minuto = (int(parte) for parte in partes[2].split(":"))
        referencia = ahora or datetime.now()
    except (TypeError, ValueError):
        raise ValueError(f"Formato de inicio_sesion no reconocido: {valor}") from None

    for anio in (referencia.year, referencia.year - 1):
        try:
            candidato = datetime(anio, mes, dia, hora, minuto)
        except ValueError:
            continue
        if candidato <= referencia:
            return candidato.strftime("%Y-%m-%d %H:%M")
    raise ValueError(f"Fecha de inicio_sesion no valida: {valor}")


def parse_who_output(
    text: str, ahora: datetime | None = None
) -> list[dict[str, str]]:
    """Parsea ``who`` y devuelve inicios ISO; omite lineas malformadas."""
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

        try:
            inicio_normalizado = normalizar_inicio_sesion(inicio_sesion, ahora)
        except (TypeError, ValueError):
            continue
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
