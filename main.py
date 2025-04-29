from pytubefix import YouTube

def baixar_video(url, path='.'):
    try:
        print("Iniciando o download...")
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        print(f"Download concluído! Vídeo salvo em: {path}")
    except Exception as e:
        print("Ocorreu um erro:", e)

if __name__ == "__main__":
    link = input("Digite a URL do vídeo do YouTube: ")
    pasta = input("Digite o caminho para salvar (ou deixe vazio para salvar na pasta atual): ").strip()
    if not pasta:
        pasta = '.'
    baixar_video(link, pasta)
