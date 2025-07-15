import customtkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
import sys
import os
from matplotlib.lines import Line2D

from view import (bar_valores, pie_valores_receitas, pie_valores, porcentagem_valor,
                  inserir_categoria_receita, inserir_categoria_gasto,
                  ver_categorias_receitas, ver_categorias_gastos,
                  inserir_receita, inserir_gastos,
                  tabela, deletar_gastos, deletar_receitas)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Dashboard(customtkinter.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        # Cores e fontes
        self.COR_FUNDO = "#F0F2F5"
        self.COR_BRANCA = "#FFFFFF"
        self.COR_TEXTO_CINZA = "#333333"
        self.COR_TEXTO_CLARO = "#888888"
        self.VERDE_CLARO = "#4C8A69"
        self.AZUL = "#5381B6"
        self.VERDE_ESCURO = "#3D6565"
        self.VERDE_PORCENTAGEM = "#4D8D69"
        self.COR_VERMELHA = "#E65353"
        self.COR_VERMELHA_HOVER = "#C14545"
        self.COR_PIZZA_BEGE = "#F7BD76"
        self.COR_PIZZA_VERDE = "#94CBA2"
        self.COR_PIZZA_AZUL = "#5581B6"
        self.lista_cores_pizza = [self.COR_PIZZA_BEGE, self.COR_PIZZA_AZUL, self.COR_PIZZA_VERDE, '#f9766e', '#e285c5', '#8983BF']

        self.FONT_TITULO_APP = ('Arial', 20, 'bold')
        self.FONT_CARD_TITULO = ('Arial', 16)
        self.FONT_VALOR_CARD = ('Arial', 28, 'bold')
        self.FONT_TITULO_SECAO = ('Arial', 13, 'bold')
        self.FONT_LABEL = ('Arial', 12)

        # Config da janela principal
        self.title("Poupaê - Dashboard")
        self.geometry('1280x750')
        self.configure(fg_color=self.COR_FUNDO)
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1, uniform="row_group")
        self.grid_rowconfigure(2, weight=1, uniform="row_group")

        # estilo apenas para o ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=self.COR_BRANCA, foreground=self.COR_TEXTO_CINZA, rowheight=30, fieldbackground=self.COR_BRANCA, borderwidth=0, relief='flat')
        style.map('Treeview', background=[('selected', self.AZUL)])
        style.configure("Treeview.Heading", background=self.AZUL, foreground=self.COR_BRANCA, font=('Arial', 11, 'bold'), relief='flat')
        style.map("Treeview.Heading", background=[('active', self.AZUL)])

        # ícones dos cards
        self.img_renda = customtkinter.CTkImage(light_image=Image.open(resource_path('rendaIcon.png')), size=(40,40))
        self.img_despesa = customtkinter.CTkImage(light_image=Image.open(resource_path('despesasIcon.png')), size=(40,40))
        self.img_saldo = customtkinter.CTkImage(light_image=Image.open(resource_path('walletIcon.png')), size=(40,40))

        # Chamada para construir a interface
        self.setup_ui()
        self.atualizar_tudo()

    def setup_ui(self):
        # Frames princiapis
        self.frameCima = customtkinter.CTkFrame(self, height=60, fg_color=self.COR_BRANCA, corner_radius=10)
        self.frameCima.grid(row=0, column=0, sticky="nsew")
        self.frameMeio = customtkinter.CTkFrame(self, fg_color=self.COR_FUNDO, corner_radius=0)
        self.frameMeio.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        self.frameBaixo = customtkinter.CTkFrame(self, fg_color=self.COR_FUNDO, corner_radius=0)
        self.frameBaixo.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Título no Frame Cima
        self.frameCima.grid_columnconfigure(0, weight=1)
        self.frameCima.grid_rowconfigure(0, weight=1)
        app_img = customtkinter.CTkImage(light_image=Image.open(resource_path('logo.png')), size=(45, 45))
        app_logo = customtkinter.CTkLabel(self.frameCima, image=app_img, text=" Poupaê", compound="left", padx=20, anchor="w", font=self.FONT_TITULO_APP, fg_color="transparent", text_color=self.AZUL)
        app_logo.grid(row=0, column=0, sticky="nsew")
        
        # Estrutura de layout do Frame Meio
        for i in range(3): self.frameMeio.grid_columnconfigure(i, weight=1, uniform="group1")
        self.frameMeio.grid_rowconfigure(1, weight=1)

        self.card_renda = customtkinter.CTkFrame(self.frameMeio, height=100, fg_color=self.VERDE_CLARO, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_renda.grid(row=0, column=0, sticky="nsew", pady=(0,10), padx=(0,5))
        self.card_despesas = customtkinter.CTkFrame(self.frameMeio, height=100, fg_color=self.AZUL, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_despesas.grid(row=0, column=1, sticky="nsew", pady=(0,10), padx=5)
        self.card_saldo = customtkinter.CTkFrame(self.frameMeio, height=100, fg_color=self.VERDE_ESCURO, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_saldo.grid(row=0, column=2, sticky="nsew", pady=(0,10), padx=(5,0))
        self.card_grafico_1 = customtkinter.CTkFrame(self.frameMeio, fg_color=self.COR_BRANCA, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_grafico_1.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self.card_grafico_receitas = customtkinter.CTkFrame(self.frameMeio, fg_color=self.COR_BRANCA, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_grafico_receitas.grid(row=1, column=1, sticky="nsew", padx=5)
        self.card_grafico_2 = customtkinter.CTkFrame(self.frameMeio, fg_color=self.COR_BRANCA, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.card_grafico_2.grid(row=1, column=2, sticky="nsew", padx=(5, 0))

        # Estrutura de 3 colunas para o Frame Meio
        self.frameBaixo.grid_columnconfigure(0, weight=2)
        self.frameBaixo.grid_columnconfigure(1, weight=1)
        self.frameBaixo.grid_columnconfigure(2, weight=1)
        self.frameBaixo.grid_rowconfigure(0, weight=1)
        self.frame_tabela = customtkinter.CTkFrame(self.frameBaixo, fg_color=self.COR_BRANCA, corner_radius=0, border_width=2, border_color=self.COR_TEXTO_CINZA)
        self.frame_tabela.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=10)
        self.frame_operacoes_card = customtkinter.CTkFrame(self.frameBaixo, fg_color=self.COR_BRANCA, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.frame_operacoes_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        self.frame_configuracao_card = customtkinter.CTkFrame(self.frameBaixo, fg_color=self.COR_BRANCA, border_width=2, border_color=self.COR_TEXTO_CINZA, corner_radius=10)
        self.frame_configuracao_card.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=10)
        
        # Painel de Despesas
        l_info_despesa = customtkinter.CTkLabel(self.frame_operacoes_card, text='Adicionar nova despesa', anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_info_despesa.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        l_nova_cat_despesa = customtkinter.CTkLabel(self.frame_operacoes_card, text='Nova Categoria', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_nova_cat_despesa.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.e_nova_categoria_gasto = customtkinter.CTkEntry(self.frame_operacoes_card, width=140, justify='left', corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.e_nova_categoria_gasto.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        botao_add_cat_gasto = customtkinter.CTkButton(self.frame_operacoes_card, text="SALVAR", command=self.adicionar_categoria_gasto_b, fg_color=self.AZUL, hover_color=self.VERDE_CLARO, corner_radius=8)
        botao_add_cat_gasto.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        l_categoria_despesa = customtkinter.CTkLabel(self.frame_operacoes_card, text='Categoria', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_categoria_despesa.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combo_categoria_despesas = customtkinter.CTkComboBox(self.frame_operacoes_card, values=[i[1] for i in ver_categorias_gastos(self.user_id)], font=self.FONT_LABEL, width=140, corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.combo_categoria_despesas.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.combo_categoria_despesas.set("")
        l_data_despesa = customtkinter.CTkLabel(self.frame_operacoes_card, text='Data', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_data_despesa.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.e_cal_despesas = DateEntry(self.frame_operacoes_card, width=12, background=self.AZUL, foreground=self.COR_BRANCA, borderwidth=2, date_pattern='dd/mm/yyyy')
        self.e_cal_despesas.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        l_valor_despesa = customtkinter.CTkLabel(self.frame_operacoes_card, text='Quantia Total', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_valor_despesa.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.e_valor_despesas = customtkinter.CTkEntry(self.frame_operacoes_card, width=140, justify='left', corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.e_valor_despesas.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        botao_inserir_despesas = customtkinter.CTkButton(self.frame_operacoes_card, text="ADICIONAR", command=self.inserir_despesas_b, fg_color=self.AZUL, hover_color=self.VERDE_CLARO, corner_radius=8)
        botao_inserir_despesas.grid(row=6, column=1, padx=10, pady=10, sticky="e")

        # Painel de Receitas
        l_info_receita = customtkinter.CTkLabel(self.frame_configuracao_card, text='Adicionar nova receita', anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_info_receita.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        l_nova_cat_receita = customtkinter.CTkLabel(self.frame_configuracao_card, text='Nova Categoria', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_nova_cat_receita.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.e_nova_categoria_receita = customtkinter.CTkEntry(self.frame_configuracao_card, width=140, justify='left', corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.e_nova_categoria_receita.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        botao_add_cat_receita = customtkinter.CTkButton(self.frame_configuracao_card, text="SALVAR", command=self.adicionar_categoria_receita_b, fg_color=self.AZUL, hover_color=self.VERDE_CLARO, corner_radius=8)
        botao_add_cat_receita.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        l_categoria_receita = customtkinter.CTkLabel(self.frame_configuracao_card, text='Categoria', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_categoria_receita.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combo_categoria_receitas = customtkinter.CTkComboBox(self.frame_configuracao_card, values=[i[1] for i in ver_categorias_receitas(self.user_id)], font=self.FONT_LABEL, width=140, corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.combo_categoria_receitas.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.combo_categoria_receitas.set("")
        l_data_receita = customtkinter.CTkLabel(self.frame_configuracao_card, text='Data', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_data_receita.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.e_cal_receitas = DateEntry(self.frame_configuracao_card, width=12, background=self.AZUL, foreground=self.COR_BRANCA, borderwidth=2, date_pattern='dd/mm/yyyy')
        self.e_cal_receitas.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        l_valor_receita = customtkinter.CTkLabel(self.frame_configuracao_card, text='Quantia Total', anchor="w", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
        l_valor_receita.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.e_valor_receitas = customtkinter.CTkEntry(self.frame_configuracao_card, width=140, justify='left', corner_radius=8, fg_color=self.COR_BRANCA, text_color=self.COR_TEXTO_CINZA)
        self.e_valor_receitas.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        botao_inserir_receitas = customtkinter.CTkButton(self.frame_configuracao_card, text="ADICIONAR", command=self.inserir_receitas_b, fg_color=self.AZUL, hover_color=self.VERDE_CLARO, corner_radius=8)
        botao_inserir_receitas.grid(row=6, column=1, padx=10, pady=10, sticky="e")

    def atualizar_tudo(self):
        self.resumo()
        self.secao_progresso()
        self.grafico_pie_receitas()
        self.grafico_pie()
        self.mostrar_renda()

    def resumo(self):
        valor = bar_valores(self.user_id)
        cards_info = [
            (self.card_renda, "Renda Mensal", self.VERDE_CLARO, valor[0], self.img_renda),
            (self.card_despesas, "Despesas Mensais", self.AZUL, valor[1], self.img_despesa),
            (self.card_saldo, "Saldo da Caixa", self.VERDE_ESCURO, valor[2], self.img_saldo)
        ]
        for card, titulo, cor, v, img in cards_info:
            for widget in card.winfo_children(): widget.destroy()
            card.grid_columnconfigure(0, weight=3)
            card.grid_columnconfigure(1, weight=1)
            card.grid_rowconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=1)
            l_titulo = customtkinter.CTkLabel(card, text=titulo, anchor="sw", font=self.FONT_CARD_TITULO, text_color=self.COR_BRANCA, fg_color="transparent")
            l_titulo.grid(row=0, column=0, sticky="nsew", padx=15, pady=(5,0))
            l_valor = customtkinter.CTkLabel(card, text="R$ {:,.2f}".format(v), anchor="nw", font=self.FONT_VALOR_CARD, text_color=self.COR_BRANCA, fg_color="transparent")
            l_valor.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0,5))
            l_icone = customtkinter.CTkLabel(card, image=img, text="", fg_color="transparent")
            l_icone.grid(row=0, column=1, rowspan=2, sticky="e", padx=15)

    def secao_progresso(self):
        for widget in self.card_grafico_1.winfo_children(): widget.destroy()
        self.card_grafico_1.grid_columnconfigure(1, weight=1)
        l_titulo_progresso = customtkinter.CTkLabel(self.card_grafico_1, text="Resumo Financeiro", anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_titulo_progresso.grid(row=0, column=0, sticky="w", padx=15, pady=(15,10))
        valor_p = porcentagem_valor(self.user_id)[0]
        l_percentual = customtkinter.CTkLabel(self.card_grafico_1, text="{:,.0f}%".format(valor_p), anchor="ne", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_percentual.grid(row=0, column=1, sticky="e", padx=15, pady=(15,10))
        bar = customtkinter.CTkProgressBar(self.card_grafico_1, height=15, progress_color=self.VERDE_PORCENTAGEM, fg_color=self.COR_FUNDO)
        bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)
        bar.set(valor_p / 100)
        valores_legenda = bar_valores(self.user_id)
        legendas = [("Renda", valores_legenda[0]), ("Despesas", valores_legenda[1]), ("Saldo", valores_legenda[2])]
        for i, (texto, valor) in enumerate(legendas):
            l_texto = customtkinter.CTkLabel(self.card_grafico_1, text=texto, anchor="nw", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CLARO)
            l_texto.grid(row=i+2, column=0, sticky="w", padx=15, pady=2)
            l_valor = customtkinter.CTkLabel(self.card_grafico_1, text="R$ {:,.2f}".format(valor), anchor="ne", font=self.FONT_LABEL, text_color=self.COR_TEXTO_CINZA)
            l_valor.grid(row=i+2, column=1, sticky="e", padx=15, pady=2)

    def grafico_pie_receitas(self):
        for widget in self.card_grafico_receitas.winfo_children(): widget.destroy()
        self.card_grafico_receitas.grid_rowconfigure(1, weight=1)
        self.card_grafico_receitas.grid_columnconfigure(0, weight=1)
        l_titulo_pie = customtkinter.CTkLabel(self.card_grafico_receitas, text="Receitas por Categoria", anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_titulo_pie.grid(row=0, column=0, sticky="nw", padx=15, pady=15)
        figura = plt.Figure(dpi=90)
        figura.patch.set_facecolor(self.COR_BRANCA)
        figura.subplots_adjust(right=0.7)
        ax = figura.add_subplot(111)
        ax.set_facecolor(self.COR_BRANCA)
        dados_pie = pie_valores_receitas(self.user_id)
        lista_categorias = dados_pie[0]
        lista_valores = dados_pie[1]
        if not lista_valores: return
        explode = [0.05] * len(lista_categorias)
        ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.4), autopct='%1.0f%%', colors=self.lista_cores_pizza, shadow=False, startangle=90, pctdistance=0.8, textprops={'color': self.COR_BRANCA, 'weight': 'bold'})
        legend_elements = []
        for categoria, cor in zip(lista_categorias, self.lista_cores_pizza):
            legend_elements.append(Line2D([0], [0], marker='o', color='w', label=categoria, markerfacecolor=cor, markersize=12))
        legenda = ax.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, prop={'size': 11})
        for text in legenda.get_texts(): text.set_color(self.COR_TEXTO_CINZA)
        canva_categoria = FigureCanvasTkAgg(figura, master=self.card_grafico_receitas)
        canva_categoria.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def grafico_pie(self):
        for widget in self.card_grafico_2.winfo_children(): widget.destroy()
        self.card_grafico_2.grid_rowconfigure(1, weight=1)
        self.card_grafico_2.grid_columnconfigure(0, weight=1)
        l_titulo_pie = customtkinter.CTkLabel(self.card_grafico_2, text="Despesas por Categoria", anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_titulo_pie.grid(row=0, column=0, sticky="nw", padx=15, pady=15)
        figura = plt.Figure(dpi=90)
        figura.patch.set_facecolor(self.COR_BRANCA)
        ax = figura.add_subplot(111)
        ax.set_facecolor(self.COR_BRANCA)
        figura.subplots_adjust(right=0.7)
        dados_pie = pie_valores(self.user_id)
        lista_categorias = dados_pie[0]
        lista_valores = dados_pie[1]
        if not lista_valores: return
        explode = [0.05] * len(lista_categorias)
        ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.4), autopct='%1.0f%%', colors=self.lista_cores_pizza, shadow=False, startangle=90, pctdistance=0.8, textprops={'color': self.COR_BRANCA, 'weight': 'bold'})
        legend_elements = []
        for categoria, cor in zip(lista_categorias, self.lista_cores_pizza):
            legend_elements.append(Line2D([0], [0], marker='o', color='w', label=categoria, markerfacecolor=cor, markersize=12))
        legenda = ax.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, prop={'size': 11})
        for text in legenda.get_texts(): text.set_color(self.COR_TEXTO_CINZA)
        canva_categoria = FigureCanvasTkAgg(figura, master=self.card_grafico_2)
        canva_categoria.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def mostrar_renda(self):
        # Removido o 'global tree'
        for widget in self.frame_tabela.winfo_children(): widget.destroy()
        
        l_titulo_tabela = customtkinter.CTkLabel(self.frame_tabela, text="Tabela de Transações", anchor="nw", font=self.FONT_TITULO_SECAO, text_color=self.COR_TEXTO_CINZA)
        l_titulo_tabela.pack(side="top", fill="x", padx=10, pady=10)
        
        frame_botoes_tabela = customtkinter.CTkFrame(self.frame_tabela, fg_color="transparent")
        frame_botoes_tabela.pack(side="bottom", fill="x", padx=10, pady=5)
        
        botao_deletar = customtkinter.CTkButton(frame_botoes_tabela, text="DELETAR SELECIONADO", command=self.deletar_dados, fg_color=self.COR_VERMELHA, hover_color=self.COR_VERMELHA_HOVER, corner_radius=8)
        botao_deletar.pack(side="right", pady=5)
        
        tree_frame = customtkinter.CTkFrame(self.frame_tabela, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tabela_head = ['#Id', 'Tipo', 'Categoria', 'Data', 'Quantia']
        # A tabela agora é um atributo da classe: self.tree
        self.tree = ttk.Treeview(tree_frame, selectmode="extended", columns=tabela_head, show="headings", height=4)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        
        hd=["center","center", "center", "center", "center"]
        h=[40, 60, 120, 100, 100]
        n=0
        for col in tabela_head:
            self.tree.heading(col, text=col.title(), anchor="center")
            self.tree.column(col, width=h[n], anchor=hd[n])
            n+=1
        
        lista_itens = tabela(self.user_id)
        # Limpa a tabela antes de inserir novos dados
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in lista_itens:
            self.tree.insert('', 'end', values=item)

    def adicionar_categoria_gasto_b(self):
        nome = self.e_nova_categoria_gasto.get()
        if nome == '':
            messagebox.showerror('Erro', 'Digite o nome da nova categoria de gasto.')
            return
        inserir_categoria_gasto([nome, self.user_id])
        messagebox.showinfo('Sucesso', 'Categoria de gasto adicionada!')
        self.e_nova_categoria_gasto.delete(0, 'end')
        self.combo_categoria_despesas.configure(values=[i[1] for i in ver_categorias_gastos(self.user_id)])
        self.combo_categoria_despesas.set("")

    def adicionar_categoria_receita_b(self):
        nome = self.e_nova_categoria_receita.get()
        if nome == '':
            messagebox.showerror('Erro', 'Digite o nome da nova categoria de receita.')
            return
        inserir_categoria_receita([nome, self.user_id])
        messagebox.showinfo('Sucesso', 'Categoria de receita adicionada!')
        self.e_nova_categoria_receita.delete(0, 'end')
        self.combo_categoria_receitas.configure(values=[i[1] for i in ver_categorias_receitas(self.user_id)])
        self.combo_categoria_receitas.set("")

    def inserir_receitas_b(self):
        nome = self.combo_categoria_receitas.get()
        data = self.e_cal_receitas.get()

        # Validação da Categoria
        categorias_validas = [i[1] for i in ver_categorias_receitas(self.user_id)]
        if nome not in categorias_validas and nome != "":
            messagebox.showerror('Erro de Categoria', f'A categoria "{nome}" não é válida.\n\nPor favor, selecione uma da lista ou crie uma nova na seção "Nova Categoria".')
            return
        # Fim da validação

        try:
            quantia = float(self.e_valor_receitas.get().replace(",", "."))
        except (ValueError, TypeError):
            messagebox.showerror('Erro', 'Digite um valor numérico válido.')
            return
        if nome == '' or data == '' or not quantia:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        inserir_receita([nome, data, quantia, self.user_id])
        self.combo_categoria_receitas.set("")
        self.e_valor_receitas.delete(0, 'end')
        self.atualizar_tudo()

    def inserir_despesas_b(self):
        nome = self.combo_categoria_despesas.get()
        data = self.e_cal_despesas.get()

        # Validação da Categoria
        # 1. Pega a lista de nomes de categorias válidas do banco
        categorias_validas = [i[1] for i in ver_categorias_gastos(self.user_id)]
        
        # 2. Verifica se o que foi digitado/selecionado está na lista
        if nome not in categorias_validas and nome != "":
            messagebox.showerror('Erro de Categoria', f'A categoria "{nome}" não é válida.\n\nPor favor, selecione uma da lista ou crie uma nova na seção "Nova Categoria".')
            return
        # Fim da validação

        try:
            quantia = float(self.e_valor_despesas.get().replace(",", "."))
        except (ValueError, TypeError):
            messagebox.showerror('Erro', 'Digite um valor numérico válido.')
            return
        if nome == '' or data == '' or not quantia:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        inserir_gastos([nome, data, quantia, self.user_id])
        self.combo_categoria_despesas.set("")
        self.e_valor_despesas.delete(0, 'end')
        self.atualizar_tudo()

    def deletar_dados(self):
        try:
            treev_dados = self.tree.focus()
            treev_dicionario = self.tree.item(treev_dados)
            treev_lista = treev_dicionario['values']
            id_registro = treev_lista[0]
            tipo_registro = treev_lista[1]
            if tipo_registro == 'Receita':
                deletar_receitas([id_registro, self.user_id])
            else:
                deletar_gastos([id_registro, self.user_id])
            messagebox.showinfo('Sucesso', 'Registro deletado com sucesso!')
            self.atualizar_tudo()
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos dados da tabela para deletar.')