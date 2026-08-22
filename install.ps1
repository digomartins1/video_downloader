Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Localiza ou instala o Python
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

if (-not $pyBase) {
    Write-Host "[+] Python não encontrado. Instalando automaticamente via Winget..." -ForegroundColor Cyan
    winget install -e --id Python.Python.3.12 --scope user --silent --accept-source-agreements --accept-package-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $pyBase = Obter-PythonBase
}

# 2. Prepara o diretório
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 3. Cria o ambiente virtual
$venvDir = "$appDir\venv"
$venvPython = "$venvDir\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    if (Test-Path $venvDir) {
        Remove-Item $venvDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[+] Configurando ambiente virtual..." -ForegroundColor Cyan
    & $pyBase -m venv "$venvDir" 2>$null
}

$execPython = if (Test-Path $venvPython) { $venvPython } else { $pyBase }

# 4. Baixa e extrai do GitHub
Write-Host "[+] Baixando projeto do GitHub..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# 5. Instala os requisitos
$reqFile = "$pastaProjeto\requirements.txt"
if (Test-Path $reqFile) {
    Write-Host "[+] Instalando dependências..." -ForegroundColor Cyan
    & $execPython -m pip install -r "$reqFile" --no-warn-script-location --quiet
}

# 6. Executa o programa
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
& $execPython "$pastaProjeto\main.py"
