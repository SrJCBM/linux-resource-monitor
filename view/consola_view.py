"""Funciones de presentacion inicial para la consola."""

from __future__ import annotations

from datetime import datetime


GIGABYTE_BYTES = 1024**3


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


def _format_table(headers: list[str], rows: list[list[str]]) -> str:
    """Construye una tabla ASCII alineada a partir de cabeceras y filas."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(row: list[str]) -> str:
        cells = (value.ljust(widths[index]) for index, value in enumerate(row))
        return "| " + " | ".join(cells) + " |"

    return "\n".join([separator, format_row(headers), separator, *(format_row(row) for row in rows), separator])


def _format_gigabytes(value: object) -> str:
    return _format_number(float(value or 0) / GIGABYTE_BYTES, "GB")


def _format_session_duration(inicio_sesion: object, ahora: datetime) -> str:
    """Calcula la duracion de una sesion desde una fecha ISO almacenada."""
    try:
        inicio = datetime.fromisoformat(str(inicio_sesion).replace("Z", "+00:00"))
    except ValueError:
        return "No disponible"

    referencia = ahora
    if inicio.tzinfo is not None and referencia.tzinfo is None:
        referencia = referencia.replace(tzinfo=inicio.tzinfo)
    elif inicio.tzinfo is None and referencia.tzinfo is not None:
        referencia = referencia.replace(tzinfo=None)

    minutos = max(0, int((referencia - inicio).total_seconds() // 60))
    horas, minutos = divmod(minutos, 60)
    return f"{horas} h {minutos} min"


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


def format_disco_info(data: list[dict[str, object]]) -> str:
    """Devuelve una tabla legible de los sistemas de archivos montados."""
    if not data:
        return "=== DISCO ===\nNo hay sistemas de archivos montados."

    rows = []
    for item in data:
        porcentaje_uso = float(item.get("porcentaje_uso", 0.0))
        rows.append(
            [
                str(item.get("sistema_archivos") or "No disponible"),
                str(item.get("punto_montaje") or "No disponible"),
                _format_gigabytes(item.get("espacio_total_bytes")),
                _format_gigabytes(item.get("espacio_usado_bytes")),
                _format_gigabytes(item.get("espacio_libre_bytes")),
                _format_number(porcentaje_uso, "%"),
                _estado_por_porcentaje(porcentaje_uso),
            ]
        )

    return "\n".join(
        [
            "=== DISCO ===",
            _format_table(
                ["Sistema de archivos", "Montaje", "Total", "Usado", "Libre", "Uso", "Estado"],
                rows,
            ),
        ]
    )


def format_red_info(data: list[dict[str, object]]) -> str:
    """Devuelve una tabla legible de interfaces y contadores de red."""
    if not data:
        return "=== RED ===\nNo hay interfaces de red disponibles."

    rows = []
    for item in data:
        rows.append(
            [
                str(item.get("interfaz") or "No disponible"),
                str(item.get("direccion_ip") or "No disponible"),
                _format_number(item.get("bytes_recibidos"), "B"),
                _format_number(item.get("bytes_enviados"), "B"),
                _format_number(item.get("paquetes_recibidos")),
                _format_number(item.get("paquetes_enviados")),
            ]
        )

    return "\n".join(
        [
            "=== RED ===",
            _format_table(
                ["Interfaz", "IP", "Bytes recibidos", "Bytes enviados", "Paquetes recibidos", "Paquetes enviados"],
                rows,
            ),
        ]
    )


def format_procesos_info(data: list[dict[str, object]], limite: int = 20) -> str:
    """Devuelve una tabla limitada de procesos activos."""
    procesos = data[: max(0, limite)]
    if not procesos:
        return "=== PROCESOS ===\nNo hay procesos para mostrar."

    rows = [
        [
            str(item.get("pid") or "No disponible"),
            str(item.get("nombre_proceso") or "No disponible"),
            str(item.get("estado") or "No disponible"),
            str(item.get("usuario_propietario") or "No disponible"),
        ]
        for item in procesos
    ]
    return "\n".join(
        [
            "=== PROCESOS ===",
            f"Mostrando {len(procesos)} de {len(data)} procesos",
            _format_table(["PID", "Nombre", "Estado", "Usuario"], rows),
        ]
    )


def format_usuarios_info(data: list[dict[str, object]], ahora: datetime | None = None) -> str:
    """Devuelve usuarios conectados y su duracion de sesion calculada."""
    if not data:
        return "=== USUARIOS ===\nNo hay usuarios conectados."

    referencia = ahora or datetime.now()
    rows = []
    for item in data:
        inicio_sesion = item.get("inicio_sesion")
        rows.append(
            [
                str(item.get("nombre_usuario") or "No disponible"),
                str(item.get("terminal") or "No disponible"),
                str(inicio_sesion or "No disponible"),
                _format_session_duration(inicio_sesion, referencia),
            ]
        )

    return "\n".join(
        [
            "=== USUARIOS ===",
            _format_table(["Usuario", "Terminal", "Inicio de sesion", "Duracion"], rows),
        ]
    )


def format_estado_general(
    data: dict[str, object], errores: dict[str, str] | None = None
) -> str:
    """Devuelve una vista consolidada de los seis modulos de monitoreo."""
    cpu = data.get("cpu") if isinstance(data.get("cpu"), dict) else {}
    memoria = data.get("memoria") if isinstance(data.get("memoria"), dict) else {}
    discos = data.get("discos") if isinstance(data.get("discos"), list) else []
    red = data.get("red") if isinstance(data.get("red"), list) else []
    procesos = data.get("procesos") if isinstance(data.get("procesos"), list) else []
    usuarios = data.get("usuarios") if isinstance(data.get("usuarios"), list) else []

    sections = [
        "=== ESTADO GENERAL ===",
        format_cpu_info(cpu),
        format_memoria_info(memoria),
        format_disco_info(discos),
        format_red_info(red),
        format_procesos_info(procesos),
        format_usuarios_info(usuarios),
    ]
    if errores:
        sections.extend(f"ADVERTENCIA: {modulo}: {mensaje}" for modulo, mensaje in errores.items())
    return "\n\n".join(sections)
