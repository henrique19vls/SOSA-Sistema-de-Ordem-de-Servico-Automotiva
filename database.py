import mysql.connector


def conectar():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sua_senha_aqui",
        database="oficina_mecanica"
    )
