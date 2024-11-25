import pandas as pd
from decimal import Decimal

class Metrics:
    
    def __init__(self):
        pass
    
    def csv_to_table(self, file_path: str):
        """
        Function description:
        
            Converts a CSV file into a DataFrame table.
        
            Parameters:
            file_path (str): Path to the CSV file.
        
            Returns:
            pd.DataFrame: A pandas DataFrame containing the CSV data or a exception error.
        """
        try:
            
            # Convert the csv to dataFrame format
            data = pd.read_csv(file_path, sep=';')
            return data
        except FileNotFoundError:
            print("Error: The file was not found.")
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    
    def currency_to_float(self, dataFrame: pd.DataFrame):
        """
        Modifyes the "Valor" collum of the dataframe of the DB_teste for a number.
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            The original dataframe with the collum Valor in float.
        """
        
        # Guarantee the type string for Valor to aceppt the string manipulations bellow
        dataFrame['Valor'] =dataFrame['Valor'].astype(str)
        # Conversion of the currency string format to float
        dataFrame['Valor'] = dataFrame['Valor'].str.replace(r"R\$", "", regex=True) \
                         .str.replace(r"\.", "", regex=True) \
                         .str.replace(",", ".", regex=True) \
                         .str.strip() \
                         .apply(Decimal)# More precision because money can't be rounded
                         
        return(dataFrame)
    
    
    def seller_summari(self, dataFrame: pd.DataFrame):
        """
        Summarizes the sum of sellers sales in descending order.
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            Table with a column with seller name and other with sales sum ordened in descending order.
        """
        
        dataFrame = self.currency_to_float(dataFrame)     
        
        summary = dataFrame.groupby('Vendedor')['Valor'].sum().reset_index()

        # Ordenar do maior para o menor
        summary_ordenede = summary.sort_values(by='Valor', ascending=False)

        # Formatar a coluna 'Valor' para a notação de moeda brasileira
        summary_ordenede["Valor"] = summary_ordenede['Valor'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        
        # Exibir a tabela
        return(summary_ordenede)
    
    def formatar_valor(self, valor):
        """
        Format a number to a currency format BRL.
    
        Parameters:
            Number
    
        Returns:
            String in currency BRL
        """

        return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def min_max_sale(self, dataFrame: pd.DataFrame):
        """
        Identifies the client with the biggest and the smallest sale.
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            Prints the biggest and the smalles sale with the respective client.
        """
 
        # Find the biggest sale line of the data frame
        biggest_sale_cliente = dataFrame.loc[dataFrame['Valor'].idxmax()]
        # Find the smallest sale line of the data frame
        smallest_sale_cliente = dataFrame.loc[dataFrame['Valor'].idxmin()]
        
        
       # Applying the currency format
        big_sale = self.formatar_valor(biggest_sale_cliente['Valor'])
        small_sale = self.formatar_valor(smallest_sale_cliente['Valor'])

        big_sale_string = f"Cliente com a maior venda: {biggest_sale_cliente['Cliente']}, Valor: {big_sale}"
        small_sale_string = f"Cliente com a menor venda: {smallest_sale_cliente['Cliente']}, Valor: {small_sale}"
        
        return big_sale_string,small_sale_string
    
    def sale_type_avg(self, dataFrame: pd.DataFrame):
        """
        prints the average sale valor for each type os sale in the dataframe
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            a dataframe with 2 collumns of type and valor
        """
        
        summary = dataFrame.groupby('Tipo')['Valor'].sum().reset_index()
        
        summary["Valor"] = summary["Valor"].apply(self.formatar_valor)

        
        return summary.to_string(index=False)

    def number_of_clients_sales(self, dataFrame: pd.DataFrame):
        """
        Counts the number os sales per client
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            a dataframe with 2 collumns of Client and Número de Vendas
        """
        
        clients_sales = dataFrame["Cliente"].value_counts().reset_index()
        
        clients_sales.columns = ["Cliente", "Número de Vendas"]
        
        return clients_sales
    
    def client_list_with_id(self, dataFrame: pd.DataFrame):
        
        client_list = dataFrame["Cliente"].drop_duplicates()

        # Generate ID initiating in 1
        id_list = list(range(1, len(client_list) + 1))

        df = pd.DataFrame({
            'ID': id_list,
            'Cliente': client_list
        })
        
        return df
    
    def seller_list_with_id(self, dataFrame: pd.DataFrame):
        """
        
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            
        """
        # Remover duplicados mantendo a primeira ocorrência de cada vendedor e sua respectiva equipe
        unique_sellers = dataFrame[['Vendedor', 'Equipe']].drop_duplicates()

        # Gerar os IDs (começando de 1)
        id_list = list(range(1, len(unique_sellers) + 1))

        # Criar um novo DataFrame com IDs, Vendedores e Equipes
        df = pd.DataFrame({
            'ID': id_list,
            'Vendedor': unique_sellers['Vendedor'],
            'Equipe': unique_sellers['Equipe']
        })
        
        return df
    
    def full_formated_sales_dataframe(self, dataFrame: pd.DataFrame):
        """
        
    
        Parameters:
            dataFrame (pd.DataFrame): Receives a pandas dataframe.
    
        Returns:
            
        """
        
        # Data da Venda to the postgre data format AAAA/MM/DD
        dataFrame["Data da Venda"] = pd.to_datetime(dataFrame["Data da Venda"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        
        # Turning month collumn in int
        dataFrame["Duração do Contrato (Meses)"] = dataFrame["Duração do Contrato (Meses)"].apply(int)
        
        
        # Creating an ID for every sale in the dataframe
        id_list = list(range(1, len(dataFrame["ID"]) + 1))
         
        # Adding the new ID collumn for the dataFrame 
         
        dataFrame['id_venda'] = id_list
        return dataFrame