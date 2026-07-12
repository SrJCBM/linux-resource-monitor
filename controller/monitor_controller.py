"""Validacion y consolidacion de capturas de monitoreo."""

from __future__ import annotations

from typing import Any


MODULOS_OBLIGATORIOS = {"cpu", "memoria", "discos", "red", "procesos", "usuarios"}


class CapturaIncompletaError(RuntimeError):
    """Indica que una captura no puede persistirse por datos faltantes."""


def consolidar_captura(resultado: dict[str, Any]) -> dict[str, object]:
    """Valida un resultado concurrente y devuelve sus datos consolidados."""
    datos = resultado.get("datos", {})
    errores = resultado.get("errores", {})
    if not isinstance(datos, dict) or not isinstance(errores, dict):
        raise CapturaIncompletaError("El resultado de monitoreo no es valido.")

    faltantes = MODULOS_OBLIGATORIOS - datos.keys()
    if faltantes or errores:
        detalles = []
        if faltantes:
            detalles.append(f"faltan: {', '.join(sorted(faltantes))}")
        if errores:
            detalles.append(f"errores: {', '.join(sorted(errores))}")
        raise CapturaIncompletaError("Captura incompleta (" + "; ".join(detalles) + ").")

    return {nombre: datos[nombre] for nombre in MODULOS_OBLIGATORIOS}
