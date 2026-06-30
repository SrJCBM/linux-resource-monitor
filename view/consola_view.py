"""Funciones de presentacion inicial para la consola."""

from __future__ import annotations


def _format_number(value: object, unit: str = "") -> str:
    number = float(value) if value is not None else 0.0
    suffix = f" {unit}" if unit else ""
    return f"{number:.2f}{suffix}"


def _estado_por_porcentaje(value: float) -> str:
    if value >= 90:
        return "CRITICO"
    if value >= 75:
        return "ADVERTENCIA"
    return "NORMAL"


def format_cpu_info(data: dict[str, object]) -> str:
    """Devuelve una representacion legible de las metricas de CPU."""
    porcentaje_uso = float(data.get("porcentaje_uso", 0.0))
    estado = _estado_por_porcentaje(porcentaje_uso)

    return "\n".join(
        [
            "=== CPU ===",
            f"Modelo: {data.get('modelo') or 'No disponible'}",
            f"Procesadores logicos: {data.get('procesadores_logicos', 0)}",
            f"Frecuencia: {_format_number(data.get('frecuencia_mhz'), 'MHz')}",
            (
                "Carga promedio: "
                f"{_format_number(data.get('carga_promedio_1m'))} / "
                f"{_format_number(data.get('carga_promedio_5m'))} / "
                f"{_format_number(data.get('carga_promedio_15m'))}"
            ),
            f"Uso actual: {_format_number(porcentaje_uso, '%')}",
            f"Estado: {estado}",
        ]
    )


def format_memoria_info(data: dict[str, object]) -> str:
    """Devuelve una representacion legible de las metricas de memoria."""
    total = float(data.get("mem_total_mb", 0.0))
    usada = float(data.get("mem_usada_mb", 0.0))
    porcentaje_uso = (usada / total) * 100 if total else 0.0
    estado = _estado_por_porcentaje(porcentaje_uso)

    return "\n".join(
        [
            "=== MEMORIA ===",
            f"Memoria total: {_format_number(data.get('mem_total_mb'), 'MB')}",
            f"Memoria usada: {_format_number(data.get('mem_usada_mb'), 'MB')}",
            f"Memoria libre: {_format_number(data.get('mem_libre_mb'), 'MB')}",
            f"Memoria disponible: {_format_number(data.get('mem_disponible_mb'), 'MB')}",
            f"Swap total: {_format_number(data.get('swap_total_mb'), 'MB')}",
            f"Swap usada: {_format_number(data.get('swap_usada_mb'), 'MB')}",
            f"Estado: {estado}",
        ]
    )
