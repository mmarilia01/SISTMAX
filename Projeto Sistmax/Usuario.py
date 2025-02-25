import hashlib
import mysql.connector
from colorama import Fore, Style

# Função para gerar o hash da senha
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

# Função para verificar a senha durante o login
def verificar_senha(senha, hashed_senha):
    return gerar_hash_senha(senha) == hashed_senha

# Conexão com o banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port="3307",# Altere com seu usuário
        password="",  # Atualize a senha do seu banco, se necessário
        database="Sistmax"
    )

# Criar usuário
def criar_usuario():
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    senha = input("Digite a senha do usuário: ")
    tipo_usuario = input("Escolha o plano de usuário (BÁSICO, PRO, PREMIUM): ").upper()

    hashed_senha = gerar_hash_senha(senha)

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)", 
                    (nome, email, hashed_senha, tipo_usuario))
        conn.commit()

        print(Fore.GREEN + "\n===== Usuário Criado com sucesso =====" + Style.RESET_ALL)
    except mysql.connector.Error as err:
        print(f"Erro ao criar usuário: {err}")
    finally:
        conn.close()

# Atualizar usuário (nome, plano e senha)
def atualizar_usuario():
    email = input("Digite o e-mail do usuário a ser atualizado: ")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            novo_nome = input("Digite o novo nome (ou pressione Enter para manter o mesmo): ") or usuario[1]
            novo_tipo_usuario = input("Digite o novo plano de usuário (BÁSICO, PRO, PREMIUM, ou Enter para manter o mesmo): ").upper() or usuario[3]
            
            nova_senha = input("Digite a nova senha (ou pressione Enter para manter a mesma): ")
            hashed_senha = gerar_hash_senha(nova_senha) if nova_senha else usuario[2]

            cursor.execute("UPDATE usuarios SET nome = %s, tipo_usuario = %s, senha = %s WHERE email = %s", 
                           (novo_nome, novo_tipo_usuario, hashed_senha, email))
            conn.commit()

            print(Fore.GREEN + "Usuário atualizado com sucesso!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Usuário não encontrado." + Style.RESET_ALL)
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar usuário: {err}")
    finally:
        conn.close()

# Listar usuários
def listar_usuarios():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, email, tipo_usuario FROM usuarios")
        usuarios = cursor.fetchall()

        if usuarios:
            print(Fore.RED + "\n===== Lista de usuários =====" + Style.RESET_ALL)
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nome: {usuario[1]}, E-mail: {usuario[2]}, Tipo: {usuario[3]}")
        else:
            print(Fore.RED + "\n===== Nenhum usuário encontrado. =====" + Style.RESET_ALL)
    except mysql.connector.Error as err:
        print(f"Erro ao listar usuários: {err}")
    finally:
        conn.close()

# Deletar usuário
def deletar_usuario():
    email = input("Digite o e-mail do usuário a ser deletado: ")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
        conn.commit()

        print(Fore.GREEN + "Usuário deletado com sucesso!" + Style.RESET_ALL)
    except mysql.connector.Error as err:
        print(f"Erro ao deletar usuário: {err}")
    finally:
        conn.close()

# Login de usuário
def login_usuario():
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()

        if resultado:
            hashed_senha = resultado[0]
            if verificar_senha(senha, hashed_senha):
                print(Fore.GREEN + "Login bem-sucedido!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Senha incorreta!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Usuário não encontrado." + Style.RESET_ALL)
    except mysql.connector.Error as err:
        print(f"Erro ao fazer login: {err}")
    finally:
        conn.close()

# Menu principal
def menu():
    while True:
        print(Fore.MAGENTA + "\n===== SISTEMA DE USUÁRIOS =====" + Style.RESET_ALL)
        print("1 - Criar Usuário")
        print("2 - Atualizar Usuário")
        print("3 - Listar Usuários")
        print("4 - Deletar Usuário")
        print("5 - Login")
        print("6 - Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            atualizar_usuario()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "5":
            login_usuario()
        elif opcao == "6":
            print(Fore.YELLOW + "Saindo..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)

# Executando o menu
if __name__ == "__main__":
    menu()
