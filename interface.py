import customtkinter
from tkinter import messagebox
from datetime import datetime


class SelectionFrame(customtkinter.CTkFrame):
    """
    Frame (conteúdo) que contém a UI para a seleção de ação.
    """
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller # Controlador principal para chamar funções da App

        self.label_instrucao = customtkinter.CTkLabel(
            self,
            text="Selecione a operação desejada:",
            font=customtkinter.CTkFont(size=16)
        )

        self.options = ["Download dos arquivos", "Analisar e renomear arquivos"]
        self.combobox_selection = customtkinter.CTkComboBox(
            self,
            values=self.options,
            width=250
        )
        self.combobox_selection.set(self.options[0])

        self.button_avancar = customtkinter.CTkButton(
            self,
            text="Avançar",
            command=self.proceed, # Chama a função proceed deste frame
            height=40
        )

        # Posiciona os widgets dentro do frame
        self.label_instrucao.pack(pady=(60, 10))
        self.combobox_selection.pack(pady=10)
        self.button_avancar.pack(pady=(15, 20), padx=80, fill="x")

    def proceed(self):
        """Passa a opção selecionada para o controlador principal (a classe App)."""
        selected_option = self.combobox_selection.get()
        self.controller.process_selection(selected_option)


class LoginSiafiFrame(customtkinter.CTkFrame):
    """
    Frame (conteúdo) que contém a UI para o login no SIAFI.
    """
    PAD_X = 30
    PAD_Y_WIDGET = 5
    PAD_Y_WIDGET_GROUP = 15
    
    def __init__(self, master, controller):
        super().__init__(master, corner_radius=15)
        self.controller = controller
        
        self.current_year: str = str(datetime.now().year)

        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """Cria todos os widgets para este frame."""
        validate_command = (self.register(self._only_numeric_input), '%P')
        
        # --- Frame do Título ---
        self.frame_titulo = customtkinter.CTkFrame(self, fg_color="transparent")
        
        self.label_titulo = customtkinter.CTkLabel(
            self.frame_titulo, text="Acesso ao SIAFI", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        
        # --- Botão de Configurações ---
        self.button_settings = customtkinter.CTkButton(
            self.frame_titulo, 
            text="⚙️",
            width=35, 
            height=35, 
            font=customtkinter.CTkFont(size=22),
            fg_color="transparent",
            border_width=0, 
            hover_color="#3e3e3e",
            command=self.controller.navigate_to_settings # Chama o método do controller
        )
        
        # --- Restante dos widgets (SEM Unidade Executora) ---
        self.label_usuario = customtkinter.CTkLabel(self, text="Usuário do SIAFI", anchor="w")
        self.entry_usuario = customtkinter.CTkEntry(self)
        self.label_senha = customtkinter.CTkLabel(self, text="Senha do SIAFI", anchor="w")
        self.entry_senha = customtkinter.CTkEntry(self, show="*")
        self.label_ano = customtkinter.CTkLabel(self, text="Ano de Exercício", anchor="w")
        self.entry_ano = customtkinter.CTkEntry(
            self, validate="key", validatecommand=validate_command
        )
        self.check_ano_atual = customtkinter.CTkCheckBox(
            self, text="Usar Ano Atual", command=self._toggle_ano_atual
        )
        self.button_enviar = customtkinter.CTkButton(self, text="Enviar", command=self.enviar_dados, height=40)

    def _layout_widgets(self):
        """Posiciona os widgets."""
        # --- Layout do Frame do Título ---
        self.frame_titulo.pack(
            fill="x", 
            padx=self.PAD_X - 10, 
            pady=(10, 15)
        )
        self.label_titulo.pack(
            side="left", 
            fill="x", 
            expand=True, 
            padx=(10, 0)
        )
        self.button_settings.pack(
            side="right", 
            fill="none", 
            expand=False
        )
        
        # --- Restante do layout (SEM Unidade Executora) ---
        self.label_usuario.pack(padx=self.PAD_X, pady=(0, 0), fill="x")
        self.entry_usuario.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, self.PAD_Y_WIDGET_GROUP), fill="x")
        self.label_senha.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 0), fill="x")
        self.entry_senha.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, self.PAD_Y_WIDGET_GROUP), fill="x")
        self.label_ano.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET_GROUP, 0), fill="x")
        self.entry_ano.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 10), fill="x")
        self.check_ano_atual.pack(padx=self.PAD_X, pady=self.PAD_Y_WIDGET, anchor="w")
        self.button_enviar.pack(pady=(20, 15), padx=self.PAD_X, fill="x")

    def _toggle_ano_atual(self):
        if self.check_ano_atual.get() == 1:
            self.entry_ano.delete(0, "end")
            self.entry_ano.insert(0, self.current_year)
            self.entry_ano.configure(state="disabled")
        else:
            self.entry_ano.configure(state="normal")
            self.entry_ano.delete(0, "end")

    def _only_numeric_input(self, P: str) -> bool:
        # Esta função agora é usada apenas pelo campo 'Ano'
        return P.isdigit() or P == ""

    def enviar_dados(self):
        usuario_val = self.entry_usuario.get()
        senha_val = self.entry_senha.get()
        ano_val = self.entry_ano.get()

        if not all([usuario_val, senha_val, ano_val]):
            messagebox.showwarning(
                "Campos Obrigatórios", "Por favor, preencha todos os campos antes de enviar."
            )
            return
        if not (ano_val.isdigit() and len(ano_val) == 4):
            messagebox.showwarning(
                "Ano Inválido", "O Ano de Exercício deve ser um número com 4 dígitos."
            )
            return

        # Envia os dados sem a Unidade Executora
        self.controller.on_login_submit(usuario_val, senha_val, ano_val)


