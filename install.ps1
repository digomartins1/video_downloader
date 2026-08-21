# 🎬 Video Downloader (Python Modular)

<p align="center">
  <a href="#!"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="#!"><img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp"></a>
  <a href="#!"><img src="https://img.shields.io/badge/UI-Rich_CLI-008000?style=for-the-badge" alt="Rich CLI"></a>
  <a href="#!"><img src="https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge" alt="Status"></a>
  <a href="#!"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <b>Um baixador e extrator multimídia modular, de alta performance e desacoplado feito em Python.</b><br>
  Suporta download de vídeos em alta resolução (1080p, 2K, 4K), extração de áudio para MP3, gravação de transmissões ao vivo (HLS/DASH) e sistema de instalação 100% automático para leigos.
</p>

---

## 📑 Índice

- [✨ Funcionalidades e Destaques](#funcionalidades)
- [🖥️ Demonstração Visual](#demonstracao)
- [📁 Arquitetura e Estrutura de Pastas](#arquitetura)
- [⚙️ Pré-requisitos e Dependências](#prerequisitos)
  - [📦 Instalação do FFmpeg](#instalacao-ffmpeg)
- [🚀 Como Instalar e Executar](#instalacao)
  - [🪟 Método 1: Instalação Automática no Windows (1 Clique - Recomendado para Leigos)](#windows-powershell)
  - [🐧🍏 Método 2: Inicializador Multiplataforma (Linux/macOS)](#bootstrapper)
  - [💻 Método 3: Instalação Manual (Ambiente de Desenvolvimento)](#instalacao-manual)
- [📖 Guia de Uso Passo a Passo](#guia-de-uso)
- [📡 Matriz de Compatibilidade e Streaming](#compatibilidade)
- [🧩 Guia de Extensão para Desenvolvedores](#extensao)
- [🛠️ Configurações Avançadas](#configuracoes)
- [❓ Resolução de Problemas (FAQ)](#faq)
- [🗺️ Roadmap (Próximos Passos)](#roadmap)
- [🤝 Como Contribuir](#contribuir)
- [📄 Licença](#licenca)

---

<a id="funcionalidades"></a>
## ✨ Funcionalidades e Destaques

- 🌐 **Amplo Suporte a Plataformas:** Baixa vídeos do YouTube (incluindo Shorts), TikTok, Instagram (Reels/Vídeos), Twitter/X, Twitch, Facebook, Vimeo, Reddit e mais de 1000 outros sites suportados pela engine `yt-dlp`.
- 🔴 **Captura de Transmissões ao Vivo (Livestreams):** Gravação em tempo real de transmissões (YouTube Live, Twitch, Kick) e links diretos nos protocolos **HLS (`.m3u8`)** e **DASH (`.mpd`)**.
- 🎞️ **Controle de Resolução:** Seleção dinâmica da melhor qualidade disponível (até 4K/8K) ou opções travadas (1080p, 720p, etc.) com união automática de vídeo e áudio.
- 🎵 **Conversor MP3 Integrado:** Extrai apenas a faixa sonora na melhor qualidade e a codifica em `.mp3` (192 kbps) com pós-processamento FFmpeg.
- 📊 **Interface de Terminal com `Rich`:** Exibição de metadados do vídeo (título, autor, duração), spinners animados e barra de download com velocidade (MB/s), bytes transferidos e tempo restante (ETA).
- 🧱 **Arquitetura Desacoplada (Clean Architecture / SRP):** Serviços isolados da interface gráfica/CLI para que o núcleo de download possa ser reaproveitado em APIs Web (FastAPI) ou interfaces Desktop (CustomTkinter/PyQt).
- ⚡ **Instalação Automática para Leigos:** Com apenas 1 linha de comando no terminal do Windows, o sistema instala o Python (se faltar), baixa o FFmpeg, cria um ambiente isolado e abre o programa sozinho.

---

<a id="demonstracao"></a>
## 🖥️ Demonstração Visual

Exemplo do fluxo de execução no terminal:

```text
╭────────────────── Python Video Downloader ──────────────────╮
╰─────────────────────────────────────────────────────────────╯

Insira a URL do vídeo: https://www.youtube.com/watch?v=Exemplo

╭─ Vídeo Encontrado ──────────────────────────────────────────╮
│ Título: Documentário sobre Tecnologia                       │
│ Canal/Autor: Canal Exemplo                                  │
│ Duração: 14:32                                              │
╰─────────────────────────────────────────────────────────────╯

Escolha o tipo de download:
1. Melhor Vídeo disponível (com áudio)
2. Vídeo 1080p
3. Vídeo 720p
4. Apenas Áudio (MP3)

Opção (1-4): 2

Baixando... ━━━━━━━━━━━━━━━━━━━━━━━━━╸ 78% 45.2/57.9 MB 4.2 MB/s 00:03

✔ Download concluído com sucesso! Arquivo salvo na pasta downloads/

Deseja baixar outro vídeo? (s/n):
```

---

<a id="arquitetura"></a>
## 📁 Arquitetura e Estrutura de Pastas

```text
video_downloader/
│
├── install.ps1                 # 🪟 Instalador 100% automático para Windows (PowerShell)
├── launcher.py                 # 🚀 Instalador autônomo multiplataforma (Linux/macOS)
├── main.py                     # 🚪 Ponto de entrada padrão da aplicação (com auto-setup de FFmpeg)
├── requirements.txt            # 📦 Lista de dependências Python (yt-dlp, rich, static-ffmpeg)
├── README.md                   # 📄 Documentação técnica do projeto
├── .gitignore                  # 🙈 Arquivos ignorados pelo controle de versão
├── LICENSE                     # ⚖️ Licença oficial MIT
│
├── downloads/                  # 💾 Diretório onde os arquivos de mídia são salvos
│
└── src/                        # 🧠 Código-fonte modularizado
    ├── __init__.py
    ├── config.py               # ⚙️ Definições de diretórios e parâmetros base do yt-dlp
    │
    ├── services/               # 💼 Camada de Regras de Negócio e Serviços
    │   ├── __init__.py
    │   ├── info_service.py     # 🔍 Extração segura de metadados sem download prévio
    │   └── download_service.py # 📥 Motor de download, seleção de codec e conversão
    │
    ├── utils/                  # 🛠️ Funções Utilitárias e Ajudantes
    │   ├── __init__.py
    │   └── formatters.py       # ⏱️ Formatadores de tempo e tamanho legível de bytes
    │
    └── cli/                    # 🖥️ Camada de Apresentação (Interface de Usuário)
        ├── __init__.py
        └── interface.py        # 🎨 Menus, loop de repetição e barras de progresso
```

---

<a id="prerequisitos"></a>
## ⚙️ Pré-requisitos e Dependências

- **Python 3.10 ou superior:** [Download do Python](https://www.python.org/downloads/) *(Marque a opção "Add Python to PATH" caso instale manualmente)*.
- O projeto já possui a biblioteca **`static-ffmpeg`** embutida, que baixa e configura os binários do FFmpeg de forma totalmente automática.

<a id="instalacao-ffmpeg"></a>
### 📦 Instalação do FFmpeg (Opcional)

Se preferir instalar o FFmpeg diretamente no seu sistema operacional:

- **Windows:** `winget install Gyan.FFmpeg`
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg -y`
- **macOS:** `brew install ffmpeg`

---

<a id="instalacao"></a>
## 🚀 Como Instalar e Executar

<a id="windows-powershell"></a>
### 🪟 Método 1: Instalação Automática no Windows (1 Clique - Recomendado para Leigos)

Não é necessário saber programar nem instalar o Python previamente. O script faz **tudo sozinho**:

#### 📌 Passo a Passo Detalhado:

1. **Abra o PowerShell no seu computador:**
   - No teclado, pressione a tecla **Windows** (ou clique no menu Iniciar).
   - Digite **`PowerShell`**.
   - Clique em **Windows PowerShell** para abrir a janela azul/preta.

2. **Copie e cole o comando abaixo:**
   ```powershell
   irm https://raw.githubusercontent.com/digomartins1/video_downloader/main/install.ps1 | iex
   ```
   > *(Dica: No PowerShell, basta clicar com o **botão direito do mouse** dentro da janela para colar o texto).*

3. **Pressione a tecla Enter:**
   - O instalador verificará se você tem Python (se não tiver, ele instala o Python 3.12 sozinho).
   - Ele cria um ambiente virtual isolado em uma pasta segura.
   - Baixa o projeto, configura o suporte a conversão de MP3 e abre o baixador imediatamente na sua tela.

---

<a id="bootstrapper"></a>
### 🐧🍏 Método 2: Inicializador Multiplataforma (Linux / macOS)

Se você já possui Python instalado e está no Linux ou Mac:

1. Baixe o arquivo [`launcher.py`](launcher.py) ou execute no terminal:
   ```bash
   curl -sSL "https://raw.githubusercontent.com/digomartins1/video_downloader/main/launcher.py" -o launcher.py && python launcher.py
   ```
2. O script fará o download dos arquivos, instalará os pacotes e iniciará a aplicação.

---

<a id="instalacao-manual"></a>
### 💻 Método 3: Instalação Manual (Ambiente de Desenvolvimento)

Para quem deseja clonar o código e programar:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/digomartins1/video_downloader.git
   cd video_downloader
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto:**
   ```bash
   python main.py
   ```

---

<a id="guia-de-uso"></a>
## 📖 Guia de Uso Passo a Passo

1. Inicie o programa pelo terminal.
2. Cole a URL do vídeo ou transmissão que deseja baixar.
3. O sistema exibirá o **Título**, **Canal/Autor** e **Duração**.
4. Escolha a opção desejada:
   - **`1`**: Melhor qualidade de vídeo e áudio combinados.
   - **`2`**: Vídeo em resolução até 1080p (Full HD).
   - **`3`**: Vídeo em resolução até 720p (HD).
   - **`4`**: Extração de áudio convertida para `.mp3`.
5. Acompanhe a barra com velocidade em tempo real. O arquivo será salvo na pasta `downloads/`.
6. Ao finalizar, o programa perguntará: `Deseja baixar outro vídeo? (s/n)`. Digitando `s`, a tela é limpa para um novo download.

---

<a id="compatibilidade"></a>
## 📡 Matriz de Compatibilidade e Streaming

| Plataforma / Tipo | Suporte | Observações |
| :--- | :---: | :--- |
| **YouTube (Vídeos e Shorts)** | ✅ Sim | Suporte total até 4K/8K e extração de áudio. |
| **TikTok e Instagram Reels** | ✅ Sim | Download direto sem marca d'água quando disponível. |
| **Twitter / X & Reddit** | ✅ Sim | Extração de mídias e vídeos anexados a posts. |
| **Twitch e Kick (Lives & VODs)** | ✅ Sim | Grava transmissões ao vivo ou gravações passadas. |
| **Streams HLS (`.m3u8`) e DASH (`.mpd`)** | ✅ Sim | Baixa e une blocos de transmissão via FFmpeg. |
| **Serviços com DRM (Netflix, Prime, Disney+)** | ❌ Não | Não suportado devido a criptografia de direitos autorais. |

---

<a id="extensao"></a>
## 🧩 Guia de Extensão para Desenvolvedores

O módulo `DownloadService` é totalmente desacoplado da interface visual e pode ser integrado em outros sistemas:

### Exemplo em Interface Gráfica (Desktop GUI com CustomTkinter ou PyQt):
```python
from src.services.download_service import DownloadService

def progresso(d):
    if d['status'] == 'downloading':
        porcentagem = (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100
        minha_barra.set(porcentagem)

downloader = DownloadService(progress_hook=progresso)
downloader.download("https://www.youtube.com/watch?v=exemplo", format_choice="1080")
```

### Exemplo em API REST (FastAPI):
```python
from fastapi import FastAPI, BackgroundTasks
from src.services.download_service import DownloadService

app = FastAPI()

@app.post("/api/download")
def api_download(url: str, background_tasks: BackgroundTasks):
    downloader = DownloadService()
    background_tasks.add_task(downloader.download, url)
    return {"status": "Download iniciado em segundo plano"}
```

---

<a id="configuracoes"></a>
## 🛠️ Configurações Avançadas

Para alterar diretórios ou parâmetros do motor de download, edite o arquivo `src/config.py`:

```python
# Modificar o diretório padrão onde os vídeos são salvos:
DOWNLOAD_DIR = Path("D:/MeusVideos")

# Adicionar limites de velocidade ou proxies no yt-dlp:
DEFAULT_YT_DLP_OPTS = {
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
    "ratelimit": 5000000, # Limita o download em 5MB/s
    "quiet": True,
}
```

---

<a id="faq"></a>
## ❓ Resolução de Problemas (FAQ)

<details>
<summary><b>1. Onde ficam salvos os vídeos que eu baixo?</b></summary>
Todos os vídeos baixados são salvos automaticamente dentro da pasta <code>downloads/</code> localizada dentro do diretório do projeto.
</details>

<details>
<summary><b>2. Erro de FFmpeg ou conversão para MP3 travando</b></summary>
O projeto utiliza a biblioteca <code>static-ffmpeg</code> para configuração automática. Caso o seu sistema possua restrições, instale o FFmpeg via <code>winget install Gyan.FFmpeg</code> no PowerShell e reinicie o terminal.
</details>

<details>
<summary><b>3. Erro: <code>HTTP Error 403: Forbidden</code> ou bloqueio temporário</b></summary>
Alguns sites atualizam suas proteções periodicamente. Para atualizar a engine de download, execute:
```bash
pip install --upgrade yt-dlp
```
</details>

---

<a id="roadmap"></a>
## 🗺️ Roadmap (Próximos Passos)

- [ ] Suporte a download de playlists completas com numeração de faixas.
- [ ] Download e sincronização automática de legendas (`.srt`).
- [ ] Interface gráfica desktop nativa construída com CustomTkinter.
- [ ] Fila de downloads paralelos (Multi-threading).

---

<a id="contribuir"></a>
## 🤝 Como Contribuir

1. Faça um **Fork** do repositório.
2. Crie uma Branch para sua modificação (`git checkout -b feature/MinhaNovaFeature`).
3. Faça o commit das alterações (`git commit -m 'Adiciona funcionalidade X'`).
4. Envie para o GitHub (`git push origin feature/MinhaNovaFeature`).
5. Abra um **Pull Request**.

---

<a id="licenca"></a>
## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

<p align="center">
  Desenvolvido com 🐍 Python e mantido pela comunidade open-source.
</p>
