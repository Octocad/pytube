from pytubefix import YouTube

def baixar_video(url, path='.', modo='video'):
    try:
        print("Conectando ao YouTube...")
        yt = YouTube(url)

        if modo == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
            print("Baixando apenas o áudio...")
        elif modo == 'video':
            print("\nResoluções disponíveis:")
            for i, s in enumerate(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc(), start=1):
                print(f"{i}. {s.resolution}")

            escolha = int(input("\nEscolha a resolução (número): ")) - 1
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            stream = streams[escolha]
            print(f"Baixando o vídeo em {stream.resolution}...")
        else:
            print("Modo inválido. Escolha 'audio' ou 'video'.")
            return

        stream.download(output_path=path)
        print(f"\nDownload concluído! Arquivo salvo em: {path}")

    except Exception as e:
        print("\nOcorreu um erro:", e)

if __name__ == "__main__":
    link = input("Digite a URL do vídeo do YouTube: ")
    pasta = input("Digite o caminho para salvar (ou deixe vazio para salvar na pasta padrão): ").strip()
    if not pasta:
        pasta = './pytube_videos'

    modo = input("Deseja baixar [video] ou [audio]? ").strip().lower()
    baixar_video(link, pasta, modo)