import streamlit as st
import pandas as pd
import plotly.express as px
from utils.metrics_functions import Metrics

metric = Metrics()

# Iniciating the streamlit layout
st.set_page_config(layout="wide")


dataFrame = metric.csv_to_table("/home/brito/Documentos/desenvolvimento/Recrutamento Triggo/desafio-sql/DB_Teste.csv")
dataFrame = metric.currency_to_float(dataFrame)


# Formating the data column for a format aceppted by pandas
dataFrame["Data da Venda"] = pd.to_datetime(dataFrame["Data da Venda"], format='%d/%m/%Y')
dataFrame = dataFrame.sort_values("Data da Venda")

# Applying the correct data format for the application in a new column in database, with formact m-y
dataFrame["Month"] = dataFrame["Data da Venda"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Atribuing the valor of selected month on the streamlit web page for filtring the data by month
month = st.sidebar.selectbox("Filtro para faturamento mensal", dataFrame["Month"].unique())
df_filtered = dataFrame[dataFrame["Month"] == month]

# Creating the columns that will be displayed in the page
col1, col2 = st.columns(2) 
col3= st.columns(1) 
col4= st.columns(1)  


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Building the Valor mensal do faturamento por tipo de venda graph
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fig_prod = px.bar(df_filtered, x="Tipo", y="Valor", 
                  color="Tipo", title="Valor mensal do faturamento por tipo de venda")

col1.plotly_chart(fig_prod, use_container_width=True)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Building Valor mensal do faturamento por vendedor graph
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seller_sale = df_filtered.groupby("Vendedor")[["Valor"]].sum().reset_index()

fig_sale = px.bar(seller_sale, x="Vendedor", y="Valor", color = "Vendedor", 
                   title="Valor mensal do faturamento por vendedor")

col2.plotly_chart(fig_sale, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# building Valor total de vendas por Vendedor table using the result of the querys made in  sql_querys
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seller_avg = pd.read_csv('python_questão_1.txt', sep='\t')


# Transforming the column valor to number
seller_avg = metric.currency_to_float(seller_avg)

seller_avg['Vendedor'] = seller_avg['Vendedor'].str.replace('Vendedor ', '').astype(int)

# Sorting with number format
seller_avg = seller_avg.sort_values(by=["Vendedor"])

# Returning to currency BRL format for better visualisation on graph
seller_avg['Vendedor'] = 'Vendedor ' + seller_avg['Vendedor'].astype(str)

fig_seller_avg = px.bar(seller_avg, x='Vendedor', y='Valor', 
                        title="Valor total de vendas por Vendedor",  
                        labels={'Valor': 'Valor vendido (R$)', 'Vendedor': 'Vendedor'},
                        color='Valor', color_continuous_scale='Blues')

col3[0].plotly_chart(fig_seller_avg, use_container_width=True)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# building Valor total de vendas por trimestre table using the result of the querys made in  sql_querys
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


quarterly_sales = pd.read_csv('sql_questão_4.txt', sep='\t')

fig_quarterly_sales = px.line(quarterly_sales, x='trimestre', y='valor', 
                              title="Valor total de vendas por trimestre",  
                              labels={'valor': 'Valor vendido (R$)', 'trimestre': 'Data'},
                              markers=True,  
                              line_shape='spline',  
                              color_discrete_sequence=['#800080'],
                              ) 

col4[0].plotly_chart(fig_quarterly_sales, use_container_width=True)
