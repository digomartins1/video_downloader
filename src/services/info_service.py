import yt_dlp
from typing import Dict, Any, Optional

class InfoService:
    @staticmethod
    def get_info(url: str) -> Optional[Dict[str, Any]]:
        """Extrai metadados do vídeo sem realizar download."""
        opts = {"quiet": True, "extract_flat": False}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return ydl.sanitize_info(info)
        except Exception as e:
            print(f"Erro ao extrair informações: {e}")
            return None