# Importação do SQLite
import sqlite3 as lite

# Conectando com Banco de Dados
conexao = lite.connect('dados.db')

# Criando tabela de Usuarios
with conexao:
    cur = conexao.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios(
            Id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL, 
            Confirma_Senha TEXT NOT NULL              
        ); 
    """)

# Criando tabela de categorias para Receitas
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria_Receita(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")


# Criando tabela de categorias para Gastos
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria_Gasto(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

# Criando tabela de receitas
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor REAL)")


# Criando tabela de gastos
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor REAL)")