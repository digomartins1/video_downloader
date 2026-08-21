# ============================================================
# BAIXA E EXECUTA AUTOMATICAMENTE O VIDEO DOWNLOADER
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# Função para encontrar o Python REAL (ignora o atalho da Microsoft Store)
function Encontrar-PythonReal {
    # 1. Procura nos caminhos de instalação padrão
    $locais = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "C:\Program Files\Python*\python.exe",
        "C:\Python*\python.exe"
    )
    foreach ($local in $locais) {
        $exe = Get-Item $local -ErrorAction SilentlyContinue | Select-Object -Last 1
        if ($exe -and (Test-Path $exe.FullName)) {
            return $exe.FullName
        }
    }

    # 2. Tenta o inicializador oficial 'py'
    try {
        $testePy = & py -c "import sys; print(sys.executable)" 2>$null
        if ($testePy) { return "py" }
    } catch {}

    # 3. Testa o comando 'python' se NÃO for da pasta WindowsApps
    $cmd = Get-Command "python" -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") {
        return $cmd.Source
    }

    return $null
}

$pythonReal = Encontrar-PythonReal

# Se não encontrou o Python de verdade, instala via Winget
if (-not $pythonReal) {
    Write-Host "[!] Python real não encontrado no sistema." -ForegroundColor Yellow
    Write-Host "[+] Instalando Python 3.12 automaticamente via Winget..." -ForegroundColor Cyan
    
    winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    
    # Recarrega o PATH do sistema
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    $pythonReal = Encontrar-PythonReal
    
    if (-not $pythonReal) {
        Write-Host "[ERRO] Não foi possível localizar o Python após a instalação." -ForegroundColor Red
        Write-Host "Por favor, reinicie o PowerShell e tente novamente." -ForegroundColor Yellow
        return
    }
}

Write-Host "[+] Python pronto: $pythonReal" -ForegroundColor Green

# Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# Baixa e extrai os arquivos do GitHub
Write-Host "[+] Baixando arquivos..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

# Entra na pasta do projeto
Set-Location -Path "$appDir\video_downloader-main"

# Instala/Verifica bibliotecas necessárias
if (Test-Path "requirements.txt") {
    Write-Host "[+] Verificando pacotes no requirements.txt..." -ForegroundColor Cyan
    & $pythonReal -m pip install -r requirements.txt --quiet --no-warn-script-location
}

# Inicia a aplicação
Write-Host "[+] Abrindo o programa..." -ForegroundColor Green
Clear-Host
& $pythonReal "main.py"
