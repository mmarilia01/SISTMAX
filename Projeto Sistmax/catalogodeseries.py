import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style

# Função de conexão com o banco de dados
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            password="",
            database="Sistmax"
        )
        return conexao
    except Error as e:
        print(Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET_ALL)
        return None

# Função para adicionar uma nova série
def adicionar_serie():
    try:
        titulo = input("Digite o título da série: ")
        descricao = input("Digite a descrição da série: ")
        categoria = input("Digite a categoria da série (ex: ação, drama): ")
        ano_lancamento = int(input("Digite o ano de lançamento da série: "))
        duracao = int(input("Digite a duração média de cada episódio em minutos: "))
        classificacao = input("Digite a classificação indicativa da série: ")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO conteudos (titulo, descricao, categoria, ano_lancamento, tipo, duracao_minutos, classificacao_indicativa)
                VALUES (%s, %s, %s, %s, 'serie', %s, %s)
            """
            # Passando os 7 parâmetros corretamente
            valores = (titulo, descricao, categoria, ano_lancamento, duracao, classificacao)
            cursor.execute(query, valores)
            conexao.commit()
            print(Fore.GREEN + f"Série '{titulo}' adicionada com sucesso." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar série: {erro}" + Style.RESET_ALL)

# Função para listar todas as séries
def listar_series():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM conteudos WHERE tipo = 'serie'")
            series = cursor.fetchall()

            if series:
                print("\nLista de Séries:")
                print(f"{'ID':<5} {'Título':<30} {'Ano':<5} {'Categoria':<15} {'Duração':<10} {'Classificação':<15}")
                for serie in series:
                    # Verifique a quantidade de colunas e ajuste os índices conforme necessário
                    print(f"{serie[0]:<5} {serie[1]:<30} {serie[4]:<5} {serie[3]:<15} {serie[6]:<10} {serie[7]:<15}")
            else:
                print(Fore.RED + "Nenhuma série encontrada." + Style.RESET_ALL)
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar séries: {erro}" + Style.RESET_ALL)

# Função para adicionar um episódio a uma série
def adicionar_episodio():
    try:
        conteudo_id = int(input("Digite o ID da série: "))
        temporada = int(input("Digite o número da temporada: "))
        numero_episodio = int(input("Digite o número do episódio: "))
        titulo = input("Digite o título do episódio: ")
        duracao = int(input("Digite a duração do episódio em minutos: "))
        descricao = input("Digite a descrição do episódio: ")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO episodios (conteudo_id, temporada, numero_episodio, titulo, duracao_minutos, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (conteudo_id, temporada, numero_episodio, titulo, duracao, descricao)
            cursor.execute(query, valores)
            conexao.commit()
            print(Fore.GREEN + f"Episódio '{titulo}' adicionado à série com ID {conteudo_id}." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar episódio: {erro}" + Style.RESET_ALL)

# Função para avaliar uma série
def avaliar_serie():
    try:
        usuario_id = int(input("Digite seu ID de usuário: "))
        conteudo_id = int(input("Digite o ID da série a ser avaliada: "))
        nota = float(input("Digite sua nota para a série (de 1 a 10): "))
        comentario = input("Digite seu comentário sobre a série: ")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO avaliacoes (usuario_id, conteudo_id, nota, comentario)
                VALUES (%s, %s, %s, %s)
            """
            valores = (usuario_id, conteudo_id, nota, comentario)
            cursor.execute(query, valores)
            conexao.commit()
            print(Fore.GREEN + f"Série com ID {conteudo_id} avaliada com sucesso." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao avaliar série: {erro}" + Style.RESET_ALL)

# Função para adicionar uma série aos favoritos
def adicionar_favorito():
    try:
        usuario_id = int(input("Digite seu ID de usuário: "))
        conteudo_id = int(input("Digite o ID da série a ser adicionada aos favoritos: "))

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO favoritos (usuario_id, conteudo_id)
                VALUES (%s, %s)
            """
            valores = (usuario_id, conteudo_id)
            cursor.execute(query, valores)
            conexao.commit()
            print(Fore.GREEN + f"Série com ID {conteudo_id} adicionada aos favoritos." + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar aos favoritos: {erro}" + Style.RESET_ALL)

# Função para exibir o menu e interagir com o usuário sem loop contínuo
def exibir_menu():
    print(Fore.MAGENTA + f" ===== Menu Séries =====" + Style.RESET_ALL)
    print("1. Adicionar Série")
    print("2. Listar Séries")
    print("3. Adicionar Episódio")
    print("4. Avaliar Série")
    print("5. Adicionar Série aos Favoritos")
    print("6. Sair")
    opcao = input(Fore.MAGENTA + f"Escolha uma opção (1-6): " + Style.RESET_ALL)

    if opcao == '1':
        adicionar_serie()
    elif opcao == '2':
        listar_series()
    elif opcao == '3':
        adicionar_episodio()
    elif opcao == '4':
        avaliar_serie()
    elif opcao == '5':
        adicionar_favorito()
    elif opcao == '6':
        print(Fore.YELLOW + "Saindo..." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Opção inválida! Por favor, escolha uma opção entre 1 e 6." + Style.RESET_ALL)

# Inicia o menu
exibir_menu()
