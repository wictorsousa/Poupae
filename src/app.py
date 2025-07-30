import customtkinter as ctk
from tkinter import *
from PIL import Image
import sqlite3
from tkinter import messagebox
from view import cadastrar_novo_usuario, verificar_login, verificar_email_existente 
from main import Dashboard
import sys 
import os

# Função auxiliar para encontrar o caminho dos arquivos
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para o PyInstaller """
    try:
        # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

   
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        
    #configurando a janela principal;
    def  configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()
        
        try:
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="ERRO!!!\nPor favor, preencha todos os campos")
            elif(len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuário deve ser de pelo menos 4 caracteres.")
            
            elif(len(self.username_cadastro) > 25):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuário não pode ter mais de 25 caracteres.")

            elif(len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="A sua senha deve conter pelo menos 4 caracteres.")
            
            elif(len(self.senha_cadastro) > 25):
                messagebox.showwarning(title="Sistema de Login", message="A senha não pode ter mais de 25 caracteres.")

            elif(self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nAs senhas colocadas não são iguais, coloque senhas iguais.")
                
            elif verificar_email_existente(self.email_cadastro):
                messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nEste e-mail já está em uso.")
                
            else:
                cadastrar_novo_usuario((self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
                    
                messagebox.showinfo(title="Sistema de Login", message=f"Parabéns {self.username_cadastro}\nOs seus dados foram cadastrados com sucesso")     
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro no processamento do seu cadastro\nPor favor, tente novamente")

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        
        if not self.username_login or not self.senha_login:
            messagebox.showinfo(title="Sistema de Login", message="Por favor, preencha todos os campos.")
            return

        dados_usuario = verificar_login((self.username_login, self.senha_login))
        
        if dados_usuario:
            
            user_id = dados_usuario[0]
            
            # 1. Fecha a janela de login
            self.destroy()
            
            # 2. Cria e exibe a nova janela do dashboard
            dashboard = Dashboard(user_id=user_id)
            dashboard.mainloop()
        else:
            # Se a função retornou 'None', o usuário ou senha estão incorretos
            messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nUsuário ou senha não encontrados.\nPor favor, verifique os seus dados ou cadastre-se no nosso sistema.")

    def mostrar_senha_login(self):
        if (self.ver_senha_login_var.get() == 1):
            self.senha_login_entry.configure(show="")
        else:
            self.senha_login_entry.configure(show="*")
            
    def mostrar_senha_cadastro(self):
        if (self.ver_senha_cadastro_var.get() == 1):
            self.senha_cadastro_entry.configure(show="")
            self.confirma_senha_entry.configure(show="")
        else:
            self.senha_cadastro_entry.configure(show="*")
            self.confirma_senha_entry.configure(show="*")

    def tela_de_login(self):
        
        #Trabalhando com imagens
        self.img = ctk.CTkImage(light_image=Image.open(resource_path('porco.png')), size=(360, 360)) # Defina o tamanho desejado aqui
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)
        
        #Titulo da plataforma
        self.title = ctk.CTkLabel(self, text="Faça seu login ou cadastre-se\n aqui pra acessar \nos nossos serviços",  font=('Century Gothic ', 18, 'bold'))
        self.title.grid(row=0, column=0, pady=10, padx=10)
        
        #Criar a frame do formulário de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)
        
        #Colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu login", font=('Century Gothic ', 22, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuário...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6")
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)
        
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Digite sua senha...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6", show="*")
        self.senha_login_entry.grid(row=2, column=0, pady=10, padx=10)
        
        self.ver_senha_login_var = ctk.IntVar(value=0)
        self.ver_senha_login = ctk.CTkCheckBox(self.frame_login,text="Clique para ver a senha", font= ('Century Gothic ', 12, 'bold'), corner_radius=20, variable=self.ver_senha_login_var, onvalue=1, offvalue=0, command=self.mostrar_senha_login)
        self.ver_senha_login.grid(row=3, column=0, pady=10, padx=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login, width=300, fg_color="#5381B6", text="Fazer login".upper(), font= ('Century Gothic ', 14, 'bold'), corner_radius=1, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)
        
        self.span = ctk.CTkLabel(self.frame_login, text="Se não possui conta, clique no botão abaixo para poder se \ncadastrar no nosso sistema", font=('Century Gothic ', 12))
        self.span.grid(row=5, column=0, pady=10, padx=10)
        
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="#4C8A69", hover_color="#25744A", text="Fazer cadastro".upper(), font= ('Century Gothic ', 14, 'bold'), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=10, padx=10)
       
    def tela_de_cadastro(self):
        #remover o formulário de login
        self.frame_login.place_forget()
        
        #Frame de formulário de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)
        
        #criando o nosso título
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu Cadastro", font=('Century Gothic ', 22, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        #criar os nossos widgets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6")
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)
        
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email de usuário...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6")
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)
        
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha de usuário...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6", show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)
        
        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirma senha de usuário...", font= ('Century Gothic ', 16, 'bold'), corner_radius=15, border_color="#5381B6", show="*")
        self.confirma_senha_entry.grid(row=4, column=0, pady=5, padx=10)
        
        self.ver_senha_cadastro_var = ctk.IntVar(value=0)
        self.ver_senha_cadastro = ctk.CTkCheckBox(self.frame_cadastro,text="Clique para ver a senha", font= ('Century Gothic ', 12, 'bold'), corner_radius=20, variable=self.ver_senha_cadastro_var, onvalue=1, offvalue=0, command=self.mostrar_senha_cadastro)
        self.ver_senha_cadastro.grid(row=5, column=0, pady=10)
        
        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="#4C8A69", hover_color="#25744A", text="Fazer cadastro".upper(), font= ('Century Gothic ', 14, 'bold'), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)
        
        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="#444", hover_color="#5381B6", text="Voltar ao login".upper(), font= ('Century Gothic ', 14, 'bold'), corner_radius=15, command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, pady=10, padx=10)
    
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)
    
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)

        
    
if __name__=="__main__":
    app = App()
    app.mainloop()