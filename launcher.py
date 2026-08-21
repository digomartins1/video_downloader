# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NATIVOS DO PYTHON (Sem necessidade de pip prévio)
# ==============================================================================
import os                  # Operações no sistema operacional
import sys                 # Variáveis e funções do interpretador Python
import shutil              # Manipulação de arquivos e streams de dados
import zipfile             # Extração e leitura de arquivos compactados (.zip)
import subprocess          # Execução de comandos do sistema em segundo plano
import urllib.request      # Realização de requisições HTTP para download via internet
from pathlib import Path   # Manipulação orientada a objetos de caminhos de arquivos


# ==============================================================================
# CONFIGURAÇÕES DO REPOSITÓRIO GITHUB E CAMINHOS
# ==============================================================================
GITHUB_USER = "digomartins1"       # Nome de usuário no GitHub
GITHUB_REPO = "video_downloader"   # Nome do repositório
BRANCH = "main"                    # Branch principal do projeto

# Lista de extensões e arquivos que NUNCA devem ser extraídos para a máquina
ARQUIVOS_BLOQUEADOS = ["install.ps1", ".ps1", ".bat", ".sh"]

# URL direta para baixar o arquivo .zip gerado automaticamente pelo GitHub
REPO_ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"

# Diretório base onde o launcher está rodando
APP_DIR = Path(__file__).resolve().parent

# Caminho do próprio arquivo launcher.py para permitir autoexclusão
LAUNCHER_FILE = Path(__file__).resolve()

# Arquivo temporário onde o ZIP será salvo
TEMP_ZIP = APP_DIR / "temp_repo.zip"

# Arquivo de dependências a ser lido pelo pip
REQ_FILE = APP_DIR / "requirements.txt"

# Arquivo principal que inicializa o programa após a extração
MAIN_FILE = APP_DIR / "main.py"


# ==============================================================================
# FUNÇÕES DO LAUNCHER
# ==============================================================================

def print_status(msg: str):
    """Exibe mensagens de progresso no terminal com um prefixo padrão."""
    print(f"\n[BOOTSTRAP] ➜ {msg}")


def limpar_arquivos_indesejados():
    """Remove scripts temporários ou indesejados caso existam na pasta."""
    arquivo_ps1 = APP_DIR / "install.ps1"
    if arquivo_ps1.exists():
        try:
            arquivo_ps1.unlink()
        except Exception:
            pass


def auto_destruir_launcher():
    """Exclui o arquivo launcher.py do disco após concluir toda a preparação."""
    try:
        if LAUNCHER_FILE.exists():
            LAUNCHER_FILE.unlink()
    except Exception:
        pass


def download_repo():
    """Faz o download do código-fonte completo do GitHub em formato .zip."""
    print_status(f"Baixando arquivos de {GITHUB_USER}/{GITHUB_REPO}...")
    
    # Cabeçalho User-Agent simulando um navegador para evitar bloqueios do GitHub
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
    """Extrai os arquivos do ZIP criando a árvore de módulos no diretório local."""
    print_status("Extraindo módulos...")
    try:
        with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
            folder_inside_zip = f"{GITHUB_REPO}-{BRANCH}/"

            for member in zip_ref.namelist():
                if member.startswith(folder_inside_zip):
                    # Bloqueia scripts indesejados
                    if any(member.endswith(bloqueado) for bloqueado in ARQUIVOS_BLOQUEADOS):
                        continue

                    # Evita recriar o launcher.py durante a extração
                    if member.endswith("launcher.py"):
                        continue

                    # Remove o prefixo da pasta raiz do zip
                    relative_path = member[len(folder_inside_zip):]
                    if not relative_path:
                        continue

                    target_path = APP_DIR / relative_path
                    
                    # Cria diretórios ou grava arquivos
                    if member.endswith('/'):
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with zip_ref.open(member) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)

        # Deleta o arquivo ZIP temporário
        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()

        print_status("Estrutura do projeto pronta!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao extrair arquivos: {e}")
        sys.exit(1)


def install_requirements():
    """Instala silenciosamente todas as dependências do requirements.txt via pip."""
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
    """Executa o script principal do programa (main.py)."""
    if not MAIN_FILE.exists():
        print(f"\n[ERRO] {MAIN_FILE.name} não encontrado.")
        sys.exit(1)

    print_status("Iniciando a aplicação...")
    try:
        subprocess.call([sys.executable, str(MAIN_FILE)])
    except KeyboardInterrupt:
        pass


def main():
    # 1. Limpa resíduos antes de começar
    limpar_arquivos_indesejados()

    # 2. Baixa o projeto caso ainda não exista localmente
    if not (APP_DIR / "src").exists() or not MAIN_FILE.exists():
        download_repo()
        extract_repo()

    # 3. Garante que as dependências estejam instaladas
    install_requirements()
    limpar_arquivos_indesejados()

    # 4. Apaga o launcher.py da máquina
    auto_destruir_launcher()

    # 5. Executa o programa principal
    run_application()


if __name__ == "__main__":
    main()
