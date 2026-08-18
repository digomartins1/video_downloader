from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretório padrão de downloads
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Configurações padrão do yt-dlp
DEFAULT_YT_DLP_OPTS = {
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    "quiet": True,
    "no_warnings": True,
}