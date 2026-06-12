# importa a biblioteca de conexão com mysql
import mysql.connector


# cria conexão com o banco de dados
def conectar():

    return mysql.connector.connect(

        # endereço do servidor mysql
        host="localhost",

        # usuário do banco
        user="root",

        # senha do banco (altere para a sua senha)
        password="sua_senha_aqui",

        # nome do banco utilizado
        database="oficina_mecanica"
    )
