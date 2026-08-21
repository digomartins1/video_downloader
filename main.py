import os
import sys
import subprocess

# 1. Instalação silenciosa do static-ffmpeg se necessário
try:
    import static_ffmpeg
except ModuleNotFoundError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "static-ffmpeg"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    import static_ffmpeg

# 2. Configura o FFmpeg em segundo plano (sem poluir o terminal)
try:
    with open(os.devnull, 'w') as fnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = fnull
        sys.stderr = fnull
        try:
            static_ffmpeg.add_paths()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
except Exception:
    static_ffmpeg.add_paths()

from src.cli.interface import CLIInterface

def main():
    # 3. Limpa a tela do terminal antes de mostrar o programa
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        app = CLIInterface()
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()
