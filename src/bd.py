# Importação do SQLite e outras bibliotecas necessárias
import sqlite3 as lite
import os
import sys

# --- Lógica para criar o caminho dinâmico do banco de dados ---

# Determina o caminho base, funcionando tanto no script .py quanto no .exe
if getattr(sys, 'frozen', False):
    # Se estiver rodando como um executável (.exe)
    base_path = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como um script normal (.py)
    base_path = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para a pasta 'data'
data_dir = os.path.join(base_path, 'data')

# Cria a pasta 'data' se ela não existir
os.makedirs(data_dir, exist_ok=True)

# Define o caminho completo para o arquivo do banco de dados
db_path = os.path.join(data_dir, 'dados.db')

# --- Fim da lógica do caminho ---


# Conectando com o Banco de Dados usando o caminho dinâmico
conexao = lite.connect(db_path)

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
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria_Receita(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, user_id INTEGER)")


# Criando tabela de categorias para Gastos
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Categoria_Gasto(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, user_id INTEGER)")

# Criando tabela de receitas
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor REAL, user_id INTEGER)")


# Criando tabela de gastos
with conexao:
    cur = conexao.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor REAL, user_id INTEGER)")