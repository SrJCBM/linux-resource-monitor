"""Menu de consola para el historial de capturas."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def ejecutar_menu_crud(
    controller: Any,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    """Ejecuta el menu CRUD hasta que el usuario elija volver."""
    while True:
        output_fn("\n=== HISTORIAL DE CAPTURAS ===")
        output_fn("[1] Registrar captura")
        output_fn("[2] Listar capturas")
        output_fn("[3] Consultar detalle")
        output_fn("[4] Actualizar metadatos")
        output_fn("[5] Eliminar captura")
        output_fn("[0] Volver")
        opcion = input_fn("Seleccione una opcion: ").strip()

        if opcion == "0":
            return
        if opcion == "1":
            etiqueta = input_fn("Etiqueta opcional: ").strip() or None
            comentario = input_fn("Comentario opcional: ").strip() or None
            id_captura = controller.crear_captura(etiqueta, comentario)
            output_fn(f"EXITO: captura {id_captura} registrada.")
        elif opcion == "2":
            fecha = input_fn("Fecha YYYY-MM-DD opcional: ").strip() or None
            _mostrar_listado(controller.listar_capturas(fecha), output_fn)
        elif opcion == "3":
            id_captura = _leer_id(input_fn, output_fn)
            if id_captura is not None:
                captura = controller.consultar_captura(id_captura)
                if captura is None:
                    output_fn("ADVERTENCIA: captura no encontrada.")
                else:
                    _mostrar_detalle(captura, output_fn)
        elif opcion == "4":
            id_captura = _leer_id(input_fn, output_fn)
            if id_captura is not None:
                etiqueta = input_fn("Nueva etiqueta opcional: ").strip() or None
                comentario = input_fn("Nuevo comentario opcional: ").strip() or None
                if controller.actualizar_captura(id_captura, etiqueta, comentario):
                    output_fn("EXITO: metadatos actualizados.")
                else:
                    output_fn("ADVERTENCIA: captura no encontrada.")
        elif opcion == "5":
            id_captura = _leer_id(input_fn, output_fn)
            if id_captura is not None:
                confirmacion = input_fn("Escriba SI para confirmar la eliminacion: ").strip()
                if confirmacion != "SI":
                    output_fn("Eliminacion cancelada.")
                elif controller.eliminar_captura(id_captura):
                    output_fn("EXITO: captura eliminada.")
                else:
                    output_fn("ADVERTENCIA: captura no encontrada.")
        else:
            output_fn("ERROR: Opcion invalida.")


def _leer_id(input_fn: InputFn, output_fn: OutputFn) -> int | None:
    valor = input_fn("Identificador de captura: ").strip()
    try:
        id_captura = int(valor)
    except ValueError:
        output_fn("ERROR: El identificador debe ser un numero entero.")
        return None
    if id_captura <= 0:
        output_fn("ERROR: El identificador debe ser mayor que cero.")
        return None
    return id_captura


def _mostrar_listado(capturas: list[dict[str, object]], output_fn: OutputFn) -> None:
    if not capturas:
        output_fn("No hay capturas almacenadas.")
        return
    output_fn("ID | FECHA Y HORA | ETIQUETA")
    for captura in capturas:
        output_fn(
            f"{captura['id_captura']} | {captura['fecha_hora']} | "
            f"{captura.get('etiqueta') or '-'}"
        )


def _mostrar_detalle(captura: dict[str, object], output_fn: OutputFn) -> None:
    output_fn(f"Captura: {captura['id_captura']}")
    output_fn(f"Fecha: {captura['fecha_hora']}")
    output_fn(f"Etiqueta: {captura.get('etiqueta') or '-'}")
    output_fn(f"Comentario: {captura.get('comentario') or '-'}")
    for modulo in ("cpu", "memoria", "discos", "red", "procesos", "usuarios"):
        valor = captura.get(modulo)
        if isinstance(valor, list):
            output_fn(f"{modulo.capitalize()}: {len(valor)} registros")
        else:
            output_fn(f"{modulo.capitalize()}: {valor}")
