"""Modelo de CPU basado en lecturas directas desde /proc."""

from __future__ import annotations

import time
from pathlib import Path
from typing import TypedDict


PROC_CPUINFO = Path("/proc/cpuinfo")
PROC_STAT = Path("/proc/stat")
PROC_LOADAVG = Path("/proc/loadavg")


class CpuStatSample(TypedDict):
    """Tiempos agregados de CPU leidos desde la linea principal de /proc/stat."""

    total: int
    idle: int


def _read_text(path: Path) -> str:
    """Lee un archivo de texto del sistema usando UTF-8 tolerante."""
    return path.read_text(encoding="utf-8", errors="replace")


def parse_cpuinfo(text: str) -> dict[str, float | int | str | None]:
    """Extrae procesadores logicos, modelo y frecuencia desde /proc/cpuinfo."""
    procesadores_logicos = 0
    modelo: str | None = None
    frecuencia_mhz: float | None = None

    for raw_line in text.splitlines():
        if ":" not in raw_line:
            continue

        key, value = (part.strip() for part in raw_line.split(":", 1))
        if key == "processor":
            procesadores_logicos += 1
        elif key == "model name" and modelo is None:
            modelo = value
        elif key == "cpu MHz" and frecuencia_mhz is None:
            frecuencia_mhz = round(float(value), 2)

    if procesadores_logicos == 0:
        raise ValueError("No se encontraron procesadores logicos en /proc/cpuinfo.")

    return {
        "procesadores_logicos": procesadores_logicos,
        "modelo": modelo,
        "frecuencia_mhz": frecuencia_mhz,
    }


def parse_loadavg(text: str) -> dict[str, float]:
    """Extrae las tres cargas promedio desde /proc/loadavg."""
    parts = text.split()
    if len(parts) < 3:
        raise ValueError("El contenido de /proc/loadavg esta incompleto.")

    return {
        "carga_promedio_1m": float(parts[0]),
        "carga_promedio_5m": float(parts[1]),
        "carga_promedio_15m": float(parts[2]),
    }


def parse_cpu_stat(text: str) -> CpuStatSample:
    """Extrae tiempos total e inactivo desde la linea agregada cpu de /proc/stat."""
    aggregate_line = next(
        (line for line in text.splitlines() if line.startswith("cpu ")),
        None,
    )
    if aggregate_line is None:
        raise ValueError("No se encontro la linea agregada 'cpu' en /proc/stat.")

    fields = aggregate_line.split()
    counters = [int(value) for value in fields[1:]]
    if len(counters) < 5:
        raise ValueError("La linea agregada de /proc/stat esta incompleta.")

    idle = counters[3] + counters[4]
    total = sum(counters)
    return {"total": total, "idle": idle}


def calculate_cpu_usage(first: CpuStatSample, second: CpuStatSample) -> float:
    """Calcula utilizacion de CPU con diferencias entre dos muestras."""
    total_delta = second["total"] - first["total"]
    idle_delta = second["idle"] - first["idle"]
    if total_delta <= 0:
        return 0.0

    active_delta = total_delta - idle_delta
    return round((active_delta / total_delta) * 100, 2)


def build_cpu_info(
    cpuinfo_text: str,
    loadavg_text: str,
    first_stat_text: str,
    second_stat_text: str,
) -> dict[str, float | int | str | None]:
    """Combina las lecturas de CPU requeridas por RF-01."""
    first_sample = parse_cpu_stat(first_stat_text)
    second_sample = parse_cpu_stat(second_stat_text)

    return {
        **parse_cpuinfo(cpuinfo_text),
        **parse_loadavg(loadavg_text),
        "porcentaje_uso": calculate_cpu_usage(first_sample, second_sample),
    }


def obtener_info_cpu(intervalo_segundos: float = 0.1) -> dict[str, float | int | str | None]:
    """Obtiene informacion actual de CPU leyendo /proc directamente."""
    cpuinfo_text = _read_text(PROC_CPUINFO)
    loadavg_text = _read_text(PROC_LOADAVG)
    first_stat_text = _read_text(PROC_STAT)
    time.sleep(intervalo_segundos)
    second_stat_text = _read_text(PROC_STAT)

    return build_cpu_info(cpuinfo_text, loadavg_text, first_stat_text, second_stat_text)
