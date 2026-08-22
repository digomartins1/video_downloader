import os
import sys

# 1. Se estiver rodando como código aberto (.py), instala os pacotes se faltarem
if not getattr(sys, 'frozen', False):
    import subprocess
    for package in ["static-ffmpeg", "customtkinter", "yt-dlp", "rich"]:
        try:
            __import__(package.replace("-", "_"))
        except ModuleNotFoundError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

# 2. Configura o FFmpeg em segundo plano
try:
    import static_ffmpeg
    with open(os.devnull, 'w') as fnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = fnull, fnull
        try:
            static_ffmpeg.add_paths()
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
except Exception:
    pass

# 3. Importa e inicializa a Interface Gráfica
from src.gui.interface import VideoDownloaderGUI

def main():
    app = VideoDownloaderGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
