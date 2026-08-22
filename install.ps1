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
    $candidatos = @(
        "python",
        "py",
        "python3",
        "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "C:\Program Files\Python314\python.exe",
        "C:\Program Files\Python313\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python310\python.exe"
    )

    foreach ($cand in $candidatos) {
        try {
            $teste = & $cand --version 2>$null
            if ($LASTEXITCODE -eq 0 -or $teste) {
                return $cand
            }
        } catch {}
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
# 3. CRIA O AMBIENTE VIRTUAL ISOLADO (.VENV) COM RECUPERAÇÃO
# ------------------------------------------------------------
$venvDir = "$appDir\venv"
$venvPython = "$venvDir\Scripts\python.exe"

# Se o executável não existir, limpa a pasta corrompida e tenta recriar
if (-not (Test-Path $venvPython)) {
    if (Test-Path $venvDir) {
        Remove-Item $venvDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[+] Configurando ambiente virtual isolado..." -ForegroundColor Cyan
    & $pyBase -m venv "$venvDir" 2>$null
}

# Define o interpretador final (usa o venv se existir, ou o Python base como fallback)
$execPython = if (Test-Path $venvPython) { $venvPython } else { $pyBase }

# ------------------------------------------------------------
# 4. BAIXA E EXTRAI O CÓDIGO-FONTE DO GITHUB
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
    Write-Host "[+] Verificando dependências..." -ForegroundColor Cyan
    & $execPython -m pip install -r "$reqFile" --no-warn-script-location --quiet
}

# ------------------------------------------------------------
# 6. EXECUTA A APLICAÇÃO
# ------------------------------------------------------------
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
& $execPython "$pastaProjeto\main.py"
