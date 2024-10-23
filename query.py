# CONEXÃO COM O BANCO DE DADOS E ENVIAR OS DADOS PARA O DASH
#pip install mysql-connector-python


#CONEXÃO
import mysql.connector
import pandas as pd


def conexao(query):
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        port = "3306",
        user = "root",
        password = "senai@134",
        db = "bd_carro"
    )

    dataframe = pd.read_sql(query, conn)
    # Executa a consulta SQL e armazena o resultado em DataFrame


    conn.close()

    return dataframe