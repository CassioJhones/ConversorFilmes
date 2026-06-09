import os
import json
import subprocess

def obter_mapeamento_e_tempo(caminho_mkv):
    """
    Usa o ffprobe para ler as faixas do filme e a duração total em JSON.
    Retorna os argumentos '-map' e o tempo de corte exato em segundos.
    """
    comando_probe = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "stream=index,codec_type:stream_tags=language:format=duration", 
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
        
        duracao_str = dados.get("format", {}).get("duration")
        tempo_corte = None
        if duracao_str:
            duracao_segundos = float(duracao_str)

            if duracao_segundos > 180:
                tempo_corte = duracao_segundos - 180
                    
        return argumentos_map, tempo_corte
    except Exception as e:
        print(f"⚠️ Alerta ao analisar com ffprobe (usando mapeamento padrão): {e}")
        return ["-map", "0:v:0", "-map", "0:a:0"], None

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

            argumentos_map, tempo_corte = obter_mapeamento_e_tempo(caminho_mkv)
            
            print(f"\n--------------------------------------------------------------")
            print(f"Iniciando conversão: {arquivo} -> {novo_nome}")
            if tempo_corte:
                print(f"✂️ Corte automático ativo: Removendo os últimos 3 minutos.")
            print(f"--------------------------------------------------------------\n")
            
            comando = [
                "ffmpeg",
                "-i", caminho_mkv,
                *argumentos_map,
                "-c:v", "libx264",
                "-preset", "fast",           
                "-crf", "26",                
                "-c:a", "aac",
                "-ac", "2",                  
                "-b:a", "128k",              
                "-c:s", "mov_text"
            ]
            
            if tempo_corte:
                comando.extend(["-to", str(tempo_corte)])
                
            comando.append(caminho_mp4)
            
            try:                
                subprocess.run(comando, check=True)
                print(f"\n--------------------------------------------------------------")
                print(f"✅ Sucesso: {novo_nome} salvo em /Convertidos!\n")
                print(f"--------------------------------------------------------------\n")
                
            except subprocess.CalledProcessError:
                print(f"\n❌ Erro ao converter o arquivo: {arquivo}\n")

pasta_dos_filmes = r"C:\Users..."
converter_para_tv_samsung(pasta_dos_filmes)

print("\n==============================================================")
print("🎉 TODOS OS ARQUIVOS FORAM PROCESSADOS!")
print("🖥️ O Windows será desligado em 30 segundos.")
print("Para abortar o desligamento, abra o terminal e digite: shutdown /a")
print("==============================================================\n")

os.system("shutdown /s /f /t 30")