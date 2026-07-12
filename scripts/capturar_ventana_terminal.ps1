param(
    [string]$Titulo,

    [int]$ProcessId,

    [Parameter(Mandatory = $true)]
    [string]$Salida
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class WindowCapture {
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
}
"@

if (-not $Titulo -and $ProcessId -le 0) {
    throw "Indique -Titulo o -ProcessId para identificar una unica ventana de Windows Terminal."
}

if ($ProcessId -gt 0) {
    $candidatas = @(Get-Process -Id $ProcessId -ErrorAction Stop | Where-Object {
        $_.ProcessName -eq "WindowsTerminal" -and $_.MainWindowHandle -ne 0
    })
} else {
    $candidatas = @(Get-Process | Where-Object {
        $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -eq $Titulo
    })
}

if ($candidatas.Count -ne 1) {
    $identificador = if ($ProcessId -gt 0) { "PID $ProcessId" } else { "titulo '$Titulo'" }
    throw "Se esperaba exactamente una ventana con $identificador; se encontraron $($candidatas.Count). Abra una terminal dedicada o use Win+Shift+S seleccionando solo la terminal."
}

$rect = New-Object WindowCapture+RECT
if (-not [WindowCapture]::GetWindowRect($candidatas[0].MainWindowHandle, [ref]$rect)) {
    throw "No se pudo obtener el rectangulo de la ventana de terminal."
}

$ancho = $rect.Right - $rect.Left
$alto = $rect.Bottom - $rect.Top
if ($ancho -le 0 -or $alto -le 0) {
    throw "La ventana de terminal no tiene dimensiones validas para capturar."
}

# Excluye la sombra y las esquinas transparentes del marco de Windows Terminal.
$margenIzquierdo = 32
$margenSuperior = 48
$margenDerecho = 32
$margenInferior = 32
$ancho -= $margenIzquierdo + $margenDerecho
$alto -= $margenSuperior + $margenInferior
if ($ancho -le 0 -or $alto -le 0) {
    throw "La ventana de terminal es demasiado pequena para recortarla."
}

$directorio = Split-Path -Parent $Salida
if ($directorio) {
    New-Item -ItemType Directory -Force -Path $directorio | Out-Null
}

$imagen = New-Object System.Drawing.Bitmap($ancho, $alto)
$graficos = [System.Drawing.Graphics]::FromImage($imagen)
try {
    $graficos.CopyFromScreen($rect.Left + $margenIzquierdo, $rect.Top + $margenSuperior, 0, 0, $imagen.Size)
    $imagen.Save((Resolve-Path -LiteralPath $directorio).Path + "\" + (Split-Path -Leaf $Salida), [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graficos.Dispose()
    $imagen.Dispose()
}

Write-Output "Captura guardada en $Salida"
