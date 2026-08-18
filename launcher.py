import os
import sys
import shutil
import zipfile
import subprocess
import urllib.request
from pathlib import Path

# ==========================================
# CONFIGURAÇÕES DO SEU REPOSITÓRIO GITHUB
# ==========================================
GITHUB_USER = "digomartins1"  # Ex: "joaosilva"
GITHUB_REPO = "video_downloader"  # Nome do repositório
BRANCH = "main"  # Branch padrão ("main" ou "master")

# URLs e Diretórios
REPO_ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"
APP_DIR = Path(__file__).resolve().parent
TEMP_ZIP = APP_DIR / "temp_repo.zip"
REQ_FILE = APP_DIR / "requirements.txt"
MAIN_FILE = APP_DIR / "main.py"


def print_status(msg: str):
    print(f"\n[BOOTSTRAP] ➜ {msg}")


def download_repo():
    """Baixa o repositório completo em formato .zip do GitHub."""
    print_status(f"Baixando código-fonte de {GITHUB_USER}/{GITHUB_REPO}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(REPO_ZIP_URL, headers=headers)

    try:
        with urllib.request.urlopen(req) as response, open(TEMP_ZIP, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print_status("Download dos arquivos concluído com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao baixar arquivos do GitHub: {e}")
        sys.exit(1)


def extract_repo():
    """Extrai os arquivos do repositório na pasta local."""
    print_status("Extraindo módulos...")
    try:
        with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
            # O GitHub empacota tudo dentro de uma pasta chamada 'repo-branch/'
            folder_inside_zip = f"{GITHUB_REPO}-{BRANCH}/"

            for member in zip_ref.namelist():
                if member.startswith(folder_inside_zip):
                    # Remove o prefixo da pasta raiz para extrair diretamente aqui
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

        # Remove o arquivo temporário .zip
        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()

        print_status("Estrutura do projeto pronta!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao extrair arquivos: {e}")
        sys.exit(1)


def install_requirements():
    """Instala as dependências listadas no requirements.txt automaticamente."""
    if not REQ_FILE.exists():
        print_status("Nenhum requirements.txt encontrado. Pulando instalação de pacotes.")
        return

    print_status("Verificando e instalando dependências necessárias (pip)...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)],
            stdout=subprocess.DEVNULL,  # Oculte ou remova se quiser ver o log detalhado do pip
            stderr=subprocess.STDOUT
        )
        print_status("Todas as dependências foram instaladas/atualizadas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Falha ao instalar dependências: {e}")
        sys.exit(1)


def run_application():
    """Inicia a aplicação principal."""
    if not MAIN_FILE.exists():
        print(f"\n[ERRO] Arquivo de inicialização ({MAIN_FILE.name}) não encontrado.")
        sys.exit(1)

    print_status("Iniciando a aplicação...\n" + "=" * 50 + "\n")
    try:
        # Executa o main.py usando o mesmo interpretador Python
        subprocess.call([sys.executable, str(MAIN_FILE)])
    except KeyboardInterrupt:
        pass


def main():
    print("=" * 50)
    print(f" Inicializador Automático: {GITHUB_REPO}")
    print("=" * 50)

    # 1. Se os módulos ainda não existem, baixa e extrai
    if not (APP_DIR / "src").exists() or not MAIN_FILE.exists():
        download_repo()
        extract_repo()

    # 2. Instala/Atualiza pacotes (yt-dlp, rich, etc.)
    install_requirements()

    # 3. Executa o programa
    run_application()


if __name__ == "__main__":
    main()