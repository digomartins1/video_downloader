import os
import sys
import json
import urllib.request
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from src.config import CURRENT_VERSION, GITHUB_REPO

class UpdateService:
    API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

    @classmethod
    def check_for_update(cls) -> Optional[Tuple[str, str, str]]:
        """
        Verifica se há uma versão mais recente no GitHub Releases.
        Retorna (nova_versao, url_download_exe, notas_da_versao) se houver update.
        """
        try:
            req = urllib.request.Request(cls.API_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    return None
                data = json.loads(response.read().decode())

            tag_name = data.get("tag_name", "").replace("v", "").strip()
            if not tag_name:
                return None

            if cls._is_newer_version(tag_name, CURRENT_VERSION):
                download_url = None
                for asset in data.get("assets", []):
                    if asset.get("name", "").endswith(".exe"):
                        download_url = asset.get("browser_download_url")
                        break
                
                if download_url:
                    body = data.get("body", "Melhorias gerais e correções de bugs.")
                    return tag_name, download_url, body

        except Exception:
            pass
        return None

    @staticmethod
    def _is_newer_version(remote_ver: str, local_ver: str) -> bool:
        """Compara números de versão semântica (ex: 1.1.0 vs 1.0.0)."""
        try:
            r_parts = [int(p) for p in remote_ver.split(".")]
            l_parts = [int(p) for p in local_ver.split(".")]
            return r_parts > l_parts
        except Exception:
            return remote_ver != local_ver

    @classmethod
    def apply_update(cls, download_url: str, progress_callback=None) -> bool:
        """Baixa o novo .exe e substitui o arquivo com segurança em segundo plano."""
        try:
            if not getattr(sys, 'frozen', False):
                return False  # Em modo de código aberto (.py), não substitui arquivo

            current_exe = Path(sys.executable).resolve()
            temp_new_exe = current_exe.parent / "VideoDownloader_update.tmp"
            updater_bat = current_exe.parent / "update_runner.bat"

            # Baixa o novo executável
            req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, open(temp_new_exe, "wb") as f:
                total_size = int(resp.headers.get("content-length", 0))
                downloaded = 0
                block_size = 65536

                while True:
                    buffer = resp.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    f.write(buffer)
                    if progress_callback and total_size > 0:
                        progress_callback(downloaded / total_size)

            # Script batch que aguarda o encerramento do app, move o arquivo e reinicia
            bat_content = f"""@echo off
timeout /t 1 /nobreak > nul
:repeat
del "{current_exe}" 2>nul
if exist "{current_exe}" (
    timeout /t 1 /nobreak > nul
    goto repeat
)
move /y "{temp_new_exe}" "{current_exe}" > nul
start "" "{current_exe}"
del "%~f0"
"""
            with open(updater_bat, "w", encoding="utf-8") as f:
                f.write(bat_content)

            # Executa o script invisível e encerra o processo atual
            subprocess.Popen(["cmd.exe", "/c", str(updater_bat)], creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)

        except Exception as e:
            print(f"Erro na atualização: {e}")
            return False
