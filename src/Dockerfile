# 1. Define a imagem base do Python. A versão 'bullseye' é mais completa e inclui
# bibliotecas de sistema que ajudam com ambientes gráficos.
FROM python:3.9-bullseye

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Atualiza a lista de pacotes e instala o ambiente de execução Tcl/Tk completo.
# Este é o passo chave que corrige o erro 'init.tcl'.
RUN apt-get update && apt-get install -y tk && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# 5. Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o restante do código do seu aplicativo para o contêiner
COPY . .

# 7. Define o comando que será executado quando o contêiner for iniciado
CMD ["python", "app.py"]