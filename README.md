
# 🎬 Conversor de MKV para MP4

Utiliza o **FFmpeg** para converter arquivos de vídeo `.mkv` para o formato `.mp4`. Ele foi feito para garantir compatibilidade com Smart TVs (Samsung), otimizando codecs de vídeo e áudio, além de filtrar trilhas e legendas.

## ✨ Funcionalidades

* **Conversão Otimizada:** Converte o vídeo para H.264 (`libx264`) e o áudio para AAC estéreo (`128k`), garantindo compatibilidade com TVs.
* **Filtragem Inteligente de Idiomas:** Analisa o arquivo original usando `ffprobe` e extrai apenas as trilhas de áudio e legendas em **Português** (`por`, `ptbr`) ou **Inglês** (`eng`, `en`).
* **Corte Automático (Skip Credits):** Remove automaticamente os últimos 3 minutos (180 segundos) do vídeo.
* **Processamento em Lote:** Lê todos os arquivos `.mkv` de um diretório e os salva em uma subpasta chamada `Convertidos`. Pula automaticamente os arquivos que já foram processados.
* **Desligamento Automático:** Após converter todos os arquivos do diretório, desliga o computador em 30 segundos.

## 🛠️ Pré-requisitos

Necessario ter instalado:

1. **Python 3.x**
2. **FFmpeg e FFprobe:** Você precisa baixar o FFmpeg e colocar os executáveis `ffmpeg` e `ffprobe` nas **Variáveis de Ambiente (PATH)** do Windows.
* [Link para download do FFmpeg](https://ffmpeg.org/download.html)


## 🚀 Como usar

1. Faça o clone deste repositório.
2. Abra o arquivo `conversor.py` em um editor de texto ou IDE.
3. Altere a variável `pasta_dos_filmes` para o caminho da pasta onde estão os arquivos `.mkv`:

```python
# Exemplo:
pasta_dos_filmes = r"C:\User\Filmes\Arrow\"

```

4. Execute o script através do terminal:

```bash
python nome_do_script.py

```

> **⚠️ ATENÇÃO - DESLIGAMENTO AUTOMÁTICO:**
> Ao finalizar a conversão de todos os vídeos da pasta, executará o comando `shutdown /s /f /t 30` para desligar o PC em 30 segundos.

## ⚙️ Detalhes

O FFmpeg utiliza as seguintes configurações:

* `-c:v libx264 -preset fast -crf 26`: Conversão de vídeo, mantendo uma qualidade boa com tamanho de arquivo reduzido.
* `-c:a aac -ac 2 -b:a 128k`: Áudio estéreo aceito em todas as TVs.
* `-c:s mov_text`: Formato de legenda compatível com MP4.