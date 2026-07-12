param(
    [string]$Salida = "docs/evidencias/arquitectura_actual.png"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$width = 1800
$height = 1220
$bitmap = New-Object System.Drawing.Bitmap($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$graphics.Clear([System.Drawing.Color]::FromArgb(247, 249, 252))

$fontTitle = New-Object System.Drawing.Font("Segoe UI", 28, [System.Drawing.FontStyle]::Bold)
$fontLane = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$fontBox = New-Object System.Drawing.Font("Segoe UI", 15, [System.Drawing.FontStyle]::Bold)
$fontSmall = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Regular)
$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70, 79, 91), 3)
$pen.DashStyle = [System.Drawing.Drawing2D.DashStyle]::Solid
$brushText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(28, 34, 43))
$brushMuted = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(80, 91, 105))
$format = New-Object System.Drawing.StringFormat
$format.Alignment = [System.Drawing.StringAlignment]::Center
$format.LineAlignment = [System.Drawing.StringAlignment]::Center

function Draw-RoundedBox {
    param(
        [int]$X, [int]$Y, [int]$W, [int]$H,
        [string]$Text, [System.Drawing.Color]$Fill,
        [System.Drawing.Font]$Font = $fontBox
    )
    $rect = New-Object System.Drawing.Rectangle($X, $Y, $W, $H)
    $brush = New-Object System.Drawing.SolidBrush($Fill)
    $border = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(72, 84, 98), 2)
    $graphics.FillRectangle($brush, $rect)
    $graphics.DrawRectangle($border, $rect)
    $textRect = New-Object System.Drawing.RectangleF([single]$X, [single]$Y, [single]$W, [single]$H)
    $graphics.DrawString($Text, $Font, $brushText, $textRect, $format)
    $brush.Dispose()
    $border.Dispose()
}

function Draw-Arrow {
    param([int]$X1, [int]$Y1, [int]$X2, [int]$Y2)
    $arrowPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70, 79, 91), 3)
    $cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 7, $true)
    $arrowPen.CustomEndCap = $cap
    $graphics.DrawLine($arrowPen, $X1, $Y1, $X2, $Y2)
    $cap.Dispose()
    $arrowPen.Dispose()
}

function Draw-Lane {
    param([int]$X, [string]$Title, [System.Drawing.Color]$Fill)
    $laneRect = New-Object System.Drawing.Rectangle($X, 390, 520, 720)
    $laneBrush = New-Object System.Drawing.SolidBrush($Fill)
    $lanePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(187, 196, 207), 2)
    $graphics.FillRectangle($laneBrush, $laneRect)
    $graphics.DrawRectangle($lanePen, $laneRect)
    $titleRect = New-Object System.Drawing.RectangleF([single]$X, [single]405, [single]520, [single]42)
    $graphics.DrawString($Title, $fontLane, $brushText, $titleRect, $format)
    $laneBrush.Dispose()
    $lanePen.Dispose()
}

$mainTitleRect = New-Object System.Drawing.RectangleF([single]0, [single]25, [single]$width, [single]55)
$graphics.DrawString("Linux Resource Monitor - Arquitectura MVC", $fontTitle, $brushText, $mainTitleRect, $format)
Draw-RoundedBox 730 95 340 65 "Usuario" ([System.Drawing.Color]::FromArgb(255, 255, 255))
Draw-Arrow 900 160 900 195
Draw-RoundedBox 730 195 340 65 "main.py" ([System.Drawing.Color]::FromArgb(223, 232, 246))
Draw-Arrow 900 260 900 295
Draw-RoundedBox 610 295 580 70 "Vista de consola y menus" ([System.Drawing.Color]::FromArgb(212, 229, 247))

Draw-Lane 80 "MONITOREO EN VIVO" ([System.Drawing.Color]::FromArgb(235, 245, 239))
Draw-Lane 640 "PERSISTENCIA CRUD" ([System.Drawing.Color]::FromArgb(248, 242, 228))
Draw-Lane 1200 "CONCURRENCIA" ([System.Drawing.Color]::FromArgb(241, 237, 249))

Draw-Arrow 730 365 340 470
Draw-Arrow 900 365 900 470
Draw-Arrow 1070 365 1460 470

Draw-RoundedBox 145 470 390 65 "MonitorController" ([System.Drawing.Color]::FromArgb(194, 228, 204))
Draw-Arrow 340 535 340 575
Draw-RoundedBox 115 575 450 170 "Modelos de recursos`n`nCPU | Memoria | Procesos`nDisco | Red | Usuarios" ([System.Drawing.Color]::FromArgb(218, 239, 224)) $fontBox
Draw-Arrow 260 745 260 800
Draw-Arrow 420 745 420 800
Draw-RoundedBox 115 800 290 65 "/proc" ([System.Drawing.Color]::FromArgb(255, 255, 255))
Draw-RoundedBox 415 800 150 65 "Comandos`nLinux" ([System.Drawing.Color]::FromArgb(255, 255, 255)) $fontSmall

Draw-RoundedBox 705 470 390 65 "CrudController" ([System.Drawing.Color]::FromArgb(240, 215, 164))
Draw-Arrow 900 535 900 600
Draw-RoundedBox 705 600 390 65 "RepositorioCapturas" ([System.Drawing.Color]::FromArgb(249, 227, 184))
Draw-Arrow 900 665 900 730
Draw-RoundedBox 705 730 390 80 "SQLite" ([System.Drawing.Color]::FromArgb(255, 255, 255))
Draw-Arrow 900 810 900 875
Draw-RoundedBox 705 875 390 90 "Captura completa`nen una transaccion" ([System.Drawing.Color]::FromArgb(255, 255, 255)) $fontSmall

Draw-RoundedBox 1265 470 390 65 "ConcurrenciaController" ([System.Drawing.Color]::FromArgb(219, 207, 239))
Draw-Arrow 1460 535 1460 590
Draw-RoundedBox 1265 590 390 65 "threading.Thread" ([System.Drawing.Color]::FromArgb(234, 226, 247))
Draw-Arrow 1460 655 1460 710
Draw-RoundedBox 1265 710 390 65 "Todos los hilos finalizan" ([System.Drawing.Color]::FromArgb(255, 255, 255)) $fontSmall
Draw-Arrow 1460 775 1460 830
Draw-RoundedBox 1265 830 390 65 "os.fork()" ([System.Drawing.Color]::FromArgb(234, 226, 247))
Draw-Arrow 1460 895 1460 950
Draw-RoundedBox 1265 950 390 65 "Pipe + waitpid()" ([System.Drawing.Color]::FromArgb(255, 255, 255)) $fontSmall

$noteRect = New-Object System.Drawing.RectangleF([single]120, [single]1140, [single]1560, [single]45)
$graphics.DrawString("La Vista recibe datos de los Controladores. Solo el Repositorio accede a SQLite. fork() se ejecuta despues de finalizar los hilos.", $fontSmall, $brushMuted, $noteRect, $format)

$directory = Split-Path -Parent $Salida
if ($directory) {
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
}
$bitmap.Save((Join-Path (Get-Location) $Salida), [System.Drawing.Imaging.ImageFormat]::Png)

$format.Dispose()
$brushText.Dispose()
$brushMuted.Dispose()
$pen.Dispose()
$fontTitle.Dispose()
$fontLane.Dispose()
$fontBox.Dispose()
$fontSmall.Dispose()
$graphics.Dispose()
$bitmap.Dispose()
