import pandas as pd
import psycopg2
from utils.metrics_functions import Metrics

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


            #===========================================================
            #Iniciating vendas table
            #===========================================================

            # Creating table if doesnt exists
            create_script = ''' CREATE TABLE IF NOT EXISTS vendas (
                                    id_venda            INT PRIMARY KEY,
                                    id_cliente          INT NOT NULL,
                                    id_vendedor         INT NOT NULL, 
                                    id                  VARCHAR(20) NOT NULL,
                                    categoria           VARCHAR(20) NOT NULL,
                                    data_venda          DATE NOT NULL,
                                    regional            VARCHAR(20) NOT NULL,
                                    tipo                VARCHAR(20) NOT NULL,
                                    valor               NUMERIC(15,2) NOT NULL,
                                    duracao_contrato    INT,
                                    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
                                    CONSTRAINT fk_vendedor FOREIGN KEY (id_vendedor) REFERENCES vendedor(id_vendedor)) '''
            cur.execute(create_script)

            # Verify if table is empty
            cur.execute("SELECT COUNT(*) FROM vendas")
            count = cur.fetchone()[0]
            
            if count == 0:  
                # Obtaining the filtred dataframe
                formated_data = metric.full_formated_sales_dataframe(dataFrame)

                # Using %s for avoid sql injection
                insert_script = """INSERT INTO vendas (id_venda, id_cliente, id_vendedor, id, categoria, data_venda, regional, tipo, valor, duracao_contrato) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                # Loop of insertions in the database
                for index, row in formated_data.iterrows():
                    id_venda = row['id_venda']

                    # Fetching id_cliente from the cliente table for FOREIGN KEY congruence
                    cur.execute("SELECT id_cliente FROM cliente WHERE name = %s", (row["Cliente"],))
                    id_cliente_result = cur.fetchone()
                    id_cliente = id_cliente_result[0] if id_cliente_result else None

                    # Fetching id_vendedor from the vendedor table for FOREIGN KEY congruence
                    cur.execute("SELECT id_vendedor FROM vendedor WHERE name = %s", (row["Vendedor"],))
                    id_vendedor_result = cur.fetchone()
                    id_vendedor = id_vendedor_result[0] if id_vendedor_result else None

                    id = row['ID']
                    categoria = row['Categoria']
                    data_venda = row['Data da Venda']
                    regional = row['Regional']
                    tipo = row['Tipo']
                    valor = row['Valor']
                    duracao_contrato = row['Duração do Contrato (Meses)']

                    # Insert data
                    cur.execute(insert_script, (id_venda, id_cliente, id_vendedor, id, categoria, data_venda, regional, tipo, valor, duracao_contrato))
                
                # Confirm the transactions
                conn.commit()
                print("Dados da tabela vendas inseridos com sucesso!")
            else:
                print("A tabela vendas já contém dados, inserção não realizada.")



            # Close after the use
            cur.close()
            conn.close()

        except Exception as error:
            print("Erro ao conectar ou inserir dados:", error)
