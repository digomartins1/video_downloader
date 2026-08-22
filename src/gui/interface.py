import os
import threading
import customtkinter as ctk
from tkinter import messagebox
from src.config import DOWNLOAD_DIR
from src.services.info_service import InfoService
from src.services.download_service import DownloadService
from src.utils.formatters import format_duration

# Configurações do Tema Visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VideoDownloaderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("Python Video Downloader")
        self.geometry("650x580")
        self.resizable(False, False)

        self.current_info = None

        self._build_ui()

    def _build_ui(self):
        # Título Principal
        self.title_label = ctk.CTkLabel(
            self, 
            text="🎬 Video Downloader", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Campo de Entrada de URL
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.pack(fill="x", padx=30, pady=10)

        self.url_entry = ctk.CTkEntry(
            self.url_frame, 
            placeholder_text="Cole a URL do vídeo aqui (YouTube, TikTok, Twitch, etc.)...",
            height=40
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)

        self.btn_search = ctk.CTkButton(
            self.url_frame, 
            text="Buscar", 
            width=100, 
            height=40,
            command=self._on_search_clicked
        )
        self.btn_search.pack(side="right", padx=(0, 10), pady=10)

        # Card de Informações do Vídeo
        self.info_card = ctk.CTkFrame(self)
        self.info_card.pack(fill="x", padx=30, pady=10)

        self.lbl_video_title = ctk.CTkLabel(
            self.info_card, 
            text="Título: Nenhum vídeo carregado", 
            anchor="w", 
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=570
        )
        self.lbl_video_title.pack(fill="x", padx=15, pady=(10, 2))

        self.lbl_video_author = ctk.CTkLabel(
            self.info_card, 
            text="Canal/Autor: -", 
            anchor="w",
            text_color="gray"
        )
        self.lbl_video_author.pack(fill="x", padx=15, pady=2)

        self.lbl_video_duration = ctk.CTkLabel(
            self.info_card, 
            text="Duração: -", 
            anchor="w",
            text_color="gray"
        )
        self.lbl_video_duration.pack(fill="x", padx=15, pady=(2, 10))

        # Seletor de Qualidade / Formato
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(fill="x", padx=30, pady=10)

        self.lbl_format = ctk.CTkLabel(self.options_frame, text="Formato:")
        self.lbl_format.pack(side="left", padx=(15, 10), pady=10)

        self.combo_format = ctk.CTkComboBox(
            self.options_frame,
            values=[
                "Melhor Qualidade (Vídeo)",
                "Vídeo 1080p",
                "Vídeo 720p",
                "Vídeo 480p",
                "Apenas Áudio (MP3)"
            ],
            width=220
        )
        self.combo_format.pack(side="left", padx=5, pady=10)
        self.combo_format.set("Melhor Qualidade (Vídeo)")

        # Botão de Download
        self.btn_download = ctk.CTkButton(
            self, 
            text="Baixar Agora", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            state="disabled",
            command=self._on_download_clicked
        )
        self.btn_download.pack(fill="x", padx=30, pady=15)

        # Barra de Progresso e Status
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=30, pady=(5, 5))
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(self, text="Aguardando link...", text_color="gray")
        self.lbl_status.pack(pady=(2, 10))

        # Botão para Abrir Pasta de Downloads
        self.btn_open_folder = ctk.CTkButton(
            self, 
            text="📁 Abrir Pasta de Downloads", 
            fg_color="transparent", 
            border_width=1,
            hover_color="#333333",
            command=self._open_download_folder
        )
        self.btn_open_folder.pack(pady=(0, 15))

    def _on_search_clicked(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL válida!")
            return

        self.btn_search.configure(state="disabled")
        self.lbl_status.configure(text="🔍 Obtendo informações do vídeo...", text_color="#1f6aa5")

        # Executa a busca em segundo plano (thread) para não travar a janela
        threading.Thread(target=self._search_thread, args=(url,), daemon=True).start()

    def _search_thread(self, url):
        info = InfoService.get_info(url)
        
        self.after(0, lambda: self._update_video_info(info))

    def _update_video_info(self, info):
        self.btn_search.configure(state="normal")

        if not info:
            self.lbl_status.configure(text="❌ Não foi possível carregar o vídeo.", text_color="red")
            messagebox.showerror("Erro", "Falha ao acessar o link. Verifique a URL.")
            return

        self.current_info = info
        self.lbl_video_title.configure(text=f"Título: {info.get('title', 'Sem título')}")
        self.lbl_video_author.configure(text=f"Canal/Autor: {info.get('uploader', 'Desconhecido')}")
        self.lbl_video_duration.configure(text=f"Duração: {format_duration(info.get('duration'))}")

        self.btn_download.configure(state="normal")
        self.lbl_status.configure(text="✔ Vídeo pronto para download.", text_color="#2fa572")

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            
            if total > 0:
                percent = downloaded / total
                speed = d.get("speed", 0) or 0
                speed_mb = speed / (1024 * 1024)
                
                self.after(0, lambda: self._update_progress(percent, f"Baixando: {percent*100:.1f}% ({speed_mb:.2f} MB/s)"))
        elif d["status"] == "finished":
            self.after(0, lambda: self._update_progress(1.0, "Processando e finalizando arquivo..."))

    def _update_progress(self, percent, text):
        self.progress_bar.set(percent)
        self.lbl_status.configure(text=text, text_color="#1f6aa5")

    def _on_download_clicked(self):
        url = self.url_entry.get().strip()
        selected_format = self.combo_format.get()

        is_audio = False
        res = "best"

        if selected_format == "Apenas Áudio (MP3)":
            is_audio = True
        elif "1080p" in selected_format:
            res = "1080"
        elif "720p" in selected_format:
            res = "720"
        elif "480p" in selected_format:
            res = "480"

        # Trava os botões durante o download
        self.btn_download.configure(state="disabled")
        self.btn_search.configure(state="disabled")
        self.progress_bar.set(0)

        # Inicia o download em uma thread separada
        threading.Thread(target=self._download_thread, args=(url, res, is_audio), daemon=True).start()

    def _download_thread(self, url, res, is_audio):
        downloader = DownloadService(progress_hook=self._progress_hook)
        success = downloader.download(url, format_choice=res, is_audio_only=is_audio)

        self.after(0, lambda: self._download_finished(success))

    def _download_finished(self, success):
        self.btn_download.configure(state="normal")
        self.btn_search.configure(state="normal")

        if success:
            self.lbl_status.configure(text="✔ Download concluído com sucesso!", text_color="#2fa572")
            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
        else:
            self.lbl_status.configure(text="❌ Falha no download.", text_color="red")
            messagebox.showerror("Erro", "Ocorreu um erro durante o download.")

    def _open_download_folder(self):
        """Abre a pasta de downloads no explorador de arquivos do sistema operacional."""
        if os.name == 'nt':
            os.startfile(DOWNLOAD_DIR)
        else:
            import subprocess
            subprocess.Popen(["xdg-open", str(DOWNLOAD_DIR)])
