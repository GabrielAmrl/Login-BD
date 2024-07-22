import mysql.connector
import bcrypt
import customtkinter
from PIL import Image, ImageTk  # Importar a biblioteca Pillow para suportar mais formatos de imagem

# Configurações do CustomTkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Função para conectar ao banco de dados MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # substitua pelo seu usuário MySQL
        password="37092331",  # substitua pela sua senha MySQL
        database="login_system"
    )

# Função para registrar um novo usuário
def register():
    username = entry_email.get()
    password = entry_senha.get()

    if username and password:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
            db.commit()
            message_label.configure(text="Usuário registrado com sucesso!", text_color="green")
        except mysql.connector.Error as err:
            message_label.configure(text=f"Erro: {err}", text_color="red")
            db.rollback()
    else:
        message_label.configure(text="Por favor, preencha todos os campos", text_color="yellow")

# Função para fazer login
def login():
    username = entry_email.get()
    password = entry_senha.get()

    if username and password:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                message_label.configure(text="Login bem-sucedido!", text_color="green")
            else:
                message_label.configure(text="Senha incorreta!", text_color="red")
        else:
            message_label.configure(text="Usuário não encontrado!", text_color="red")
    else:
        message_label.configure(text="Por favor, preencha todos os campos", text_color="yellow")

# Função para sair do aplicativo
def on_closing():
    cursor.close()
    db.close()
    janela.destroy()

# Configuração inicial do banco de dados
db = connect_db()
cursor = db.cursor()

# Configuração da interface gráfica
janela = customtkinter.CTk()
janela.geometry("500x300")
janela.title("Login")

# Adicionar favicon usando Pillow
favicon_image = Image.open("perfil1.png")  # Substitua pelo caminho do seu ícone
favicon = ImageTk.PhotoImage(favicon_image)
janela.iconphoto(False, favicon)

# Widgets da interface
texto = customtkinter.CTkLabel(janela, text="Fazer Login", text_color="white")
entry_email = customtkinter.CTkEntry(janela, placeholder_text="Email", placeholder_text_color="lightgray")
entry_senha = customtkinter.CTkEntry(janela, placeholder_text="Senha", show="*", placeholder_text_color="lightgray")
botao_login = customtkinter.CTkButton(janela, text="Login", command=login, fg_color="#007BFF")  # Azul
botao_register = customtkinter.CTkButton(janela, text="Registrar", command=register, fg_color="#FF5733")  # Vermelho
message_label = customtkinter.CTkLabel(janela, text="", text_color="yellow")

# Layout dos widgets
texto.pack(padx=10, pady=10)
entry_email.pack(padx=10, pady=10)
entry_senha.pack(padx=10, pady=10)
botao_login.pack(padx=10, pady=10)
botao_register.pack(padx=10, pady=10)
message_label.pack(padx=10, pady=10)

# Configurar fechamento da janela
janela.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar o loop principal da interface gráfica
janela.mainloop()
