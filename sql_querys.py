import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
from utils.metrics_functions import Metrics




try:

    # Conecting to postgreSQL with psycopg2 conector
    conn = psycopg2.connect(
                host="127.0.0.1",
                dbname="vendas",
                user="postgres",
                password="postgres",
                port="5432")

    cur = conn.cursor()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Liste todas as vendas (ID) e seus respectivos clientes apenas no ano de 2020
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    ''' 
    Query bellow:
    
    Explanation of the query: vendas is renamede with a alias v, this is for associate the columns in vendas called on the SELECT
    and avoid possible mistakes in join, because the table in the join can contain columns with the same name.
    And finnaly, v.id_cliente = c.id_cliente give the guarantee of the righ cliente associatede with his respective id of the 
    FOREIGN KEY
    ''' 
    query = ''' SELECT v.id, v.id_cliente, c.name AS cliente FROM vendas v
                JOIN cliente c ON v.id_cliente = c.id_cliente 
                WHERE EXTRACT(YEAR FROM v.data_venda) = 2020'''
    cur.execute(query)
    query_result = cur.fetchall()
    
    # creating a dataframe of the query received for a most visual print
    column_names = [desc[0] for desc in cur.description]  # receives the name of the columns stored in cur
    query_df = pd.DataFrame(query_result, columns=column_names)
    
    query_df.to_csv("sql_questão_2.txt", sep="\t", index=False, header=True, encoding="utf-8")
    
    print(query_df.to_string(index=False))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Liste a equipe de cada vendedor
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    ''' 
    Query bellow:
    
    Explanation of the query: vendas is renamede with a alias v, this is for associate the columns in vendas called on the SELECT
    and avoid possible mistakes in join, because the table in the join can contain columns with the same name. The same is done 
    
    ''' 
    query = ''' SELECT name AS vendedor, equipe FROM vendedor '''
    cur.execute(query)
    query_result = cur.fetchall()
    
    # creating a dataframe of the query received for a most visual print
    column_names = [desc[0] for desc in cur.description]  # receives the name of the columns stored in cur
    query_df = pd.DataFrame(query_result, columns=column_names)
    
    query_df.to_csv("sql_questão_3.txt", sep="\t", index=False, header=True, encoding="utf-8")
    
    print(query_df.to_string(index=False))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Construa uma tabela que avalie trimestralmente o resultado de vendas e plote um gráfico deste histórico
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
    ''' 
    Query bellow:
    
    
    
    ''' 
    query = ''' SELECT data_venda, valor FROM vendas '''
    cur.execute(query)
    query_result = cur.fetchall()
    
    # creating a dataframe of the query received for a most visual print
    column_names = [desc[0] for desc in cur.description]  # receives the name of the columns stored in cur
    query_df = pd.DataFrame(query_result, columns=column_names)
    
    
    # Transforming the data_venda column to a format that pandas can understand
    query_df['data_venda'] = pd.to_datetime(query_df['data_venda'], format='%Y/%m/%d')
    
    # Uses a function of pandas to convert the date to a period of quarter(trimestre em portugues)
    query_df['trimestre'] = query_df['data_venda'].dt.to_period('Q')

    # Quarter agroupment and sum of valors
    resultado_trimestral = query_df.groupby('trimestre')['valor'].sum().reset_index()
    
    resultado_trimestral.to_csv("sql_questão_4.txt", sep="\t", index=False, header=True, encoding="utf-8")
    
    # Converting the trimestre collumn to string for the visualization on graph
    resultado_trimestral['trimestre'] = resultado_trimestral['trimestre'].astype(str)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(resultado_trimestral['trimestre'], resultado_trimestral['valor'], marker='o')
    plt.title('Histórico Trimestral de Vendas', fontsize=16)
    plt.xlabel('Trimestre', fontsize=12)
    plt.ylabel('Total Vendido', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Close after the use
    cur.close()
    conn.close()


except Exception as error:
    print("Erro ao conectar ou inserir dados:", error)