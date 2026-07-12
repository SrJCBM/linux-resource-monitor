#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ] || [ ! -f "$1" ]; then
  echo "Uso: bash scripts/mostrar_evidencia.sh <archivo-log>" >&2
  exit 2
fi

cat "$1"
printf '\nPresione Enter para cerrar esta evidencia...'
read -r
