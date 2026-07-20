"""Repositorio SQLite para capturas completas del monitor."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from database.conexion import abrir_conexion, inicializar_base_datos
from model.usuarios_model import normalizar_inicio_sesion


BYTES_POR_GB = 1024**3


class RepositorioCapturas:
    """Encapsula las operaciones CRUD y sus transacciones SQLite."""

    def __init__(self, ruta_bd: Path) -> None:
        self.ruta_bd = Path(ruta_bd)
        inicializar_base_datos(self.ruta_bd)

    def crear_captura(
        self,
        datos: dict[str, object],
        etiqueta: str | None = None,
        comentario: str | None = None,
        usuario_registro: str | None = None,
    ) -> int:
        """Guarda una captura y todas sus metricas de forma atomica."""
        conexion = abrir_conexion(self.ruta_bd)
        try:
            with conexion:
                cursor = conexion.execute(
                    """
                    INSERT INTO capturas (etiqueta, comentario, usuario_registro)
                    VALUES (?, ?, ?)
                    """,
                    (etiqueta, comentario, usuario_registro),
                )
                id_captura = int(cursor.lastrowid)
                self._insertar_cpu(conexion, id_captura, _dict(datos, "cpu"))
                self._insertar_memoria(conexion, id_captura, _dict(datos, "memoria"))
                self._insertar_discos(conexion, id_captura, _lista(datos, "discos"))
                self._insertar_procesos(conexion, id_captura, _lista(datos, "procesos"))
                self._insertar_red(conexion, id_captura, _lista(datos, "red"))
                self._insertar_usuarios(conexion, id_captura, _lista(datos, "usuarios"))
            return id_captura
        finally:
            conexion.close()

    def listar_capturas(self, fecha: str | None = None) -> list[dict[str, Any]]:
        """Lista metadatos de capturas, opcionalmente filtrados por fecha ISO."""
        consulta = "SELECT * FROM capturas"
        parametros: tuple[object, ...] = ()
        if fecha:
            consulta += " WHERE fecha_hora LIKE ?"
            parametros = (f"{fecha}%",)
        consulta += " ORDER BY fecha_hora DESC, id_captura DESC"

        conexion = abrir_conexion(self.ruta_bd)
        try:
            return [dict(fila) for fila in conexion.execute(consulta, parametros)]
        finally:
            conexion.close()

    def obtener_captura(self, id_captura: int) -> dict[str, Any] | None:
        """Obtiene una captura y reconstruye sus metricas de disco en bytes."""
        conexion = abrir_conexion(self.ruta_bd)
        try:
            fila = conexion.execute(
                "SELECT * FROM capturas WHERE id_captura = ?", (id_captura,)
            ).fetchone()
            if fila is None:
                return None

            captura: dict[str, Any] = dict(fila)
            cpu = self._obtener_uno(conexion, "cpu_metricas", id_captura)
            if cpu is not None:
                cpu["modelo"] = cpu.pop("modelo_procesador")
                cpu.pop("id_captura", None)
            memoria = self._obtener_uno(conexion, "memoria_metricas", id_captura)
            if memoria is not None:
                memoria.pop("id_captura", None)
            discos = [
                _reconstruir_disco(disco)
                for disco in self._obtener_varios(
                    conexion, "disco_metricas", id_captura
                )
            ]

            captura.update(
                {
                    "cpu": cpu,
                    "memoria": memoria,
                    "discos": discos,
                    "procesos": self._obtener_varios(
                        conexion, "procesos_metricas", id_captura
                    ),
                    "red": self._obtener_varios(conexion, "red_metricas", id_captura),
                    "usuarios": self._obtener_varios(
                        conexion, "usuarios_metricas", id_captura
                    ),
                }
            )
            return captura
        finally:
            conexion.close()

    def actualizar_captura(
        self, id_captura: int, etiqueta: str | None, comentario: str | None
    ) -> bool:
        """Actualiza exclusivamente los metadatos editables de una captura."""
        conexion = abrir_conexion(self.ruta_bd)
        try:
            with conexion:
                cursor = conexion.execute(
                    """
                    UPDATE capturas SET etiqueta = ?, comentario = ?
                    WHERE id_captura = ?
                    """,
                    (etiqueta, comentario, id_captura),
                )
            return cursor.rowcount > 0
        finally:
            conexion.close()

    def eliminar_captura(self, id_captura: int) -> bool:
        """Elimina en cascada y reinicia su secuencia solo si no quedan capturas."""
        conexion = abrir_conexion(self.ruta_bd)
        try:
            with conexion:
                cursor = conexion.execute(
                    "DELETE FROM capturas WHERE id_captura = ?", (id_captura,)
                )
                if cursor.rowcount > 0:
                    hay_capturas = conexion.execute(
                        "SELECT 1 FROM capturas LIMIT 1"
                    ).fetchone()
                    if hay_capturas is None:
                        conexion.execute(
                            "DELETE FROM sqlite_sequence WHERE name = ?",
                            ("capturas",),
                        )
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def _insertar_cpu(
        conexion: sqlite3.Connection, id_captura: int, cpu: dict[str, Any]
    ) -> None:
        conexion.execute(
            """
            INSERT INTO cpu_metricas VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_captura,
                cpu.get("modelo"),
                cpu["procesadores_logicos"],
                cpu.get("frecuencia_mhz"),
                cpu.get("carga_promedio_1m"),
                cpu.get("carga_promedio_5m"),
                cpu.get("carga_promedio_15m"),
                cpu["porcentaje_uso"],
            ),
        )

    @staticmethod
    def _insertar_memoria(
        conexion: sqlite3.Connection, id_captura: int, memoria: dict[str, Any]
    ) -> None:
        conexion.execute(
            "INSERT INTO memoria_metricas VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                id_captura,
                memoria["mem_total_mb"],
                memoria["mem_usada_mb"],
                memoria["mem_libre_mb"],
                memoria["mem_disponible_mb"],
                memoria.get("swap_total_mb"),
                memoria.get("swap_usada_mb"),
            ),
        )

    @staticmethod
    def _insertar_discos(
        conexion: sqlite3.Connection, id_captura: int, discos: list[dict[str, Any]]
    ) -> None:
        conexion.executemany(
            """
            INSERT INTO disco_metricas (
                id_captura, sistema_archivos, punto_montaje, espacio_total_gb,
                espacio_usado_gb, espacio_libre_gb, porcentaje_uso
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    id_captura,
                    disco["sistema_archivos"],
                    disco["punto_montaje"],
                    disco["espacio_total_bytes"] / BYTES_POR_GB,
                    disco["espacio_usado_bytes"] / BYTES_POR_GB,
                    disco["espacio_libre_bytes"] / BYTES_POR_GB,
                    disco.get("porcentaje_uso"),
                )
                for disco in discos
            ],
        )

    @staticmethod
    def _insertar_procesos(
        conexion: sqlite3.Connection,
        id_captura: int,
        procesos: list[dict[str, Any]],
    ) -> None:
        conexion.executemany(
            """
            INSERT INTO procesos_metricas (
                id_captura, pid, nombre_proceso, estado, usuario_propietario
            ) VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    id_captura,
                    proceso["pid"],
                    proceso["nombre_proceso"],
                    proceso.get("estado"),
                    proceso.get("usuario_propietario"),
                )
                for proceso in procesos
            ],
        )

    @staticmethod
    def _insertar_red(
        conexion: sqlite3.Connection, id_captura: int, interfaces: list[dict[str, Any]]
    ) -> None:
        conexion.executemany(
            """
            INSERT INTO red_metricas (
                id_captura, interfaz, direccion_ip, bytes_recibidos,
                bytes_enviados, paquetes_recibidos, paquetes_enviados
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    id_captura,
                    interfaz["interfaz"],
                    interfaz.get("direccion_ip"),
                    interfaz.get("bytes_recibidos"),
                    interfaz.get("bytes_enviados"),
                    interfaz.get("paquetes_recibidos"),
                    interfaz.get("paquetes_enviados"),
                )
                for interfaz in interfaces
            ],
        )

    @staticmethod
    def _insertar_usuarios(
        conexion: sqlite3.Connection, id_captura: int, usuarios: list[dict[str, Any]]
    ) -> None:
        conexion.executemany(
            """
            INSERT INTO usuarios_metricas (
                id_captura, nombre_usuario, terminal, inicio_sesion
            ) VALUES (?, ?, ?, ?)
            """,
            [
                (
                    id_captura,
                    usuario["nombre_usuario"],
                    usuario.get("terminal"),
                    normalizar_inicio_sesion(usuario.get("inicio_sesion")),
                )
                for usuario in usuarios
            ],
        )

    @staticmethod
    def _obtener_uno(
        conexion: sqlite3.Connection, tabla: str, id_captura: int
    ) -> dict[str, Any] | None:
        fila = conexion.execute(
            f"SELECT * FROM {tabla} WHERE id_captura = ?", (id_captura,)
        ).fetchone()
        return dict(fila) if fila is not None else None

    @staticmethod
    def _obtener_varios(
        conexion: sqlite3.Connection, tabla: str, id_captura: int
    ) -> list[dict[str, Any]]:
        filas = conexion.execute(
            f"SELECT * FROM {tabla} WHERE id_captura = ?", (id_captura,)
        )
        resultados = [dict(fila) for fila in filas]
        for resultado in resultados:
            resultado.pop("id_captura", None)
        return resultados


def _dict(datos: dict[str, object], clave: str) -> dict[str, Any]:
    valor = datos[clave]
    if not isinstance(valor, dict):
        raise TypeError(f"{clave} debe ser un diccionario.")
    return valor


def _lista(datos: dict[str, object], clave: str) -> list[dict[str, Any]]:
    valor = datos[clave]
    if not isinstance(valor, list) or not all(isinstance(item, dict) for item in valor):
        raise TypeError(f"{clave} debe ser una lista de diccionarios.")
    return valor


def _reconstruir_disco(fila: dict[str, Any]) -> dict[str, Any]:
    """Restaura en bytes el contrato de disco expuesto por los modelos."""
    resultado = dict(fila)
    resultado["espacio_total_bytes"] = round(
        float(resultado.pop("espacio_total_gb")) * BYTES_POR_GB
    )
    resultado["espacio_usado_bytes"] = round(
        float(resultado.pop("espacio_usado_gb")) * BYTES_POR_GB
    )
    resultado["espacio_libre_bytes"] = round(
        float(resultado.pop("espacio_libre_gb")) * BYTES_POR_GB
    )
    resultado.pop("id_disco_metrica", None)
    return resultado
