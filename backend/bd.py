# Importação do SQLite
import sqlite3 as lite

# Conectando com Banco de Dados
conexao = lite.connect('dados.db')

# Criando tabela de categorias
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")


# Criando tabela de receitas
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor REAL)")


# Criando tabela de gastos
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor REAL)")