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
    
    print(query_df.to_string(index=False))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Liste a equipe de cada vendedor
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    ''' 
    Query bellow:
    
    Explanation of the query: vendas is renamede with a alias v, this is for associate the columns in vendas called on the SELECT
    and avoid possible mistakes in join, because the table in the join can contain columns with the same name. The same is done 
    
    ''' 
    query = ''' SELECT vr.name AS vendedor, vr.equipe FROM vendas v
                JOIN vendedor vr ON vr.id_vendedor = vr.id_vendedor '''
    cur.execute(query)
    query_result = cur.fetchall()
    
    # creating a dataframe of the query received for a most visual print
    column_names = [desc[0] for desc in cur.description]  # receives the name of the columns stored in cur
    query_df = pd.DataFrame(query_result, columns=column_names)
    
    print(query_df.to_string(index=False))
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Construa uma tabela que avalie trimestralmente o resultado de vendas e plote um gráfico deste histórico
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
    
    
    
    
    
    
    # Close after the use
    cur.close()
    conn.close()


except Exception as error:
    print("Erro ao conectar ou inserir dados:", error)