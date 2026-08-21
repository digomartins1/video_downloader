# ============================================================
# BAIXA E EXECUTA AUTOMATICAMENTE O VIDEO DOWNLOADER
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Localiza ou instala o Python
$pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
if (-not $pythonCmd) { $pythonCmd = Get-Command "py" -ErrorAction SilentlyContinue }

if (-not $pythonCmd) {
    Write-Host "[+] Instalando Python automaticamente..." -ForegroundColor Cyan
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $pythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
}

# 2. Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 3. Baixa e descompacta o projeto do GitHub
Write-Host "[+] Baixando arquivos..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

# 4. Entra na pasta do projeto e instala dependências
Set-Location -Path "$appDir\video_downloader-main"

if (Test-Path "requirements.txt") {
    Write-Host "[+] Verificando pacotes..." -ForegroundColor Cyan
    & $pythonCmd.Source -m pip install -r requirements.txt --quiet --no-warn-script-location
}

# 5. EXECUTA O PROGRAMA NA HORA
Write-Host "[+] Abrindo o programa..." -ForegroundColor Green
Clear-Host
& $pythonCmd.Source "main.py"
