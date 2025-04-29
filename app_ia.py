#Interface aplicada por IA no código do pytube
import customtkinter as ctk
from pytubefix import YouTube
import threading
import os

def iniciar_download():
    # Rodar o download em uma thread separada para não travar a interface
    threading.Thread(target=baixar).start()

def baixar():
    url = entrada_url.get()
    path = entrada_path.get()
    tipo = opcoes.get()

    if not url:
        resultado.configure(text="Por favor, insira a URL.", text_color="red")
        return

    if not path:
        path = '.'

    try:
        yt = YouTube(url, on_progress_callback=atualizar_progresso)
        if tipo == "Áudio":
            stream = yt.streams.filter(only_audio=True).first()
        else:  # Vídeo
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            resolucoes = [s.resolution for s in streams]
            escolha = resolucao_escolhida.get()

            if escolha not in resolucoes:
                resultado.configure(text="Resolução inválida.", text_color="red")
                return

            stream = next(s for s in streams if s.resolution == escolha)

        resultado.configure(text="Baixando...", text_color="yellow")
        stream.download(output_path=path)

        arquivo_nome = stream.default_filename
        resultado.configure(text=f"Download concluído!\nSalvo como: {arquivo_nome}", text_color="green")
        barra_progresso.set(0)

    except Exception as e:
        resultado.configure(text=f"Erro: {str(e)}", text_color="red")
        barra_progresso.set(0)

def atualizar_progresso(stream, chunk, bytes_remaining):
    tamanho_total = stream.filesize
    bytes_baixados = tamanho_total - bytes_remaining
    porcentagem = bytes_baixados / tamanho_total
    barra_progresso.set(porcentagem)

def atualizar_resolucoes():
    url = entrada_url.get()

    if not url:
        resultado.configure(text="Cole a URL para carregar resoluções.", text_color="red")
        return

    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        resolucoes = [s.resolution for s in streams]

        menu_resolucao.configure(values=resolucoes)
        if resolucoes:
            resolucao_escolhida.set(resolucoes[0])  # Define uma resolução padrão
        else:
            resolucao_escolhida.set("")

    except Exception as e:
        resultado.configure(text=f"Erro ao buscar resoluções: {str(e)}", text_color="red")

# Configuração da Janela Principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Downloader - Cadu Edition 🚀")
app.geometry("500x450")

# Widgets
titulo = ctk.CTkLabel(app, text="YouTube Downloader", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(pady=10)

entrada_url = ctk.CTkEntry(app, width=400, placeholder_text="Cole a URL do vídeo aqui")
entrada_url.pack(pady=10)

botao_carregar = ctk.CTkButton(app, text="Carregar Resoluções", command=atualizar_resolucoes)
botao_carregar.pack(pady=5)

resolucao_escolhida = ctk.StringVar()
menu_resolucao = ctk.CTkOptionMenu(app, variable=resolucao_escolhida, values=[])
menu_resolucao.pack(pady=10)

opcoes = ctk.StringVar(value="Vídeo")
menu_opcoes = ctk.CTkOptionMenu(app, variable=opcoes, values=["Vídeo", "Áudio"])
menu_opcoes.pack(pady=10)

entrada_path = ctk.CTkEntry(app, width=400, placeholder_text="Caminho para salvar (opcional)")
entrada_path.pack(pady=10)

botao_baixar = ctk.CTkButton(app, text="Baixar", command=iniciar_download)
botao_baixar.pack(pady=20)

barra_progresso = ctk.CTkProgressBar(app, width=400)
barra_progresso.set(0)
barra_progresso.pack(pady=10)

resultado = ctk.CTkLabel(app, text="")
resultado.pack(pady=10)

# Rodar o app
app.mainloop()
