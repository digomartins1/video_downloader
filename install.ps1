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
        # Ordena numericamente e pega a última (mai
