"""Modelo de memoria basado en /proc/meminfo."""

from __future__ import annotations

from pathlib import Path


PROC_MEMINFO = Path("/proc/meminfo")


def _read_text(path: Path) -> str:
    """Lee un archivo de texto del sistema usando UTF-8 tolerante."""
    return path.read_text(encoding="utf-8", errors="replace")


def _kb_to_mb(value_kb: int) -> float:
    return round(value_kb / 1024, 2)


def parse_meminfo(text: str) -> dict[str, float]:
    """Extrae memoria y swap desde /proc/meminfo con las reglas del proyecto."""
    values: dict[str, int] = {}
    for raw_line in text.splitlines():
        if ":" not in raw_line:
            continue

        key, value = raw_line.split(":", 1)
        parts = value.strip().split()
        if not parts:
            continue
        values[key] = int(parts[0])

    required = ("MemTotal", "MemFree", "MemAvailable", "SwapTotal", "SwapFree")
    missing = [key for key in required if key not in values]
    if missing:
        raise ValueError(f"Faltan campos requeridos en /proc/meminfo: {', '.join(missing)}.")

    mem_total = values["MemTotal"]
    mem_disponible = values["MemAvailable"]
    swap_total = values["SwapTotal"]
    swap_free = values["SwapFree"]

    return {
        "mem_total_mb": _kb_to_mb(mem_total),
        "mem_usada_mb": _kb_to_mb(mem_total - mem_disponible),
        "mem_libre_mb": _kb_to_mb(values["MemFree"]),
        "mem_disponible_mb": _kb_to_mb(mem_disponible),
        "swap_total_mb": _kb_to_mb(swap_total),
        "swap_usada_mb": _kb_to_mb(swap_total - swap_free),
    }


def obtener_info_memoria() -> dict[str, float]:
    """Obtiene informacion actual de memoria leyendo /proc/meminfo."""
    return parse_meminfo(_read_text(PROC_MEMINFO))
