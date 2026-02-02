import tkinter as tk
from tkinter import messagebox
import customtkinter 


def show_message_alert(message, title="Automação Concluída"):
    """
    Exibe um alerta 'topmost' (sempre no topo) com CustomTkinter.
    """
    # Define o modo de aparência (opcional, mas recomendado)
    customtkinter.set_appearance_mode("Dark")  # "System", "Dark", "Light"
    
    # Cria a janela principal que servirá de diálogo
    app = customtkinter.CTk()
    app.title(title)

    # Define um tamanho fixo para a janela
    window_width = 380
    window_height = 180
    
    # Calcula a posição para centralizar a janela na tela
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))
    
    app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    app.resizable(False, False) # Impede redimensionamento

    # Coloca a janela no topo de todas as outras
    app.attributes("-topmost", True)

    # --- Widgets dentro da janela ---
    
    # Frame para organizar o conteúdo
    frame = customtkinter.CTkFrame(app, fg_color="transparent")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Mensagem
    label = customtkinter.CTkLabel(
        frame, 
        text=message, 
        font=customtkinter.CTkFont(size=14),
        wraplength=window_width - 60  # Quebra de linha automática
    )
    label.pack(pady=(10, 25), fill="x")

    # Botão OK
    button = customtkinter.CTkButton(
        frame, 
        text="OK", 
        command=app.destroy, # Fecha a janela ao clicar
        width=120,
        font=customtkinter.CTkFont(size=13, weight="bold")
    )
    button.pack(pady=(10, 10))
    # --------------------------------

    # Inicia o loop da janela. O script fica "pausado" aqui
    # até que a janela seja fechada (pelo app.destroy do botão).
    app.mainloop()