class SettingsFrame(customtkinter.CTkFrame):
    """
    Frame (conteúdo) que contém a UI para as configurações
    (Linha inicial, Unidade Executora, etc.)
    """
    PAD_X = 30
    PAD_Y_WIDGET = 5
    
    def __init__(self, master, controller):
        # --- Configuração de Frame normal ---
        super().__init__(master, corner_radius=15)
        self.controller = controller

        # --- Widgets ---
        # Comando de validação apenas para o campo 'linha'
        validate_command = (self.register(self._only_numeric_input), '%P')

        self.label_titulo = customtkinter.CTkLabel(
            self, text="Configurações", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        
        # --- Linha Inicial ---
        self.label_linha = customtkinter.CTkLabel(self, text="Linha Inicial (begin):", anchor="w")
        self.entry_linha = customtkinter.CTkEntry(
            self, validate="key", validatecommand=validate_command
        )
        
        # --- Unidade Executora ---
        self.label_unid_exec = customtkinter.CTkLabel(self, text="Unidade Executora (Padrão: 2070001):", anchor="w")
        # Removemos a validação 'validatecommand' deste campo
        self.entry_unid_exec = customtkinter.CTkEntry(
            self
        )
        
        # --- Botão Salvar ---
        self.button_salvar = customtkinter.CTkButton(
            self, text="Salvar e Voltar", command=self.salvar_e_voltar, height=40
        )

        # --- Layout ---
        self.label_titulo.pack(pady=(15, 20))
        
        self.label_linha.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 0), fill="x")
        self.entry_linha.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 20), fill="x")
        
        self.label_unid_exec.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 0), fill="x")
        self.entry_unid_exec.pack(padx=self.PAD_X, pady=(self.PAD_Y_WIDGET, 20), fill="x")

        self.button_salvar.pack(pady=(15, 20), padx=self.PAD_X, fill="x")

    def _only_numeric_input(self, P: str) -> bool:
        """Permite apenas dígitos ou string vazia."""
        return P.isdigit() or P == ""

    def on_show(self):
        """
        Chamado pelo controller antes de mostrar este frame.
        Carrega os valores atuais nos campos de entrada.
        """
        # Carrega Linha Inicial
        self.entry_linha.delete(0, "end")
        self.entry_linha.insert(0, str(self.controller.begin_line))
        
        # Carrega Unidade Executora
        self.entry_unid_exec.delete(0, "end")
        self.entry_unid_exec.insert(0, str(self.controller.unid_exec))

    def salvar_e_voltar(self):
        """
        Pega ambos os valores e passa para o controller salvar e navegar de volta.
        """
        new_line_value = self.entry_linha.get()
        new_ue_value = self.entry_unid_exec.get()
        
        # O controller fará a validação e a navegação
        self.controller.on_settings_save(new_line_value, new_ue_value)


