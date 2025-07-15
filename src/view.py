# Importando SQLite
import sqlite3 as lite
import bd
import pandas as pd

# Conectando com Banco de Dados
conexao = lite.connect('dados.db')


# Cadastrar novo usuario no BD
def cadastrar_novo_usuario(i):
    with conexao:
        cur = conexao.cursor()
        query = "INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha) VALUES (?, ?, ?, ?)"
        cur.execute(query, i)

# Verificar login no BD
def verificar_login(i):
    with conexao:
        cur = conexao.cursor()
        query = "SELECT * FROM Usuarios WHERE Username = ? AND Senha = ?"
        cur.execute(query, i)
        return cur.fetchone()


# Funções de Inserção ----------------------------------------------

# Inserindo Categoria de Receita
def inserir_categoria_receita(i):
    with conexao:
        cur = conexao.cursor()
        query = "INSERT INTO Categoria_Receita (nome, user_id) VALUES (?, ?)"
        cur.execute(query, i)

# Inserindo Categoria de Gasto
def inserir_categoria_gasto(i):
    with conexao:
        cur = conexao.cursor()
        query = "INSERT INTO Categoria_Gasto (nome, user_id) VALUES (?, ?)"
        cur.execute(query, i)


# Inserindo Receitas
def inserir_receita(i):

    with conexao:
        cur = conexao.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em, valor, user_id) VALUES (?, ?, ?, ?)"
        cur.execute(query, i)


# Inserindo Gastos
def inserir_gastos(i):

    with conexao:
        cur = conexao.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor, user_id) VALUES (?, ?, ?, ?)"
        cur.execute(query, i)

# Funções para Deletar -----------------------------------------

# Deletar Receitas
def deletar_receitas(i):
    with conexao:
        cur = conexao.cursor()
        query = "DELETE FROM Receitas WHERE id=? AND user_id=?"
        cur.execute(query, i)

# Deletar Gastos
def deletar_gastos(i):
    with conexao:
        cur = conexao.cursor()
        query = "DELETE FROM Gastos WHERE id=? AND user_id=?"
        cur.execute(query, i)

# Funções para ver dados ------------------------------------------

# Ver Categorias de Receita
def ver_categorias_receitas(user_id):
    lista_itens = []
    with conexao:
        cur = conexao.cursor()
        query = "SELECT * FROM Categoria_Receita WHERE user_id = ?"
        cur.execute(query, (user_id,))
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver Categorias de Gasto
def ver_categorias_gastos(user_id):
    lista_itens = []
    with conexao:
        cur = conexao.cursor()
        query = "SELECT * FROM Categoria_Gasto WHERE user_id = ?"
        cur.execute(query, (user_id,))
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver Receitas
def ver_receitas(user_id):
    lista_itens = []

    with conexao:
        cur = conexao.cursor()
        query = ("SELECT * FROM Receitas WHERE user_id = ?")
        cur.execute(query, (user_id,))
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# Ver Gastos
def ver_gastos(user_id):
    lista_itens = []

    with conexao:
        cur = conexao.cursor()
        query = ("SELECT * FROM Gastos WHERE user_id = ?")
        cur.execute(query, (user_id,))
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens


# função para dados da tabela
def tabela(user_id):
    gastos = ver_gastos(user_id)
    receitas = ver_receitas(user_id)

    tabela_lista = []

    for i in gastos:
        # Adicionando a etiqueta "Gasto"
        tabela_lista.append([i[0], 'Gasto', i[1], i[2], i[3]])

    for i in receitas:
        # Adicionando a etiqueta "Receita"
        tabela_lista.append([i[0], 'Receita', i[1], i[2], i[3]])

    return tabela_lista




# função para dados do grafico de barra
def bar_valores(user_id):
    #receita total ----------------
    receitas = ver_receitas(user_id)
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])
    
    receita_total = sum(receitas_lista)

    # despesa total -------------------
    gastos = ver_gastos(user_id)
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])
    
    gasto_total = sum(gastos_lista)

    # Saldo total
    saldo_total = receita_total - gasto_total

    return [receita_total, gasto_total, saldo_total]


# função grafico pie receitas
def pie_valores_receitas(user_id):
    receitas = ver_receitas(user_id)
    tabela_lista = []

    for i in receitas:
        tabela_lista.append(i)
    
    dataframe = pd.DataFrame(tabela_lista, columns = ['id', 'categoria', 'Data', 'valor', 'user_id'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return ([lista_categorias, lista_quantias])


# função grafico pie despesas
def pie_valores(user_id):
    gastos = ver_gastos(user_id)
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)
    
    dataframe = pd.DataFrame(tabela_lista, columns = ['id', 'categoria', 'Data', 'valor', 'user_id'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return ([lista_categorias, lista_quantias])


# função porcentagem
def porcentagem_valor(user_id):
    #receita total ----------------
    receitas = ver_receitas(user_id)
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])
    
    receita_total = sum(receitas_lista)

    # despesa total -------------------
    gastos = ver_gastos(user_id)
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])
    
    gasto_total = sum(gastos_lista)

    # Porcentagem total

    if receita_total == 0:
        return [0, 0] # retorna 0% caso não tenha nada no bd

    porcentagem_total = ((receita_total - gasto_total) / receita_total) * 100

    return [porcentagem_total]