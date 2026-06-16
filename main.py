from database import *
from funcoes import *


def perguntar_continuar():

    escolha = input("\nDeseja continuar? (s/n): ").lower()

    if escolha == "s":
        return True

    elif escolha == "n":
        print("Sistema encerrado.")
        return False

    else:
        print("Escolha s para sim ou n para não!")
        return perguntar_continuar()


def menu():

    continuar = True

    while continuar:

        print("\n=== SISTEMA DE ORDEM DE SERVIÇO AUTOMOTIVA ===")
        print("1 - Cadastrar cliente")
        print("2 - Registrar ordem de serviço")
        print("3 - Encaminhar ordem para mecânico")
        print("4 - Concluir ordem de serviço")
        print("5 - Ver histórico")
        print("6 - Ver estatísticas")
        print("0 - Sair")

        op = input("\nEscolha: ")

        if op == "1":
            cadastrar_cliente()
            continuar = perguntar_continuar()

        elif op == "2":
            registrar_ordem()
            continuar = perguntar_continuar()

        elif op == "3":
            encaminhar_ordem()
            continuar = perguntar_continuar()

        elif op == "4":
            concluir_ordem()
            continuar = perguntar_continuar()

        elif op == "5":
            historico_ordens()
            continuar = perguntar_continuar()

        elif op == "6":
            relatorio()
            continuar = perguntar_continuar()

        elif op == "0":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida!")


menu()
