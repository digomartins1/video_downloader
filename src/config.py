from pathlib import Path

# ==========================================
# VERSÃO E REPOSITÓRIO DO PROGRAMA
# ==========================================
CURRENT_VERSION = "1.1.0"
GITHUB_REPO = "digomartins1/video_downloader"

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Opções padrão do yt-dlp
DEFAULT_YT_DLP_OPTS = {
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    "quiet": True,
    "no_warnings": True,
}
