import yt_dlp
from typing import Callable, Optional
from src.config import DOWNLOAD_DIR

class DownloadService:
    def __init__(self, progress_hook: Optional[Callable] = None):
        self.progress_hook = progress_hook

    def download(self, url: str, format_choice: str = "best", is_audio_only: bool = False) -> bool:
        """Executa o download do vídeo ou extração de áudio em MP3."""
        ydl_opts = {
            "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }

        if self.progress_hook:
            ydl_opts["progress_hooks"] = [self.progress_hook]

        if is_audio_only:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            if format_choice == "best":
                ydl_opts["format"] = "bestvideo+bestaudio/best"
            else:
                ydl_opts["format"] = f"bestvideo[height<={format_choice}]+bestaudio/best[height<={format_choice}]/best"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"\nErro durante o download: {e}")
            return False
