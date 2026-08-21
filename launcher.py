import os
import sys
import shutil
import zipfile
import subprocess
import urllib.request
from pathlib import Path

# ==========================================
# CONFIGURAÇÕES DO REPOSITÓRIO GITHUB
# ==========================================
GITHUB_USER = "SEU_USUARIO_AQUI"
GITHUB_REPO = "Video-Downloader"
BRANCH = "main"

# Arquivos/extensões bloqueados que NÃO devem ser extraídos
ARQUIVOS_BLOQUEADOS = ["install.ps1", ".ps1", ".bat", ".sh"]

REPO_ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"
APP_DIR = Path(__file__).resolve().parent
TEMP_ZIP = APP_DIR / "temp_repo.zip"
REQ_FILE = APP_DIR / "requirements.txt"
MAIN_FILE = APP_DIR / "main.py"


def print_status(msg: str):
    print(f"\n[BOOTSTRAP] ➜ {msg}")


def limpar_arquivos_indesejados():
    """Remove qualquer install.ps1 que tenha ficado na pasta."""
    arquivo_ps1 = APP_DIR / "install.ps1"
    if arquivo_ps1.exists():
        try:
            arquivo_ps1.unlink()
        except Exception:
            pass


def download_repo():
    """Baixa o repositório em formato .zip."""
    print_status(f"Baixando arquivos de {GITHUB_USER}/{GITHUB_REPO}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(REPO_ZIP_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response, open(TEMP_ZIP, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print_status("Download dos arquivos concluído!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao baixar arquivos do GitHub: {e}")
        sys.exit(1)


def extract_repo():
    """Extrai apenas os arquivos necessários do projeto."""
    print_status("Extraindo módulos...")
    try:
        with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
            folder_inside_zip = f"{GITHUB_REPO}-{BRANCH}/"
            
            for member in zip_ref.namelist():
                if member.startswith(folder_inside_zip):
                    # Bloqueia o install.ps1 e scripts indesejados
                    if any(member.endswith(bloqueado) for bloqueado in ARQUIVOS_BLOQUEADOS):
                        continue

                    relative_path = member[len(folder_inside_zip):]
                    if not relative_path:
                        continue
                    
                    target_path = APP_DIR / relative_path
                    if member.endswith('/'):
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with zip_ref.open(member) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)

        # Apaga o .zip temporário
        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()
            
        print_status("Estrutura do projeto pronta!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao extrair arquivos: {e}")
        sys.exit(1)


def install_requirements():
    """Instala as dependências silenciosamente."""
    if not REQ_FILE.exists():
        return

    print_status("Verificando dependências...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Falha ao instalar dependências: {e}")
        sys.exit(1)


def run_application():
    """Executa a aplicação principal."""
    if not MAIN_FILE.exists():
        print(f"\n[ERRO] {MAIN_FILE.name} não encontrado.")
        sys.exit(1)

    print_status("Iniciando a aplicação...")
    try:
        subprocess.call([sys.executable, str(MAIN_FILE)])
    except KeyboardInterrupt:
        pass


def main():
    # 1. Garante a remoção de qualquer install.ps1 residual
    limpar_arquivos_indesejados()

    # 2. Baixa e extrai filtrando apenas o que é necessário
    if not (APP_DIR / "src").exists() or not MAIN_FILE.exists():
        download_repo()
        extract_repo()

    # 3. Instala pacotes e executa
    install_requirements()
    limpar_arquivos_indesejados()
    run_application()


if __name__ == "__main__":
    main()
