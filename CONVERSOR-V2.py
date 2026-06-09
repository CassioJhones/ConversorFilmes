import os
import json
import subprocess

def obter_mapeamento_dinamico(caminho_mkv):
    """
    ffprobe para ler as faixas do filme em JSON e retorna
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
    pasta_saida = os.path.join(diretorio_filmes, "Convertidos")
    os.makedirs(pasta_saida, exist_ok=True)

    for arquivo in os.listdir(diretorio_filmes):
        if arquivo.lower().endswith(".mkv"):
            caminho_mkv = os.path.join(diretorio_filmes, arquivo)
            novo_nome = arquivo.rsplit('.', 1)[0] + ".mp4"
            
            caminho_mp4 = os.path.join(pasta_saida, novo_nome)
            
            if os.path.exists(caminho_mp4):
                print(f"O arquivo {novo_nome} já existe na pasta Convertidos. Pulando...")
                continue
                
            print(f"\nAnalisando faixas de mídia para: {arquivo}")
            argumentos_map = obter_mapeamento_dinamico(caminho_mkv)
            
            print(f"\n--------------------------------------------------------------")
            print(f"Iniciando conversão: {arquivo} -> {novo_nome}")
            print(f"--------------------------------------------------------------\n")
            
            comando = [
                "ffmpeg",
                "-i", caminho_mkv,
                *argumentos_map,
                "-c:v", "libx264",
                "-preset", "fast",           
                "-crf", "26",                # Comprime baseado na cena
                "-c:a", "aac",
                "-ac", "2",                  # Força Stereo
                "-b:a", "128k",              
                "-c:s", "mov_text",
                caminho_mp4
            ]
            
            try:                
                subprocess.run(comando, check=True)
                print(f"\n--------------------------------------------------------------")
                print(f"✅ Sucesso: {novo_nome} salvo em /Convertidos!\n")
                print(f"--------------------------------------------------------------\n")
                
            except subprocess.CalledProcessError:
                print(f"\n❌ Erro ao converter o arquivo: {arquivo}\n")

pasta_dos_filmes = r"C:\Users\Sala\Downloads\Downloads Cassio\TORRENT\Spider-Noir"
converter_para_tv_samsung(pasta_dos_filmes)