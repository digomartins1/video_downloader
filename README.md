# 🎬 Video Downloader (Python Modular)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Engine-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp">
  <img src="https://img.shields.io/badge/UI-Rich_CLI-008000?style=for-the-badge" alt="Rich CLI">
  <img src="https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License">
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
- [🚀 Como Instalar e Executar](#instalacao)
- [📖 Guia de Uso Passo a Passo](#guia-de-uso)
- [📡 Matriz de Compatibilidade e Streaming](#compatibilidade)
- [🤝 Como Contribuir](#contribuir)
- [📄 Licença](#licenca)

---

<a id="funcionalidades"></a>
## ✨ Funcionalidades e Destaques

- 🌐 **Amplo Suporte a Plataformas:** Baixa vídeos do YouTube, TikTok, Instagram, Twitter/X e mais de 1000 sites via `yt-dlp`.
- 🔴 **Captura de Transmissões ao Vivo:** Gravação de links **HLS (`.m3u8`)** e **DASH (`.mpd`)**.
- 🎞️ **Controle de Resolução:** Seleção dinâmica até 4K/8K com união automática via FFmpeg.
- 🎵 **Conversor MP3 Integrado:** Extração direta de áudio em 192 kbps.
- 📊 **Interface Rich CLI:** Feedback visual com barras de progresso e metadados detalhados.
- ⚡ **Auto-Bootstrapper:** Script que configura o ambiente e dependências automaticamente.

---

<a id="demonstracao"></a>
## 🖥️ Demonstração Visual

```text
╭────────────────── Python Video Downloader ──────────────────╮
╰─────────────────────────────────────────────────────────────╯

Insira a URL do vídeo: https://www.youtube.com/watch?v=Exemplo

╭─ Vídeo Encontrado ──────────────────────────────────────────╮
│ Título: Documentário sobre Tecnologia                       │
│ Canal/Autor: Canal Exemplo                                  │
│ Duração: 14:32                                              │
╰─────────────────────────────────────────────────────────────╯

Opção (1-4): 2

Baixando... ━━━━━━━━━━━━━━━━━━━━━━━━━╸ 78% 45.2/57.9 MB 4.2 MB/s 00:03