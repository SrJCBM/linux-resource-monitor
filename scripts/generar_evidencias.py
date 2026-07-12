"""Genera logs reproducibles de las evidencias ejecutadas en Linux."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
LOGS_PREDETERMINADOS = ROOT / "docs" / "evidencias" / "logs"
Ejecutor = Callable[..., subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class CasoEvidencia:
    """Describe un comando verificable y los requisitos que demuestra."""

    nombre: str
    comando: list[str]
    requisitos: str


def casos_predeterminados() -> list[CasoEvidencia]:
    """Devuelve los casos reales que deben ejecutarse desde WSL o Linux."""
    python = sys.executable
    return [
        CasoEvidencia(
            "suite_completa",
            [python, "-m", "unittest", "discover", "-s", "tests"],
            "RNF-01, RNF-06, RNF-09",
        ),
        CasoEvidencia(
            "estado_general",
            [
                python,
                "-c",
                (
                    "from controller.monitor_controller import MonitorController; "
                    "r=MonitorController().obtener_estado_general(); d=r['datos']; "
                    "print({'modulos': sorted(d), 'errores': r['errores'], "
                    "'cpu': d.get('cpu'), 'memoria': d.get('memoria'), "
                    "'discos': len(d.get('discos', [])), 'red': len(d.get('red', [])), "
                    "'procesos': len(d.get('procesos', [])), 'usuarios': len(d.get('usuarios', []))})"
                ),
            ],
            "RF-01 a RF-06, RF-08",
        ),
        CasoEvidencia(
            "crud_sqlite",
            [
                python,
                "-c",
                (
                    "import tempfile; from pathlib import Path; "
                    "from controller.crud_controller import CrudController; "
                    "from controller.monitor_controller import MonitorController; "
                    "from model.repositorio import RepositorioCapturas; "
                    "t=tempfile.TemporaryDirectory(); r=RepositorioCapturas(Path(t.name)/'monitor.sqlite3'); "
                    "c=CrudController(r, recolector=MonitorController().obtener_estado_general); "
                    "i=c.crear_captura('evidencia','CRUD real'); "
                    "print({'id': i, 'listadas': len(c.listar_capturas()), "
                    "'actualizada': c.actualizar_captura(i,'actualizada','ok'), "
                    "'eliminada': c.eliminar_captura(i), 'restantes': len(c.listar_capturas())})"
                ),
            ],
            "RF-09 a RF-12, RNF-03, RNF-13, RNF-14",
        ),
        CasoEvidencia(
            "hilos_y_fork",
            [
                python,
                "-c",
                (
                    "from controller.monitor_controller import MonitorController; "
                    "r=MonitorController().demostrar_concurrencia(); "
                    "print({'hilos': r['recoleccion']['evidencias'], 'errores': r['recoleccion']['errores'], "
                    "'fork': r['fork']})"
                ),
            ],
            "RF-07, RF-08, RNF-07",
        ),
    ]


def generar_evidencias(
    casos: list[CasoEvidencia],
    directorio_salida: Path = LOGS_PREDETERMINADOS,
    ejecutar: Ejecutor = subprocess.run,
) -> list[dict[str, object]]:
    """Ejecuta casos y conserva stdout, stderr y codigo de salida sin alterarlos."""
    directorio_salida.mkdir(parents=True, exist_ok=True)
    resultados: list[dict[str, object]] = []
    for indice, caso in enumerate(casos, start=1):
        resultado = ejecutar(
            caso.comando,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        ruta = directorio_salida / f"{indice:02d}_{caso.nombre}.txt"
        contenido = "\n".join(
            [
                f"Evidence: {caso.nombre}",
                f"Requirements: {caso.requisitos}",
                f"Executed at (UTC): {datetime.now(timezone.utc).isoformat()}",
                f"Command: {' '.join(caso.comando)}",
                f"Return code: {resultado.returncode}",
                "",
                "--- STDOUT ---",
                resultado.stdout.rstrip(),
                "",
                "--- STDERR ---",
                resultado.stderr.rstrip(),
                "",
            ]
        ).rstrip() + "\n"
        ruta.write_text(contenido, encoding="utf-8")
        resultados.append(
            {
                "nombre": caso.nombre,
                "ruta": ruta,
                "exitoso": resultado.returncode == 0,
            }
        )
    return resultados


def main() -> int:
    """Genera los logs de evidencia y devuelve error si algun caso falla."""
    resultados = generar_evidencias(casos_predeterminados())
    for resultado in resultados:
        estado = "OK" if resultado["exitoso"] else "ERROR"
        print(f"{estado}: {resultado['ruta']}")
    return 0 if all(resultado["exitoso"] for resultado in resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
