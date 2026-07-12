# Manual de instalacion

## Requisitos

El proyecto se ejecuta en Linux. Puede utilizar Ubuntu, otra distribucion Linux
compatible o Ubuntu dentro de WSL 2.

Se necesita:

- Python 3.
- Git.
- Los comandos `ps`, `who`, `df` e `ip`.
- Acceso al sistema de archivos virtual `/proc`.

Compruebe los requisitos antes de continuar:

```bash
python3 --version
git --version
command -v ps
command -v who
command -v df
command -v ip
test -r /proc/cpuinfo && echo "/proc disponible"
```

No se requiere `sudo` para instalar, ejecutar o probar el monitor.

## Clonar el proyecto

```bash
git clone <url-del-repositorio>
cd linux-resource-monitor
```

## Crear un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

La primera version usa la biblioteca estandar de Python. El archivo
`requirements.txt` se conserva para que el comando de instalacion sea estable
si el proyecto necesita una dependencia justificada en el futuro.

## Verificar la instalacion

Ejecute la suite completa:

```bash
python3 -m unittest discover -s tests
```

En Linux el resultado esperado es que todas las pruebas pasen. En Windows sin
WSL, las pruebas que dependen de `os.fork()` se omiten de forma explicita.

## Ejecutar desde Windows con WSL

Abra Ubuntu desde Windows Terminal, o ejecute desde PowerShell:

```powershell
wsl.exe -d Ubuntu --cd "<ruta-del-repositorio-en-wsl>" -- python3 -m unittest discover -s tests
```

En un repositorio ubicado en el disco C:, la ruta WSL normalmente comienza por
`/mnt/c/`.

## Base de datos

La base SQLite se crea automaticamente la primera vez que se inicia la
aplicacion, en:

```text
database/data/monitor.sqlite3
```

Ese archivo contiene el historial de capturas local y esta excluido de Git.
No copie una base de datos con datos de otro usuario al repositorio.
