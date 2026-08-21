import subprocess
import sys

# Se o static_ffmpeg não estiver instalado, ele instala sozinho agora mesmo
try:
    import static_ffmpeg
except ModuleNotFoundError:
    print("[SETUP] Configurando suporte ao FFmpeg automaticamente...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "static-ffmpeg"])
    import static_ffmpeg

# Baixa e adiciona o FFmpeg e FFprobe ao sistema automaticamente
static_ffmpeg.add_paths()

from src.cli.interface import CLIInterface

def main():
    try:
        app = CLIInterface()
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()
