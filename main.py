from utils.metricsFunctions import Metrics
from bd_initiation import Init_bd

metrics = Metrics()

# Saving the csv in a panads dataframe
dataFrame = metrics.csv_to_table("/home/brito/Documentos/desenvolvimento/Recrutamento Triggo/desafio-sql/DB_Teste.csv")




ordened_sales = metrics.seller_summari(dataFrame)

print() 
print("==== Tabela sumarizando o valor total vendido por cada vendedor e dispondo decrescentemente ====")
print() 

print(ordened_sales.to_string(index=False))

print()
print("================================================================================================")

print() 
print("======================= Clientes responsáveis pela maior e menor venda =========================")
print()

var1, var2 = metrics.min_max_sale(dataFrame)

print(var1)
print(var2)

print()
print("================================================================================================") 

print() 
print("======================================= média de venda =========================================")
print()

print(metrics.sale_type_avg(dataFrame))

print()
print("================================================================================================") 

print() 
print("================================= Numero de vendas por cliente =================================")
print()

print(metrics.number_of_clients_sales(dataFrame))

print()
print("================================================================================================")



bd = Init_bd()

# Reusing the manipuled dataFrame to create the dataBase onm postgrew with valor in number format 
bd.bd_configuration(dataFrame)