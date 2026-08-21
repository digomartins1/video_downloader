# ==============================================================================
# IMPORTAÇÃO DE MÓDULOS NATIVOS DO PYTHON (Sem necessidade de pip prévio)
# ==============================================================================
import os                  # Interage com o sistema operacional (caminhos, processos)
import sys                 # Fornece acesso a variáveis do interpretador (ex: sys.executable)
import shutil              # Operações de alto nível em arquivos e fluxos de dados
import zipfile             # Módulo para manipulação e extração de arquivos compactados .zip
import subprocess          # Permite executar comandos do sistema (como o pip e outros scripts)
import urllib.request      # Biblioteca para realizar requisições HTTP e downloads pela internet
from pathlib import Path   # Manipulação moderna e orientada a objetos de caminhos de arquivos


# ==============================================================================
# CONFIGURAÇÕES DO REPOSITÓRIO GITHUB E CAMINHOS LOCAIS
# ==============================================================================
GITHUB_USER = "digomartins1"       # Usuário proprietário do repositório no GitHub
GITHUB_REPO = "video_downloader"   # Nome exato do repositório
BRANCH = "main"                    # Nome da branch padrão de onde o código será baixado

# Lista de arquivos e extensões bloqueados que NÃO devem ser extraídos para a máquina
ARQUIVOS_BLOQUEADOS = ["install.ps1", ".ps1", ".bat", ".sh"]

# URL direta para download do código-fonte completo compactado em .zip pelo GitHub
REPO_ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"

# Diretório raiz onde este script (launcher.py) está sendo executado
APP_DIR = Path(__file__).resolve().parent

# Caminho completo para salvar o arquivo temporário baixado do GitHub
TEMP_ZIP = APP_DIR / "temp_repo.zip"

# Caminho para o arquivo de dependências (pip)
REQ_FILE = APP_DIR / "requirements.txt"

# Caminho para o arquivo principal de execução da aplicação
MAIN_FILE = APP_DIR / "main.py"


# ==============================================================================
# FUNÇÕES DO INICIALIZADOR (BOOTSTRAPPER)
# ==============================================================================

def print_status(msg: str):
    """
    Exibe uma mensagem formatada de status no terminal com um prefixo padrão.
    """
    print(f"\n[BOOTSTRAP] ➜ {msg}")


def limpar_arquivos_indesejados():
    """
    Verifica se o arquivo indesejado 'install.ps1' existe na pasta
    do projeto e o remove com segurança.
    """
    arquivo_ps1 = APP_DIR / "install.ps1"
    if arquivo_ps1.exists():
        try:
            # unlink() apaga o arquivo do disco
            arquivo_ps1.unlink()
        except Exception:
            # Ignora erros caso o arquivo esteja em uso ou com permissão restrita
            pass


def download_repo():
    """
    Faz o download do repositório completo em formato .zip diretamente do GitHub.
    """
    print_status(f"Baixando arquivos de {GITHUB_USER}/{GITHUB_REPO}...")
    
    # Cabeçalho User-Agent simulando um navegador para evitar bloqueios da API do GitHub
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(REPO_ZIP_URL, headers=headers)

    try:
        # Abre a conexão HTTP e grava os bytes baixados diretamente no arquivo temp_repo.zip
        with urllib.request.urlopen(req) as response, open(TEMP_ZIP, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print_status("Download dos arquivos concluído!")
    except Exception as e:
        # Se falhar (ex: sem internet ou repositório privado), exibe o erro e encerra
        print(f"\n[ERRO] Falha ao baixar arquivos do GitHub: {e}")
        sys.exit(1)


def extract_repo():
    """
    Descompacta o arquivo ZIP baixado, filtrando arquivos indesejados
    e mantendo a estrutura de pastas correta na raiz do projeto.
    """
    print_status("Extraindo módulos...")
    try:
        # Abre o arquivo ZIP em modo de leitura
        with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
            # O GitHub sempre empacota os arquivos dentro de uma pasta raiz: 'nome_repo-branch/'
            folder_inside_zip = f"{GITHUB_REPO}-{BRANCH}/"

            # Itera sobre cada arquivo/pasta dentro do ZIP
            for member in zip_ref.namelist():
                if member.startswith(folder_inside_zip):
                    # Filtro de segurança: se o arquivo for .ps1, .bat ou .sh, ele é ignorado
                    if any(member.endswith(bloqueado) for bloqueado in ARQUIVOS_BLOQUEADOS):
                        continue

                    # Remove o prefixo da pasta raiz do ZIP para extrair direto na pasta local
                    relative_path = member[len(folder_inside_zip):]
                    if not relative_path:
                        continue

                    target_path = APP_DIR / relative_path
                    
                    # Se for diretório, cria a pasta localmente
                    if member.endswith('/'):
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        # Garante que a pasta pai exista antes de extrair o arquivo
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        # Copia o conteúdo do membro do ZIP para o arquivo de destino
                        with zip_ref.open(member) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)

        # Apaga o arquivo temporário .zip após a extração bem-sucedida
        if TEMP_ZIP.exists():
            TEMP_ZIP.unlink()

        print_status("Estrutura do projeto pronta!")
    except Exception as e:
        print(f"\n[ERRO] Falha ao extrair arquivos: {e}")
        sys.exit(1)


def install_requirements():
    """
    Instala ou atualiza automaticamente as dependências listadas
    no requirements.txt de forma silenciosa via pip.
    """
    # Se o arquivo requirements.txt não existir, não há nada para instalar
    if not REQ_FILE.exists():
        return

    print_status("Verificando dependências...")
    try:
        # Executa: python -m pip install -r requirements.txt
        # O stdout=DEVNULL oculta os logs brutos para manter a tela limpa
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQ_FILE)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Falha ao instalar dependências: {e}")
        sys.exit(1)


def run_application():
    """
    Inicia o script principal (main.py) utilizando o mesmo interpretador Python.
    """
    if not MAIN_FILE.exists():
        print(f"\n[ERRO] {MAIN_FILE.name} não encontrado.")
        sys.exit(1)

    print_status("Iniciando a aplicação...")
    try:
        # Executa: python main.py
        subprocess.call([sys.executable, str(MAIN_FILE)])
    except KeyboardInterrupt:
        # Permite ao usuário cancelar a execução com Ctrl + C sem gerar logs de erro
        pass


# ==============================================================================
# FLUXO PRINCIPAL DE EXECUÇÃO
# ==============================================================================

def main():
    # 1. Limpa qualquer arquivo indesejado que tenha sobrado
    limpar_arquivos_indesejados()

    # 2. Se a pasta 'src' ou o 'main.py' ainda não existirem localmente, baixa e extrai
    if not (APP_DIR / "src").exists() or not MAIN_FILE.exists():
        download_repo()
        extract_repo()

    # 3. Garante que os pacotes necessários estão instalados
    install_requirements()
    
    # 4. Faz uma última checagem de limpeza antes de abrir o app
    limpar_arquivos_indesejados()
    
    # 5. Inicia o programa principal
    run_application()


# Ponto de entrada padrão: só executa a função main() se o script for chamado diretamente
if __name__ == "__main__":
    main()
