import mysql.connector
from mysql.connector import Error
from hashlib import sha256
from colorama import Fore, Style
import os
import time

# Função para conectar ao banco de dados
def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            port="3307",# Altere com seu usuário
            password="",  # Altere com sua senha
            database="Sistmax"
        )
        return conn
    except Error as e:
        print(Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET_ALL)
        return None

# Função para gerar o hash da senha
def gerar_hash_senha(senha):
    return sha256(senha.encode('utf-8')).hexdigest()

# Função para verificar a senha
def verificar_senha(email, senha):
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                hashed_senha = resultado[0]
                return gerar_hash_senha(senha) == hashed_senha
            else:
                return False
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao verificar senha: {erro}" + Style.RESET_ALL)
        return False

# Função para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função de login de usuário com limite de tentativas
def login_usuario():
    tentativas = 0
    while tentativas < 3:
        print(Fore.YELLOW + "\n Seja Bem-vindo ao SISTMAX " + Style.RESET_ALL)
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        if verificar_senha(email, senha):
            print(Fore.GREEN + "Login bem-sucedido!" + Style.RESET_ALL)
            menu_principal()
            return
        else:
            tentativas += 1
            print(Fore.RED + f"Credenciais inválidas. Tentativa {tentativas}/3." + Style.RESET_ALL)
    
    print(Fore.RED + "Número máximo de tentativas atingido. Tente novamente mais tarde." + Style.RESET_ALL)
    time.sleep(2)  # Aguarda 2 segundos antes de limpar a tela
  

# Função principal do menu
def menu_principal():
    while True:
        
        print(Fore.MAGENTA + "\n===== Bem-vindo ao Catálogo de Filmes e Séries =====" + Style.RESET_ALL)
        print("1. Adicionar filme")
        print("2. Listar filmes")
        print("3. Adicionar série")
        print("4. Listar séries")
        print("5. Sair")

        escolha = input(Fore.MAGENTA + "Escolha uma opção: " + Style.RESET_ALL)

        if escolha == "1":
            titulo = input("Digite o título do filme: ")
            ano = input("Digite o ano do filme: ")
            genero = input("Digite o gênero do filme: ")
            diretor = input("Digite o nome do diretor: ")
            duracao = input("Digite a duração do filme (em minutos): ")
            adicionar_filme(titulo, ano, genero, diretor, duracao)
        elif escolha == "2":
            listar_filmes()
        elif escolha == "3":
            titulo = input("Digite o título da série: ")
            ano_lancamento = input("Digite o ano de lançamento da série: ")
            categoria = input("Digite a categoria da série: ")
            duracao_minutos = input("Digite a duração de cada episódio da série (em minutos): ")
            classificacao_indicativa = input("Digite a classificação indicativa da série: ")
            adicionar_serie(titulo, ano_lancamento, categoria, duracao_minutos, classificacao_indicativa)
        elif escolha == "4":
            listar_series()
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)

# Função para adicionar filme
def adicionar_filme(titulo, ano, genero, diretor, duracao):
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO filmes (titulo, ano, genero, diretor, duracao) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (titulo, ano, genero, diretor, duracao))
            conexao.commit()
            print(Fore.GREEN + f"Filme '{titulo}' adicionado ao catálogo." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar filme: {erro}" + Style.RESET_ALL)

# Função para listar filmes
def listar_filmes():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM filmes")
            filmes = cursor.fetchall()
            if filmes:
                print(f"\n{'ID':<5} {'Título':<20} {'Ano':<10} {'Gênero':<15} {'Diretor':<20} {'Duração':<10}")
                print("-" * 75)
                for filme in filmes:
                    print(f"{filme[0]:<5} {filme[1]:<20} {filme[2]:<10} {filme[3]:<15} {filme[4]:<20} {filme[5]:<10}")
            else:
                print(Fore.RED + "Nenhum filme no catálogo." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar filmes: {erro}" + Style.RESET_ALL)

# Função para adicionar série
def adicionar_serie(titulo, ano_lancamento, categoria, duracao_minutos, classificacao_indicativa):
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO conteudos (titulo, ano_lancamento, categoria, tipo, duracao_minutos, classificacao_indicativa) VALUES (%s, %s, %s, 'serie', %s, %s)"
            cursor.execute(query, (titulo, ano_lancamento, categoria, duracao_minutos, classificacao_indicativa))
            conexao.commit()
            print(Fore.GREEN + f"Série '{titulo}' adicionada ao catálogo." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar série: {erro}" + Style.RESET_ALL)

# Função para listar séries
def listar_series():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, titulo, ano_lancamento, categoria, classificacao_indicativa FROM conteudos WHERE tipo = 'serie'")
            series = cursor.fetchall()
            if series:
                print(f"\n{'ID':<5} {'Título':<20} {'Ano':<10} {'Categoria':<15} {'Classificação':<10}")
                print("-" * 75)
                for serie in series:
                    print(f"{serie[0]:<5} {serie[1]:<20} {serie[2]:<10} {serie[3]:<15} {serie[4]:<10}")
            else:
                print(Fore.RED + "Nenhuma série no catálogo." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar séries: {erro}" + Style.RESET_ALL)

# Iniciar o login
if __name__ == "__main__":
    login_usuario()
