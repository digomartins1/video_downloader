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
- ⚡ **Auto-Bootstrapper (`launcher.py`):** Arquivo único que baixa o código-fonte atualizado do GitHub, cria a árvore de pastas e instala os pacotes `pip` sem etapas manuais.

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