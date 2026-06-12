# importa a conexão com o banco
from database import *

# importa as funções do sistema
from funcoes import *


# pergunta se o usuário deseja continuar no sistema
def perguntar_continuar():

    escolha = input("\nDeseja continuar? (s/n): ").lower()

    # continua no menu
    if escolha == "s":
        return True

    # encerra o sistema
    elif escolha == "n":
        print("Sistema encerrado.")
        return False

    # impede respostas inválidas
    else:
        print("Escolha s para sim ou n para não!")
        return perguntar_continuar()


# função principal do sistema
def menu():

    continuar = True

    # mantém o menu funcionando
    while continuar:

        # exibe as opções disponíveis
        print("\n=== SISTEMA DE ORDEM DE SERVIÇO AUTOMOTIVA ===")
        print("1 - Cadastrar cliente")
        print("2 - Registrar ordem de serviço")
        print("3 - Encaminhar ordem para mecânico")
        print("4 - Concluir ordem de serviço")
        print("5 - Ver histórico")
        print("6 - Ver estatísticas")
        print("0 - Sair")

        # recebe a opção escolhida
        op = input("\nEscolha: ")

        # cadastra novo cliente
        if op == "1":
            cadastrar_cliente()
            continuar = perguntar_continuar()

        # registra nova ordem de serviço
        elif op == "2":
            registrar_ordem()
            continuar = perguntar_continuar()

        # encaminha ordem para mecânico
        elif op == "3":
            encaminhar_ordem()
            continuar = perguntar_continuar()

        # conclui atendimento
        elif op == "4":
            concluir_ordem()
            continuar = perguntar_continuar()

        # mostra histórico de ordens
        elif op == "5":
            historico_ordens()
            continuar = perguntar_continuar()

        # exibe estatísticas do sistema
        elif op == "6":
            relatorio()
            continuar = perguntar_continuar()

        # encerra o sistema
        elif op == "0":
            print("Sistema encerrado.")
            break

        # impede opções inválidas
        else:
            print("Opção inválida!")


# inicia o sistema
menu()
