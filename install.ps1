# ============================================================
# VIDEO DOWNLOADER - INICIALIZADOR AUTOMÁTICO COM WINGET
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verifica se o Python REAL já está funcionando
$temPython = $false
try {
    $teste = (& python --version) 2>&1
    # Só considera instalado se responder com "Python 3.x.x"
    if ($LASTEXITCODE -eq 0 -and $teste -match "Python 3\.") {
        $temPython = $true
        Write-Host "[+] Python detectado: $teste" -ForegroundColor Green
    }
} catch {
    $temPython = $false
}

# 2. Se NÃO tiver Python, instala pelo Winget exatamente com o seu comando
if (-not $temPython) {
    Write-Host "[!] Python nao encontrado. Instalando via Winget..." -ForegroundColor Yellow
    
    # O SEU COMANDO DO WINGET
    winget install --id Python.Python.3 --silent --accept-source-agreements --accept-package-agreements
    
    # RECARREGA O PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    # Testa a versão novamente após instalar
    Write-Host "[+] Verificando instalacao..." -ForegroundColor Cyan
    python --version
}

# 3. Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 4. Baixa os arquivos do seu GitHub
Write-Host "[+] Baixando arquivos do projeto..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

# 5. Extrai os arquivos
Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

# 6. Entra na pasta do projeto
$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# 7. Instala as dependências do requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "[+] Verificando pacotes (pip)..." -ForegroundColor Cyan
    python -m pip install -r requirements.txt --quiet --no-warn-script-location
}

# 8. Executa o programa
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
python main.py
