# ============================================================
# VIDEO DOWNLOADER - INSTALADOR 100% AUTOMÁTICO PARA WINDOWS
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# ------------------------------------------------------------
# 1. LOCALIZA OU INSTALA O PYTHON BASE NO WINDOWS
# ------------------------------------------------------------
function Obter-PythonBase {
    # 1.1 Verifica se o comando 'python' ou 'py' já responde no terminal
    $cmdPy = Get-Command "python" -ErrorAction SilentlyContinue
    if ($cmdPy) { return $cmdPy.Source }

    $cmdLauncher = Get-Command "py" -ErrorAction SilentlyContinue
    if ($cmdLauncher) { return "py" }

    # 1.2 Procura nos diretórios padrão de instalação do Windows
    $locais = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
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

    return $null
}

$pyBase = Obter-PythonBase

# Se não tiver Python no computador, instala automaticamente via Winget
if (-not $pyBase) {
    Write-Host "[+] Python não encontrado. Instalando automaticamente via Winget..." -ForegroundColor Cyan
    winget install -e --id Python.Python.3.12 --scope user --silent --accept-source-agreements --accept-package-agreements
    
    # Atualiza as variáveis de ambiente do PowerShell
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $pyBase = Obter-PythonBase
}

# ------------------------------------------------------------
# 2. PREPARA A PASTA LOCAL NO APPDATA
# ------------------------------------------------------------
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# ------------------------------------------------------------
# 3. CRIA O AMBIENTE VIRTUAL ISOLADO (.VENV)
# ------------------------------------------------------------
$venvDir = "$appDir\venv"
$venvPython = "$venvDir\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[+] Criando ambiente virtual isolado (.venv)..." -ForegroundColor Cyan
    & $pyBase -m venv "$venvDir"
}

# ------------------------------------------------------------
# 4. BAIXA E EXTRAI O CÓDIGO-FONTE ATUALIZADO DO GITHUB
# ------------------------------------------------------------
Write-Host "[+] Baixando projeto do GitHub..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# ------------------------------------------------------------
# 5. INSTALA TODAS AS DEPENDÊNCIAS (yt-dlp, rich e static-ffmpeg)
# ------------------------------------------------------------
$reqFile = "$pastaProjeto\requirements.txt"
if (Test-Path $reqFile) {
    Write-Host "[+] Instalando dependências (yt-dlp, rich e static-ffmpeg)..." -ForegroundColor Cyan
    & "$venvPython" -m pip install -r "$reqFile" --no-warn-script-location --quiet
}

# ------------------------------------------------------------
# 6. EXECUTA A APLICAÇÃO
# ------------------------------------------------------------
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
& "$venvPython" "$pastaProjeto\main.py"
