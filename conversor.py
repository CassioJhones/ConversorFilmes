import os
import json
import subprocess

def obter_mapeamento_dinamico(caminho_mkv):
    """
    Usa o ffprobe para ler as faixas do filme em JSON e retorna
    uma lista de argumentos '-map' contendo apenas os idiomas desejados.
    """
    comando_probe = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "stream=index,codec_type:stream_tags=language", 
        "-of", "json", 
        caminho_mkv
    ]
    
    try:
        resultado = subprocess.run(comando_probe, capture_output=True, text=True, check=True)
        dados = json.loads(resultado.stdout)
        
        argumentos_map = ["-map", "0:v:0"] 
        
        tem_audio = False
        for stream in dados.get("streams", []):
            idx = stream.get("index")
            tipo = stream.get("codec_type")
            tags = stream.get("tags", {})
            lang = tags.get("language", "").lower()
            
            if tipo == "audio":
                if lang in ["por", "eng", "ptbr", "en"] or not tem_audio:
                    argumentos_map.extend(["-map", f"0:{idx}"])
                    tem_audio = True
                    
            elif tipo == "subtitle":
                if lang in ["por", "eng", "ptbr", "en"]:
                    argumentos_map.extend(["-map", f"0:{idx}"])
                    
        return argumentos_map
    except Exception as e:
        print(f"⚠️ Alerta ao analisar com ffprobe (usando mapeamento padrão): {e}")
        return ["-map", "0:v:0", "-map", "0:a:0"]

def converter_para_tv_samsung(diretorio_filmes):
    for arquivo in os.listdir(diretorio_filmes):
        if arquivo.lower().endswith(".mkv"):
            caminho_mkv = os.path.join(diretorio_filmes, arquivo)
            
            novo_nome = arquivo.rsplit('.', 1)[0] + ".mp4"
            caminho_mp4 = os.path.join(diretorio_filmes, novo_nome)
            
            if os.path.exists(caminho_mp4):
                print(f"O arquivo {novo_nome} já existe. Pulando...")
                continue
                
            print(f"Analisando faixas de mídia para: {arquivo}")
            argumentos_map = obter_mapeamento_dinamico(caminho_mkv)
            
            print(f"Iniciando conversão: {arquivo} -> {novo_nome}")
            
            comando = [
                "ffmpeg",
                "-i", caminho_mkv,
                *argumentos_map,
                "-c:v", "libx264",
                "-preset", "fast",           
                "-c:a", "aac",
                "-b:a", "192k",
                "-c:s", "mov_text",
                caminho_mp4
            ]
            
            try:                
                subprocess.run(comando, check=True)
                print(f"✅ Sucesso: {novo_nome} concluído!\n")
            except subprocess.CalledProcessError:
                print(f"❌ Erro ao converter o arquivo: {arquivo}\n")

pasta_dos_filmes = r"C:\Users..."
converter_para_tv_samsung(pasta_dos_filmes)