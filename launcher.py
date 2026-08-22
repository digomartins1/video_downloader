import os
import sys
import shutil
import zipfile
import subprocess
import urllib.request
from pathlib import Path

# ==========================================
# CONFIGURAÇÕES DO GITHUB
# ==========================================
GITHUB_USER = "digomartins1"
GITHUB_REPO = "video_downloader"
BRANCH = "main"

REPO_ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"
APP_DIR = Path(__file__).resolve().parent
TEMP_ZIP = APP_DIR / "temp_repo.zip"
REQ_FILE = APP_DIR / "requirements.txt"
MAIN_FILE = APP_DIR / "main.py"

ARQUIVOS_BLOQUEADOS = ["install.ps1", ".ps1", ".bat", ".sh"]


def print_status(msg: str):
    print(f"\n[INSTALADOR] ➜ {msg}")


def obter_python_do_sistema() -> str:
    """Encontra o executável real do Python instalado na máquina."""
    candidatos = [
        "python",
        "py",
        "python3",
        str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Python/Python312/python.exe"),
        str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Python/Python311/python.exe"),
        "C:/Program Files/Python312/python.exe",
        "C:/Program Files/Python311/python.exe",
    ]
    for cand in candidatos:
        try:
            res = subprocess.run([cand, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                return cand
        except Exception:
            continue
    return "python"


def download_repo():
    """Baixa os arquivos do GitHub."""
    print_status(f"Baixando arquivos mais recentes de {GITHUB_REPO}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(REPO_ZIP_URL, headers=headers)
    try:
        with urllib.request.urlopen(req) as response, open(TEMP_ZIP, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print_status("Download concluído!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao baixar arquivos: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)


def extract_repo():
    """Extrai os módulos do ZIP."""
    print_status("Extraindo projeto...")
    try:
        with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
            folder_inside_zip = f"{GITHUB_REPO}-{BRANCH}/"

            for member in zip_ref.namelist():
                if member.startswith(folder_inside_zip):
                    if any(member.endswith(bloq) for bloq in ARQUIVOS_BLOQUEADOS):
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

        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()
        print_status("Arquivos extraídos com sucesso!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao extrair arquivos: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)


def install_requirements(py_cmd: str):
    """Instala as bibliotecas usando o Python real da máquina."""
    if not REQ_FILE.exists():
        return

    print_status("Verificando e instalando pacotes necessários...")
    try:
        subprocess.check_call(
            [py_cmd, "-m", "pip", "install", "-r", str(REQ_FILE)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print_status("Tudo configurado com sucesso!")
    except Exception as e:
        print(f"\n[AVISO] Não foi possível atualizar os pacotes: {e}")


def run_application(py_cmd: str):
    """Abre o programa principal."""
    if not MAIN_FILE.exists():
        print(f"\n[ERRO] Arquivo principal não encontrado.")
        input("\nPressione Enter para sair...")
        sys.exit(1)

    print_status("Abrindo o Video Downloader...")
    try:
        subprocess.Popen([py_cmd, str(MAIN_FILE)])
    except Exception as e:
        print(f"\n[ERRO] Falha ao abrir o programa: {e}")
        input("\nPressione Enter para sair...")


def main():
    print("=" * 45)
    print("   INSTALADOR AUTOMÁTICO - VIDEO DOWNLOADER   ")
    print("=" * 45)

    py_cmd = obter_python_do_sistema()

    # 1. Se os arquivos não existem na pasta, baixa e extrai
    if not (APP_DIR / "src").exists() or not MAIN_FILE.exists():
        download_repo()
        extract_repo()

    # 2. Instala os pacotes
    install_requirements(py_cmd)

    # 3. Executa o Video Downloader
    run_application(py_cmd)


if __name__ == "__main__":
    main()