class Interface(customtkinter.CTk):
    """
    Classe principal da aplicação que gerencia a ÚNICA janela e todos os frames.
    """
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # --- Atributos para guardar os dados finais ---
        self.user: str | None = None
        self.password: str | None = None
        self.exercise_year: str | None = None
        self.begin_line: int = 2 
        self.unid_exec: str = "2070001"
        self.analyze_selected: bool = False

        # --- NOVO ATRIBUTO ---
        # Guarda o nome do frame que está visível no momento
        self.current_frame_name: str | None = None

        self._setup_window("Seleção de Ação", 400, 250)

        # Container principal onde os frames serão empilhados
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SelectionFrame, LoginSiafiFrame, SettingsFrame):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame("SelectionFrame")

        # --- NOVO PROTOCOLO ---
        # Intercepta o clique no "X" e o direciona para nossa função
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

    def show_frame(self, frame_name: str):
        """
        Traz o frame desejado para a frente e chama on_show se existir.
        """
        # --- ATUALIZAÇÃO ---
        # Guarda o nome do frame que estamos prestes a mostrar
        self.current_frame_name = frame_name
        
        frame = self.frames[frame_name]
        
        if hasattr(frame, 'on_show'):
            frame.on_show()
            
        frame.tkraise()

    def process_selection(self, choice: str):
        """
        Decide o que fazer com base na escolha do primeiro frame.
        """
        if choice == "Download dos arquivos":
            self.withdraw() 
            self.show_frame("LoginSiafiFrame") 
            self._setup_window("Login SIAFI", 400, 470) 
            self.deiconify() 
            
        elif choice == "Analisar e renomear arquivos":
            print("Opção 'Analisar e renomear arquivos' selecionada.")
            self.analyze_selected = True
            self.destroy() # Fecha a UI para o script principal continuar
            
        # Removemos o 'else: self.destroy()' porque o _on_window_close
        # agora cuida de fechar a janela na tela de seleção.

    def on_login_submit(self, user, password, year):
        """Recebe os dados do login, armazena e fecha a aplicação."""
        self.user = user
        self.password = password
        self.exercise_year = year
        
        print(f"Login enviado. Usuário: {self.user}, Ano: {self.exercise_year}")
        print(f"Configuração - Linha: {self.begin_line}, Unid.Exec.: {self.unid_exec}")
        
        self.destroy()

    def on_settings_save(self, new_line_value: str, new_ue_value: str):
        """Salva os novos valores de configuração e navega de volta ao Login."""
        
        # Validação da Linha Inicial
        if not new_line_value.isdigit() or int(new_line_value) < 1:
            messagebox.showwarning(
                "Valor Inválido", 
                "A linha inicial deve ser um número inteiro positivo."
            )
            return
            
        # Validação da Unidade Executora foi removida a pedido.
            
        # Sucesso: Salva ambos os valores
        self.begin_line = int(new_line_value)
        # Permite salvar qualquer valor, inclusive vazio, se o usuário desejar
        self.unid_exec = new_ue_value 
        
        # Navega de volta ao login
        self.withdraw()
        self.show_frame("LoginSiafiFrame")
        self._setup_window("Login SIAFI", 400, 470)
        self.deiconify()

    def navigate_to_settings(self):
        """
        Abre o frame de configurações e redimensiona a janela.
        """
        self.withdraw() 
        self.show_frame("SettingsFrame") 
        self._setup_window("Configurações", 400, 370) 
        self.deiconify() 

    # --- NOVO MÉTODO ---
    def _on_window_close(self):
        """
        Manipulador customizado para o botão 'X' da janela.
        Verifica o frame atual antes de decidir se fecha o app
        ou se apenas navega para outra tela.
        """
        # Se estivermos na tela de Configurações, volte ao Login (sem salvar)
        if self.current_frame_name == "SettingsFrame":
            print("Fechando Configurações, voltando ao Login (sem salvar).")
            self.withdraw()
            self.show_frame("LoginSiafiFrame")
            self._setup_window("Login SIAFI", 400, 470)
            self.deiconify()
        else:
            # Em qualquer outra tela (Login, Seleção), feche o app
            print("Fechando a aplicação.")
            self.destroy()

    def _setup_window(self, title: str, width: int, height: int):
        """Configura ou atualiza as propriedades da janela."""
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self._center_window()

    def _center_window(self):
        """Centraliza a janela na tela."""
        self.update_idletasks() 
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
