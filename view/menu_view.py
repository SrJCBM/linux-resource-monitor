"""Menu de consola para el historial de capturas."""

from __future__ import annotations

import unicodedata
from collections.abc import Callable
from typing import Any

from view.consola_view import (
    format_cpu_info,
    format_disco_info,
    format_estado_general,
    format_memoria_info,
    format_procesos_info,
    format_red_info,
    format_usuarios_info,
)


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


def ejecutar_menu_principal(
    monitor: Any,
    crud: Any,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> None:
    """Ejecuta el menu integrado de los modulos de monitoreo y CRUD."""
    formateadores = {
        "2": ("cpu", format_cpu_info),
        "3": ("memoria", format_memoria_info),
        "4": ("procesos", format_procesos_info),
        "5": ("discos", format_disco_info),
        "6": ("red", format_red_info),
        "7": ("usuarios", format_usuarios_info),
    }

    while True:
        output_fn("\n=== MENU PRINCIPAL ===")
        output_fn("[1] Estado general")
        output_fn("[2] CPU")
        output_fn("[3] Memoria y swap")
        output_fn("[4] Procesos")
        output_fn("[5] Disco")
        output_fn("[6] Red")
        output_fn("[7] Usuarios conectados")
        output_fn("[8] Historial y CRUD")
        output_fn("[9] Demostracion de hilos y fork")
        output_fn("[0] Salir")
        opcion = input_fn("Seleccione una opcion: ").strip()

        if opcion == "0":
            output_fn("Hasta luego.")
            return
        if opcion == "1":
            try:
                resultado = monitor.obtener_estado_general()
                output_fn(
                    format_estado_general(
                        resultado.get("datos", {}), resultado.get("errores", {})
                    )
                )
            except (OSError, RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo obtener el estado general: {exc}")
            _esperar_retorno(input_fn)
            continue
        if opcion in formateadores:
            nombre, formateador = formateadores[opcion]
            try:
                output_fn(formateador(monitor.obtener_modulo(nombre)))
            except (OSError, RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo obtener {nombre}: {exc}")
            _esperar_retorno(input_fn)
            continue
        if opcion == "8":
            ejecutar_menu_crud(crud, input_fn, output_fn)
            continue
        if opcion == "9":
            try:
                output_fn(_format_demostracion_concurrencia(monitor.demostrar_concurrencia()))
            except (OSError, RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo ejecutar la demostracion: {exc}")
            _esperar_retorno(input_fn)
            continue
        output_fn("ERROR: Opcion invalida.")


def _esperar_retorno(input_fn: InputFn) -> None:
    input_fn("Presione Enter para volver al menu principal: ")


def _format_demostracion_concurrencia(resultado: dict[str, object]) -> str:
    recoleccion = resultado.get("recoleccion", {})
    fork = resultado.get("fork", {})
    if not isinstance(recoleccion, dict) or not isinstance(fork, dict):
        return "ERROR: La demostracion devolvio un resultado invalido."

    evidencias = recoleccion.get("evidencias", [])
    errores = recoleccion.get("errores", {})
    lineas = [
        "=== DEMOSTRACION DE CONCURRENCIA ===",
        f"Hilos completados: {len(evidencias) if isinstance(evidencias, list) else 0}",
        f"Errores de hilos: {len(errores) if isinstance(errores, dict) else 0}",
        f"PID padre: {fork.get('parent_pid', 'No disponible')}",
        f"PID hijo: {fork.get('child_pid', 'No disponible')}",
        f"Estado de salida: {fork.get('exit_status', 'No disponible')}",
    ]
    return "\n".join(lineas)


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
            try:
                id_captura = controller.crear_captura(etiqueta, comentario)
                output_fn(f"EXITO: captura {id_captura} registrada.")
            except (RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo registrar la captura: {exc}")
        elif opcion == "2":
            fecha = input_fn("Fecha YYYY-MM-DD opcional: ").strip() or None
            try:
                _mostrar_listado(controller.listar_capturas(fecha), output_fn)
            except (RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo listar las capturas: {exc}")
        elif opcion == "3":
            try:
                if _mostrar_capturas_disponibles(controller, output_fn):
                    id_captura = _leer_id(input_fn, output_fn)
                    if id_captura is None:
                        continue
                    captura = controller.consultar_captura(id_captura)
                    if captura is None:
                        output_fn("ADVERTENCIA: captura no encontrada.")
                    else:
                        _mostrar_detalle(captura, output_fn)
            except (RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo consultar la captura: {exc}")
        elif opcion == "4":
            try:
                if _mostrar_capturas_disponibles(controller, output_fn):
                    id_captura = _leer_id(input_fn, output_fn)
                    if id_captura is None:
                        continue
                    etiqueta = input_fn("Nueva etiqueta opcional: ").strip() or None
                    comentario = input_fn("Nuevo comentario opcional: ").strip() or None
                    if controller.actualizar_captura(id_captura, etiqueta, comentario):
                        output_fn("EXITO: metadatos actualizados.")
                    else:
                        output_fn("ADVERTENCIA: captura no encontrada.")
            except (RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo actualizar la captura: {exc}")
        elif opcion == "5":
            try:
                if _mostrar_capturas_disponibles(controller, output_fn):
                    id_captura = _leer_id(input_fn, output_fn)
                    if id_captura is None:
                        continue
                    confirmacion = input_fn(
                        "Escriba SI para confirmar la eliminacion: "
                    ).strip()
                    confirmacion = "".join(
                        caracter
                        for caracter in unicodedata.normalize(
                            "NFD", confirmacion.casefold()
                        )
                        if not unicodedata.combining(caracter)
                    )
                    if confirmacion != "si":
                        output_fn("Eliminacion cancelada.")
                    elif controller.eliminar_captura(id_captura):
                        output_fn("EXITO: captura eliminada.")
                    else:
                        output_fn("ADVERTENCIA: captura no encontrada.")
            except (RuntimeError, ValueError) as exc:
                output_fn(f"ERROR: No se pudo eliminar la captura: {exc}")
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
    output_fn("N. | ID | FECHA Y HORA | ETIQUETA")
    for numero, captura in enumerate(capturas, start=1):
        output_fn(
            f"{numero} | {captura['id_captura']} | {captura['fecha_hora']} | "
            f"{captura.get('etiqueta') or '-'}"
        )


def _mostrar_capturas_disponibles(controller: Any, output_fn: OutputFn) -> bool:
    capturas = controller.listar_capturas()
    if not capturas:
        output_fn("No hay capturas almacenadas.")
        return False
    _mostrar_listado(capturas, output_fn)
    return True


def _mostrar_detalle(captura: dict[str, object], output_fn: OutputFn) -> None:
    output_fn(f"Captura: {captura['id_captura']}")
    output_fn(f"Fecha: {captura['fecha_hora']}")
    output_fn(f"Etiqueta: {captura.get('etiqueta') or '-'}")
    output_fn(f"Comentario: {captura.get('comentario') or '-'}")
    formateadores = {
        "cpu": format_cpu_info,
        "memoria": format_memoria_info,
        "discos": format_disco_info,
        "red": format_red_info,
        "procesos": format_procesos_info,
        "usuarios": format_usuarios_info,
    }
    for modulo in ("cpu", "memoria", "discos", "red", "procesos", "usuarios"):
        valor = captura.get(modulo)
        formateador = formateadores[modulo]
        if modulo in {"cpu", "memoria"} and isinstance(valor, dict):
            output_fn(formateador(valor))
        elif isinstance(valor, list):
            output_fn(formateador(valor))
        else:
            output_fn(f"{modulo.capitalize()}: No disponible")
