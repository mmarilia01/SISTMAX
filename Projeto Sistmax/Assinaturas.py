import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style
import time
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_animacao(mensagem, segundos=2):
    print(Fore.CYAN + mensagem + Style.RESET_ALL, end='', flush=True)
    for _ in range(segundos):
        time.sleep(0.5)
        print(Fore.CYAN + '.' + Style.RESET_ALL, end='', flush=True)
    print("\n")

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

def listar_planos():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, preco, duracao_meses FROM planos")
            planos = cursor.fetchall()

            limpar_tela()
            print(Fore.YELLOW + "\nPLANOS DISPONÍVEIS" + Style.RESET_ALL)
            print(f"{'ID':<5} {'Nome do Plano':<20} {'Preço':<10} {'Duração (meses)':<20}")
            print("-" * 60)
            for plano in planos:
                print(f"{plano[0]:<5} {plano[1]:<20} R$ {plano[2]:<10} {plano[3]:<20}")

            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar planos: {erro}" + Style.RESET_ALL)

def mudar_assinatura():
    try:
        usuario_id = input("\nDigite o ID do usuário: ").strip()
        listar_planos()
        plano = input("Digite o nome do plano desejado: ").strip()

        # Aqui pode ser feito o processo para mudar a assinatura do usuário
        # Atualizar a tabela de assinaturas usando o nome do plano
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                UPDATE assinaturas 
                SET plano = %s
                WHERE usuario_id = %s AND status = 'ativa'
            """
            cursor.execute(query, (plano, usuario_id))
            conexao.commit()
            carregar_animacao("Mudando assinatura")
            print(Fore.GREEN + f"\nAssinatura para o usuário {usuario_id} foi alterada para o plano '{plano}'!" + Style.RESET_ALL)
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao mudar assinatura: {erro}" + Style.RESET_ALL)


def menu_principal():
    while True:
        limpar_tela()
        print(Fore.MAGENTA + "\n===== SISTEMA DE ASSINATURAS =====" + Style.RESET_ALL)
        print("1 - Listar Planos")
        print("2 - Mudar Assinatura")
        print("3 - Sair")
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            listar_planos()
        elif opcao == '2':
            mudar_assinatura()
        elif opcao == '3':
            carregar_animacao("Saindo do sistema")
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente." + Style.RESET_ALL)
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()
