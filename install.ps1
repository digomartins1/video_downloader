# ============================================================
# VIDEO DOWNLOADER - INICIALIZADOR AUTOMÁTICO
# ============================================================
Clear-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Video Downloader...          " -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verifica se já existe um Python funcional no computador
$pythonPronto = $false
try {
    $teste = & py --version 2>&1
    if ($LASTEXITCODE -eq 0 -and $teste -match "Python 3\.") {
        $pythonPronto = $true
        Write-Host "[+] Python detectado: $teste" -ForegroundColor Green
    }
} catch {
    $pythonPronto = $false
}

# 2. Se NÃO tiver Python, busca e instala a versão MAIS RECENTE via Winget
if (-not $pythonPronto) {
    Write-Host "[!] Python nao encontrado. Buscando versao mais recente no Winget..." -ForegroundColor Yellow

    # Procura todas as versões do Python 3 disponíveis no Winget e pega a mais nova
    $versoes = (winget search --id "Python.Python.3" --source winget | Select-String -Pattern 'Python\.Python\.3\.\d+' -AllMatches).Matches.Value | Select-Object -Unique
    
    if ($versoes) {
        # Ordena numericamente e pega a última (mais recente)
        $idMaisRecente = $versoes | Sort-Object { [version]($_ -replace 'Python\.Python\.', '') } | Select-Object -Last 1
    } else {
        $idMaisRecente = "Python.Python.3.12"  # Fallback de segurança
    }

    Write-Host "[+] Instalando [$idMaisRecente] via Winget..." -ForegroundColor Cyan
    winget install -e --id $idMaisRecente --scope user --accept-source-agreements --accept-package-agreements

    # Atualiza o PATH da sessão atual para o terminal reconhecer o Python agora
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 3. Prepara a pasta local
$appDir = "$env:LOCALAPPDATA\video_downloader"
$zipFile = "$appDir\repo.zip"

if (-not (Test-Path $appDir)) {
    New-Item -ItemType Directory -Path $appDir -Force | Out-Null
}

# 4. Baixa e descompacta os arquivos do GitHub
Write-Host "[+] Baixando arquivos do projeto..." -ForegroundColor Cyan
$zipUrl = "https://github.com/digomartins1/video_downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Expand-Archive -Path $zipFile -DestinationPath $appDir -Force
Remove-Item $zipFile -Force

# 5. Entra na pasta do projeto
$pastaProjeto = "$appDir\video_downloader-main"
Set-Location -Path $pastaProjeto

# 6. Instala dependências do requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "[+] Verificando pacotes (pip)..." -ForegroundColor Cyan
    py -m pip install -r requirements.txt --quiet --no-warn-script-location
}

# 7. Abre o programa
Write-Host "[+] Abrindo Video Downloader..." -ForegroundColor Green
Clear-Host
py main.py
