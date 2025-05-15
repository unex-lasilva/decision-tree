import math

import pandas as pd

def entropia(data_frame, classes, atributo_classe):
    soma = 0
    qtd_total = len(data_frame[atributo_classe])
    for classe in classes:
        qtd_classe = len(data_frame[data_frame[atributo_classe] == classe])
        p_i = qtd_classe / qtd_total
        if p_i == 0:
            log = 0
        else:
            log = math.log2(p_i)
        item = p_i * log
        soma += item
    return -1 * soma

def ganho(data_frame, atributo, atributo_classe):
    values = data_frame[atributo].unique()
    classes = data_frame[atributo_classe].unique()
    qtd_total = len(data_frame[atributo])
    soma = 0
    for value in values:
        sub_set = data_frame[ data_frame[atributo] == value ]
        qtd_value = len(sub_set)
        p_v = qtd_value / qtd_total
        entropia_subset = entropia(data_frame=sub_set, classes=classes,
                                   atributo_classe=atributo_classe)
        soma += p_v * entropia_subset

        print(f"qtd_value = {qtd_value} pv=  {p_v}")
        print(f"atributo = {atributo}, valor = {value}")
        print(f"entropia = {entropia_subset}")
        print(sub_set)
    print(f"soma = {soma}")

    return entropia(data_frame, classes, atributo_classe) - soma



# Criando o DataFrame
dados = {
    'Gênero': ['F', 'M', 'F', 'M', 'F', 'M', 'M', 'F', 'M', 'F'],
    'Idade': [22, 35, 28, 40, 23, 30, 36, 27, 50, 24],
    'Escolaridade': [
        'Médio', 'Superior completo', 'Superior incompleto', 'Superior completo',
        'Médio', 'Médio', 'Pós-graduação', 'Superior completo',
        'Pós-graduação', 'Superior incompleto'
    ],
    'Estado Civil': [
        'Solteiro', 'Casado', 'Solteiro', 'Divorciado', 'Solteiro',
        'Casado', 'Casado', 'Solteiro', 'Divorciado', 'Solteiro'
    ],
    'Renda (R$)': [2500, 4000, 3200, 4100, 2700, 3000, 4200, 2900, 4500, 2600],
    'Comprou': ['Não', 'Sim', 'Sim', 'Sim', 'Não', 'Não', 'Sim', 'Não', 'Sim', 'Não']
}

df = pd.DataFrame(dados)

# Exibindo o DataFrame
print(df)


print(entropia(data_frame=df, classes=['Não', 'Sim'], atributo_classe='Comprou'))

columns = [column for column in df.columns]
columns.remove('Comprou')

ganhos = {}

for column in columns:
    ganhos[column] = ganho(data_frame=df, atributo=column,
          atributo_classe='Comprou')

print(ganhos)
