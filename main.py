from utils.metrics_functions import Metrics
from bd_initiation import Init_bd

metrics = Metrics()

# Saving the csv in a panads dataframe
dataFrame = metrics.csv_to_table("/home/brito/Documentos/desenvolvimento/Recrutamento Triggo/desafio-sql/DB_Teste.csv")




ordened_sales = metrics.seller_summari(dataFrame)

print() 
print("==== Tabela sumarizando o valor total vendido por cada vendedor e dispondo decrescentemente ====")
print() 

ordened_sales.to_csv("python_questão_1.txt", sep="\t", index=False, header=True, encoding="utf-8")

print(ordened_sales.to_string(index=False))


print()
print("================================================================================================")

print() 
print("======================= Clientes responsáveis pela maior e menor venda =========================")
print()

var1, var2 = metrics.min_max_sale(dataFrame)

min_max_sale_list = [var1, var2]

with open("python_questão_2.txt", "a", encoding="utf-8") as f:
    for item in min_max_sale_list:
        f.write(item + "\n")


print(var1)
print(var2)

print()
print("================================================================================================") 

print() 
print("======================================= média por tipo de venda =========================================")
print()

type_sale_avg = metrics.sale_type_avg(dataFrame)

with open("python_questão_3.txt", "w", encoding="utf-8") as f:
    f.write(type_sale_avg)

print(type_sale_avg)


print()
print("================================================================================================") 

print() 
print("================================= Numero de vendas por cliente =================================")
print()

number_sales = metrics.number_of_clients_sales(dataFrame)

number_sales.to_csv("python_questão_4.txt", sep="\t", index=False, header=True, encoding="utf-8")



print(number_sales)

print()
print("================================================================================================")



bd = Init_bd()

# Reusing the manipuled dataFrame to create the dataBase onm postgrew with valor in number format 
bd.bd_configuration(dataFrame)