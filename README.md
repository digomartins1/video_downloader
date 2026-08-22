# 🎬 Video Downloader (Python GUI Modular)

<p align="center">
  <a href="#!"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="#!"><img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp"></a>
  <a href="#!"><img src="https://img.shields.io/badge/UI-CustomTkinter-blue?style=for-the-badge" alt="CustomTkinter GUI"></a>
  <a href="#!"><img src="https://img.shields.io/badge/Auto--Update-GitHub_Releases-green?style=for-the-badge" alt="Auto-Update"></a>
  <a href="#!"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <b>Um baixador multimídia moderno com Interface Gráfica nativa (Modo Escuro), modular, de alta performance e desacoplado feito em Python.</b><br>
  Suporta download de vídeos em alta resolução (1080p, 2K, 4K), extração para MP3, transmissões ao vivo (HLS/DASH), instalador automático e <b>sistema de auto-atualização embutido</b>.
</p>

---

## 📑 Índice

- [✨ Funcionalidades e Destaques](#funcionalidades)
- [🖥️ Demonstração da Interface Gráfica](#demonstracao)
- [📁 Arquitetura e Estrutura de Pastas](#arquitetura)
- [⚙️ Pré-requisitos](#prerequisitos)
  - [📦 Suporte ao FFmpeg](#instalacao-ffmpeg)
- [🚀 Como Instalar e Executar](#instalacao)
  - [🪟 Método 1: Instalação Automática no Windows (1 Clique - Recomendado para Leigos)](#windows-powershell)
  - [🐧🍏 Método 2: Inicializador Multiplataforma (Linux/macOS)](#bootstrapper)
  - [💻 Método 3: Instalação Manual (Ambiente de Desenvolvimento)](#instalacao-manual)
- [🔨 Como Gerar o Executável (.EXE)](#gerar-exe)
- [🔄 Como Funciona a Auto-Atualização](#auto-update)
- [📖 Guia de Uso](#guia-de-uso)
- [📡 Matriz de Compatibilidade e Streaming](#compatibilidade)
- [🛠️ Configurações Avançadas](#configuracoes)
- [❓ Resolução de Problemas (FAQ)](#faq)
- [🤝 Como Contribuir](#contribuir)
- [📄 Licença](#licenca)

---

<a id="funcionalidades"></a>
## ✨ Funcionalidades e Destaques

- 🎨 **Interface Gráfica Moderna (GUI):** Visual escuro profissional estilo Windows 11 desenvolvido com `CustomTkinter`.
- 🔄 **Sistema de Auto-Atualização:** O programa checa a API do GitHub Releases e se atualiza sozinho sem quebrar o executável.
- 🌐 **Amplo Suporte a Plataformas:** Baixa vídeos do YouTube (incluindo Shorts), TikTok, Instagram (Reels/Vídeos), Twitter/X, Twitch, Facebook, Vimeo, Reddit e mais de 1000 outros sites suportados pela engine `yt-dlp`.
- 🔴 **Captura de Transmissões ao Vivo (Livestreams):** Gravação em tempo real de transmissões (YouTube Live, Twitch, Kick) e links diretos nos protocolos **HLS (`.m3u8`)** e **DASH (`.mpd`)**.
- 🎞️ **Controle de Resolução:** Seleção dinâmica da melhor qualidade disponível (até 4K/8K) ou opções travadas (1080p, 720p, 480p).
- 🎵 **Conversor MP3 Integrado:** Extrai apenas a faixa sonora na melhor qualidade e a codifica em `.mp3` (192 kbps) com pós-processamento FFmpeg automático via `static-ffmpeg`.
- 📁 **Acesso Rápido:** Botão na interface para abrir a pasta `downloads/` diretamente no Windows Explorer.
- ⚡ **Instalação em 1 Linha:** Comando para o PowerShell que instala o Python (se faltar), configura o ambiente isolado e abre o programa automaticamente.

---

<a id="demonstracao"></a>
## 🖥️ Demonstração da Interface Gráfica

A aplicação conta com uma interface desktop intuitiva:

- **Campo de Entrada com Busca:** Cole a URL e clique em "Buscar" para visualizar o Título, Canal e Duração antes de baixar.
- **Menu de Seleção de Formato:** Alterne entre *Melhor Qualidade*, *1080p*, *720p*, *480p* ou *Apenas Áudio (MP3)*.
- **Barra de Progresso Fluida:** Acompanhe a porcentagem e a velocidade em tempo real (MB/s).
- **Notificação de Atualização:** Janela pop-up avisando quando houver uma nova versão disponível no GitHub.

---

<a id="arquitetura"></a>
## 📁 Arquitetura e Estrutura de Pastas

```text
video_downloader/
│
├── install.ps1                 # 🪟 Instalador 100% automático para Windows (PowerShell)
├── launcher.py                 # 🚀 Instalador autônomo multiplataforma (Linux/macOS)
├── main.py                     # 🚪 Ponto de entrada que inicia a Interface Gráfica
├── requirements.txt            # 📦 Lista de dependências (yt-dlp, rich, static-ffmpeg, customtkinter, pyinstaller)
├── README.md                   # 📄 Documentação técnica do projeto
├── .gitignore                  # 🙈 Arquivos ignorados pelo Git
├── LICENSE                     # ⚖️ Licença oficial MIT
│
├── downloads/                  # 💾 Diretório onde os arquivos de mídia são salvos
│
└── src/                        # 🧠 Código-fonte modularizado
    ├── __init__.py
    ├── config.py               # ⚙️ Versão atual (v1.0.0), repositório e diretórios
    │
    ├── services/               # 💼 Camada de Regras de Negócio e Serviços
    │   ├── __init__.py
    │   ├── info_service.py     # 🔍 Extração segura de metadados sem download prévio
    │   ├── download_service.py # 📥 Motor de download, seleção de codec e conversão
    │   └── update_service.py   # 🔄 Verificador e instalador de atualizações via GitHub
    │
    ├── utils/                  # 🛠️ Funções Utilitárias
    │   ├── __init__.py
    │   └── formatters.py       # ⏱️ Formatadores de tempo e tamanho legível de bytes
    │
    └── gui/                    # 🎨 Camada de Interface Gráfica (Desktop)
        ├── __init__.py
        └── interface.py        # 🖥️ Janela CustomTkinter com modo escuro e threads
```

---

<a id="prerequisitos"></a>
## ⚙️ Pré-requisitos

- **Python 3.10 ou superior:** [Download do Python](https://www.python.org/downloads/) *(Marque a opção "Add Python to PATH")*.

<a id="instalacao-ffmpeg"></a>
### 📦 Suporte ao FFmpeg

O projeto já inclui a biblioteca **`static-ffmpeg`**, que baixa e configura os binários do FFmpeg e FFprobe de forma automática em segundo plano.

Caso queira instalá-lo de forma global no sistema operacional:
- **Windows:** `winget install Gyan.FFmpeg`
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg -y`
- **macOS:** `brew install ffmpeg`

---

<a id="instalacao"></a>
## 🚀 Como Instalar e Executar

<a id="windows-powershell"></a>
### 🪟 Método 1: Instalação Automática no Windows (1 Clique - Recomendado para Leigos)

Não requer conhecimento de programação nem instalação prévia de Python:

1. Abra o **PowerShell** no Windows (Pressione a tecla Windows, digite `PowerShell` e aperte Enter).
2. Cole o comando abaixo e aperte **Enter**:
   ```powershell
   irm https://raw.githubusercontent.com/digomartins1/video_downloader/main/install.ps1 | iex
   ```
3. O script cuidará de tudo: instala o Python (se faltar), cria o ambiente virtual, baixa as dependências e abre a interface gráfica na hora.

---

<a id="bootstrapper"></a>
### 🐧🍏 Método 2: Inicializador Multiplataforma (Linux / macOS)

Se você já possui Python instalado e está no Linux ou Mac:

```bash
curl -sSL "https://raw.githubusercontent.com/digomartins1/video_downloader/main/launcher.py" -o launcher.py && python launcher.py
```

---

<a id="instalacao-manual"></a>
### 💻 Método 3: Instalação Manual (Ambiente de Desenvolvimento)

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

4. **Inicie o programa:**
   ```bash
   python main.py
   ```

---

<a id="gerar-exe"></a>
## 🔨 Como Gerar o Executável (.EXE)

Para compilar todo o projeto em um único arquivo `.exe` fechado para distribuir para qualquer computador Windows:

```powershell
pyinstaller --noconsole --onefile --name "VideoDownloader" --collect-all customtkinter main.py
```

O arquivo final será gerado dentro da pasta **`dist/VideoDownloader.exe`**.

---

<a id="auto-update"></a>
## 🔄 Como Funciona a Auto-Atualização

Quando o aplicativo roda no modo `.exe`, ele verifica se há novas versões disponíveis no GitHub Releases:

1. O desenvolvedor altera a variável `CURRENT_VERSION = "1.0.1"` no `src/config.py`.
2. Compila o `.exe` com o comando do PyInstaller.
3. Cria uma **Nova Release** no GitHub com a tag `v1.0.1` e anexa o `VideoDownloader.exe`.
4. Quando o usuário abrir o programa, aparecerá um aviso: *"Nova versão 1.0.1 disponível! Deseja atualizar?"*.
5. Ao confirmar, o programa baixa o arquivo, substitui o `.exe` em segundo plano e reinicia atualizado sozinho.

---

<a id="guia-de-uso"></a>
## 📖 Guia de Uso

1. Abra o aplicativo (pela interface gráfica ou executável).
2. Cole o link do vídeo e clique em **Buscar**.
3. Escolha o formato desejado (Vídeo ou MP3).
4. Clique em **Baixar Agora**.
5. Ao finalizar, clique em **Abrir Pasta de Downloads** para acessar seu arquivo.

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
| **Serviços com DRM (Netflix, Prime, Disney+)** | ❌ Não | Não suportado devido a restrições legais de direitos autorais. |

---

<a id="configuracoes"></a>
## 🛠️ Configurações Avançadas

Para alterar diretórios ou parâmetros do motor de download, edite o arquivo `src/config.py`:

```python
# Modificar a versão da sua aplicação:
CURRENT_VERSION = "1.0.0"

# Modificar a pasta onde os vídeos são salvos:
DOWNLOAD_DIR = Path("D:/MeusVideos")

# Configurações do yt-dlp:
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
Todos os arquivos são salvos na pasta <code>downloads/</code>. Você pode clicar no botão "Abrir Pasta de Downloads" na interface para acessá-los diretamente.
</details>

<details>
<summary><b>2. Erro de FFmpeg ou conversão para MP3 travando</b></summary>
O projeto utiliza a biblioteca <code>static-ffmpeg</code> para auto-configuração. Se necessário, instale o FFmpeg no sistema via <code>winget install Gyan.FFmpeg</code> no PowerShell.
</details>

<details>
<summary><b>3. Erro: <code>HTTP Error 403: Forbidden</code></b></summary>
Alguns sites atualizam suas proteções periodicamente. Para resolver, atualize a engine executando:
```bash
pip install --upgrade yt-dlp
```
</details>

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
