import pandas as pd
import psycopg2
from utils.metricsFunctions import Metrics

class Init_bd:
    
    def __init__(self):
        pass

    def bd_configuration(self, dataFrame: pd.DataFrame):
        
        metric = Metrics()
        
        conn = None
        
        try:
            # Conecting to postgreSQL with psycopg2 conector
            conn = psycopg2.connect(
                        host="127.0.0.1",
                        dbname="vendas",
                        user="postgres",
                        password="postgres",
                        port="5432")

            cur = conn.cursor()


            #===========================================================
            #Iniciating cliente table
            #===========================================================
            
            # Creating table if doesnt exists
            create_script = ''' CREATE TABLE IF NOT EXISTS cliente (
                                    id_cliente      INT PRIMARY KEY,
                                    name    VARCHAR(20) NOT NULL) '''
            cur.execute(create_script)

            # Verify if table is empty
            cur.execute("SELECT COUNT(*) FROM cliente")
            count = cur.fetchone()[0]

            # Only inserts if table is empty
            if count == 0:  
                # Obtaining the filtred dataframe
                client_list = metric.client_list_with_id(dataFrame)

                # Using %s for avoid sql injection
                insert_script = "INSERT INTO cliente (id_cliente, name) VALUES (%s, %s)"

                # Loop of insertions
                for index, row in client_list.iterrows():
                    id_val = row['ID']
                    name_val = row['Cliente']

                    # Insert data
                    cur.execute(insert_script, (id_val, name_val))

                # Confirm the transations
                conn.commit()
                print("Dados da tabela cliente inseridos com sucesso!")
            else:
                print("A tabela clientes já contém dados, inserção não realizada.")

            
            #===========================================================
            #Iniciating vendedor table
            #===========================================================

            # Creating table if doesnt exists
            create_script = ''' CREATE TABLE IF NOT EXISTS vendedor (
                                    id_vendedor      INT PRIMARY KEY,
                                    name    VARCHAR(20) NOT NULL,
                                    equipe  VARCHAR(20) NOT NULL) '''
            cur.execute(create_script)

            # Verify if table is empty
            cur.execute("SELECT COUNT(*) FROM vendedor")
            count = cur.fetchone()[0]
            
            if count == 0:  
                # Obtaining the filtred dataframe
                client_list = metric.seller_list_with_id(dataFrame)

                # Using %s for avoid sql injection
                insert_script = "INSERT INTO vendedor (id_vendedor, name, equipe) VALUES (%s, %s, %s)"

                # Loop of insertions
                for index, row in client_list.iterrows():
                    id_val = row['ID']
                    name_val = row['Vendedor']
                    team_val = row['Equipe']

                     # Insert data
                    cur.execute(insert_script, (id_val, name_val, team_val))
                
                # Confirm the transations
                conn.commit()
                print("Dados da tabela vendedor inseridos com sucesso!")
            else:
                print("A tabela vendedor já contém dados, inserção não realizada.")


            



            # Close after the use
            cur.close()
            conn.close()

        except Exception as error:
            print("Erro ao conectar ou inserir dados:", error)
