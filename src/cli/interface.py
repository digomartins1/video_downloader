from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from src.services.info_service import InfoService
from src.services.download_service import DownloadService
from src.utils.formatters import format_duration

console = Console()


class CLIInterface:
    def __init__(self):
        self.progress = None
        self.task_id = None

    def _progress_hook(self, d: dict):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            if self.progress and self.task_id is not None:
                self.progress.update(self.task_id, total=total, completed=downloaded)
        elif d["status"] == "finished":
            if self.progress and self.task_id is not None:
                self.progress.update(self.task_id, description="[green]Processando arquivo...")

    def run(self):
        console.print(Panel.fit("[bold cyan]Python Video Downloader[/bold cyan]", border_style="blue"))

        url = console.input("\n[bold yellow]Insira a URL do vídeo:[/bold yellow] ").strip()
        if not url:
            console.print("[red]URL inválida![/red]")
            return

        with console.status("[cyan]Obtendo informações do vídeo...[/cyan]"):
            info = InfoService.get_info(url)

        if not info:
            console.print("[red]Não foi possível acessar as informações da URL.[/red]")
            return

        console.print(Panel(
            f"[bold]Título:[/bold] {info.get('title')}\n"
            f"[bold]Canal/Autor:[/bold] {info.get('uploader', 'Desconhecido')}\n"
            f"[bold]Duração:[/bold] {format_duration(info.get('duration'))}",
            title="[green]Vídeo Encontrado[/green]"
        ))

        console.print("\n[bold]Escolha o tipo de download:[/bold]")
        console.print("1. Melhor Vídeo disponível (com áudio)")
        console.print("2. Vídeo 1080p")
        console.print("3. Vídeo 720p")
        console.print("4. Apenas Áudio (MP3)")

        opcao = console.input("\nOpção (1-4): ").strip()

        is_audio = False
        res = "best"

        if opcao == "2":
            res = "1080"
        elif opcao == "3":
            res = "720"
        elif opcao == "4":
            is_audio = True

        downloader = DownloadService(progress_hook=self._progress_hook)

        with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                console=console
        ) as progress:
            self.progress = progress
            self.task_id = progress.add_task("Baixando...", total=None)
            success = downloader.download(url, format_choice=res, is_audio_only=is_audio)

        if success:
            console.print(
                "\n[bold green]✔ Download concluído com sucesso![/bold green] Arquivo salvo na pasta [cyan]downloads/[/cyan]")
        else:
            console.print("\n[bold red]✖ Falha no download.[/bold red]")