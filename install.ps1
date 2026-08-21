# ============================================================
# VIDEO DOWNLOADER - 100% AUTOMÁTICO COM VENV ISOLADO
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Localiza o Python base do sistema
function Obter-PythonBase {
    $locais = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python313\python.exe",
        "C:\Program Files\Python*\python.exe",
        "C:\Python*\python.exe"
    )
    foreach ($local in $locais) {
        $exe = Get-Item $local -ErrorAction SilentlyContinue | Select-Object -Last 1
        if ($exe -and (Test-Path $exe.FullName)) {
            return $exe.FullName
        }
    }

    $py = Get-Command "py" -ErrorAction SilentlyContinue
    if ($py) { return "py" }

    return $null
}

$pyBase = Obter-PythonBase

# Se não tiver Python, instala via Winget
if (-not $pyBase) {
    Write-Host "[+] Instalando Python automaticamente via Winget..." -ForegroundColor Cyan
    winget install -e --id Python.Python.3.12 --scope user --silent --accept-source-agreements --accept-package-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $pyBase = Obter-PythonBase
}

# 2. Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 3. Cria o Ambiente Virtual isolado (venv) se ainda não existir
$venvDir = "$appDir\venv"
$venvPython = "$venvDir\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[+] Configurando ambiente isolado do projeto..." -ForegroundColor Cyan
    & $pyBase -m venv "$venvDir"
}

# 4. Baixa e descompacta os arquivos do GitHub
Write-Host "[+] Baixando projeto do GitHub..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# 5. Instala os pacotes DIRETAMENTE dentro do ambiente isolado
Write-Host "[+] Instalando dependencias (rich e yt-dlp)..." -ForegroundColor Cyan
& "$venvPython" -m pip install rich yt-dlp --no-warn-script-location

# 6. Executa o programa usando o Python do ambiente isolado
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
& "$venvPython" "$pastaProjeto\main.py"
