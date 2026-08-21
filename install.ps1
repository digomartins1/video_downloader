# ============================================================
# VIDEO DOWNLOADER - INICIALIZADOR AUTOMÁTICO (PYTHON PURO)
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Função que acha o executável REAL do Python sem passar pela Microsoft Store
function Obter-CaminhoPython {
    $caminhos = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python*\python.exe",
        "C:\Python*\python.exe"
    )

    foreach ($c in $caminhos) {
        $arquivo = Get-Item $c -ErrorAction SilentlyContinue | Select-Object -Last 1
        if ($arquivo -and (Test-Path $arquivo.FullName)) {
            return $arquivo.FullName
        }
    }
    return $null
}

$pyExe = Obter-CaminhoPython

# 2. Se o Python não estiver instalado, baixa o oficial e instala direto
if (-not $pyExe) {
    Write-Host "[!] Python nao encontrado. Baixando instalador oficial do python.org..." -ForegroundColor Yellow
    
    $installerPath = "$env:TEMP\python_setup.exe"
    $pythonUrl = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
    
    Write-Host "[+] Instalando Python em segundo plano (aguarde cerca de 30s)..." -ForegroundColor Cyan
    Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_pip=1" -Wait
    Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
    
    # Busca novamente o caminho do Python recém-instalado
    $pyExe = Obter-CaminhoPython
}

if (-not $pyExe) {
    Write-Host "[ERRO] Nao foi possivel iniciar o Python automaticamente." -ForegroundColor Red
    return
}

Write-Host "[+] Python carregado: $pyExe" -ForegroundColor Green

# 3. Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 4. Baixa o código .py do seu GitHub
Write-Host "[+] Baixando arquivos do GitHub..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

# 5. Extrai os arquivos
Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

# 6. Entra na pasta do projeto
$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# 7. Instala as dependências necessárias do requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "[+] Verificando pacotes (pip)..." -ForegroundColor Cyan
    & "$pyExe" -m pip install -r requirements.txt --quiet --no-warn-script-location
}

# 8. Executa o main.py
Write-Host "[+] Abrindo o programa..." -ForegroundColor Green
Clear-Host
& "$pyExe" "$pastaProjeto\main.py"
