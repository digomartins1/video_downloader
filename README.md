# 🎬 Video Downloader (Python Modular)

<p align="center">
  <kbd>🐍 Python 3.10+</kbd> • 
  <kbd>⚙️ Engine: yt-dlp</kbd> • 
  <kbd>🎨 UI: Rich CLI</kbd> • 
  <kbd>⚡ Status: Ativo</kbd> • 
  <kbd>📄 Licença: MIT</kbd>
</p>

<p align="center">
  <b>Um baixador e extrator multimídia modular, de alta performance e desacoplado feito em Python.</b><br>
  Suporta download de vídeos em alta resolução (1080p, 2K, 4K), extração de áudio para MP3, gravação de transmissões ao vivo (HLS/DASH) e sistema de inicialização autônoma (Bootstrapper).
</p>

---

## 📑 Índice

- [✨ Funcionalidades e Destaques](#funcionalidades)
- [🖥️ Demonstração Visual](#demonstracao)
- [📁 Arquitetura e Estrutura de Pastas](#arquitetura)
- [⚙️ Pré-requisitos e Dependências](#prerequisitos)
  - [📦 Instalação do FFmpeg](#instalacao-ffmpeg)
- [🚀 Como Instalar e Executar](#instalacao)
  - [Método 1: Inicializador Automático (Bootstrapper)](#bootstrapper)
  - [Método 2: Instalação Manual (Ambiente de Desenvolvimento)](#instalacao-manual)
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
- ⚡ **Auto-Bootstrapper (`launcher.py`):** Arquivo único que baixa o código-fonte atualizado do GitHub, cria a árvore de pastas e instala os pacotes `pip` sem etapas manuais, autoexcluindo-se após a preparação.

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
├── launcher.py                 # 🚀 Instalador autônomo (baixa o projeto, dependências e se autoexclui)
├── main.py                     # 🚪 Ponto de entrada padrão da aplicação (com auto-setup de FFmpeg)
├── requirements.txt            # 📦 Lista de dependências Python (yt-dlp, rich, static-ffmpeg)
├── README.md                   # 📄 Documentação técnica do projeto
├── .gitignore                  # 🙈 Arquivos ignorados pelo controle de versão
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

- **Python 3.10 ou superior:** [Download do Python](https://www.python.org/downloads/) *(Marque a opção "Add Python to PATH" na instalação)*.
- O projeto já conta com a biblioteca **`static-ffmpeg`**, que faz o download automático dos binários do FFmpeg. Caso queira instalá-lo de forma global no seu sistema operacional, use os comandos abaixo:

<a id="instalacao-ffmpeg"></a>
### 📦 Instalação do FFmpeg

#### No Windows:
Abra o **PowerShell como Administrador** e execute:
```powershell
winget install Gyan.FFmpeg
```

#### No Linux (Ubuntu/Debian):
```bash
sudo apt update && sudo apt install ffmpeg -y
```

#### No macOS:
```bash
brew install ffmpeg
```

---

<a id="instalacao"></a>
## 🚀 Como Instalar e Executar

<a id="bootstrapper"></a>
### Método 1: Inicializador Automático (Bootstrapper)
*Indicado para quem não quer clonar o repositório manualmente.*

Execute o comando correspondente no seu terminal:
- **Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/digomartins1/video_downloader/main/launcher.py" -OutFile "launcher.py"; python launcher.py
```
- **Linux / macOS:**
```bash
curl -sSL "https://raw.githubusercontent.com/digomartins1/video_downloader/main/launcher.py" -o launcher.py && python launcher.py
```

O `launcher.py` fará todo o download dos módulos, instalará as dependências, se autoexcluirá e iniciará a aplicação.

---

<a id="instalacao-manual"></a>
### Método 2: Instalação Manual (Ambiente de Desenvolvimento)

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

4. **Execute a aplicação:**
```bash
python main.py
```

---

<a id="guia-de-uso"></a>
## 📖 Guia de Uso Passo a Passo

1. Execute o arquivo principal (`python main.py`).
2. Cole a URL do vídeo ou transmissão que deseja baixar.
3. Aguarde a validação dos metadados (Título, Autor e Duração).
4. Selecione a opção no menu:
   - **`1`**: Melhor qualidade geral de vídeo + melhor áudio combinados.
   - **`2`**: Vídeo em resolução até 1080p (Full HD).
   - **`3`**: Vídeo em resolução até 720p (HD).
   - **`4`**: Extração de áudio convertida para `.mp3`.
5. Ao término, o arquivo estará pronto dentro da pasta `downloads/`.
6. O programa perguntará se você deseja fazer outro download (`s/n`). Ao digitar `s`, a tela é limpa e o processo reinicia.

---

<a id="compatibilidade"></a>
## 📡 Matriz de Compatibilidade e Streaming

| Plataforma / Tipo | Suporte | Observações |
| :--- | :---: | :--- |
| **YouTube (Vídeos e Shorts)** | ✅ Sim | Suporte total até 4K/8K e extração de áudio. |
| **TikTok e Instagram Reels** | ✅ Sim | Download direto sem marca d'água quando disponível. |
| **Twitter / X & Reddit** | ✅ Sim | Extração de mídias e vídeos de posts. |
| **Twitch e Kick (Lives & VODs)** | ✅ Sim | Grava transmissões ao vivo ou gravações passadas. |
| **Streams HLS (`.m3u8`) e DASH (`.mpd`)** | ✅ Sim | Baixa e une blocos de transmissão via FFmpeg. |
| **Serviços com DRM (Netflix, Prime, Disney+)** | ❌ Não | Não suportado devido a criptografia de direitos autorais. |

---

<a id="extensao"></a>
## 🧩 Guia de Extensão para Desenvolvedores

Como o `DownloadService` é totalmente desacoplado da interface de terminal, você pode importá-lo em outros projetos facilmente:

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
    return {"status": "Download adicionado à fila"}
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
<summary><b>1. Erro: <code>ImportError: cannot import name 'DownloadService'</code></b></summary>
Certifique-se de que o arquivo <code>src/services/download_service.py</code> contém o código salvo e a classe declarada como <code>class DownloadService:</code>.
</details>

<details>
<summary><b>2. Erro de FFmpeg ou conversão para MP3 travando</b></summary>
O projeto usa a biblioteca <code>static-ffmpeg</code> para auto-configuração. Caso ocorra erro, instale o FFmpeg no sistema operacional via <code>winget install Gyan.FFmpeg</code> e reinicie o terminal.
</details>

<details>
<summary><b>3. Erro: <code>HTTP Error 403: Forbidden</code></b></summary>
Algumas plataformas atualizam seus bloqueios periodicamente. Para resolver, atualize a engine executando:
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
