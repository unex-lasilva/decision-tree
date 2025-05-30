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
        sub_set = data_frame[data_frame[atributo] == value]
        qtd_value = len(sub_set)
        p_v = qtd_value / qtd_total
        entropia_subset = entropia(data_frame=sub_set, classes=classes, atributo_classe=atributo_classe)
        soma += p_v * entropia_subset
    return entropia(data_frame, classes, atributo_classe) - soma

def atributo_com_maior_ganho(data_frame, atributos, atributo_classe):
    ganhos = {}
    for atributo in atributos:
        ganhos[atributo] = ganho(data_frame, atributo, atributo_classe)
    return max(ganhos, key=ganhos.get)

def id3(data_frame, atributos, atributo_classe):
    classes_unicas = data_frame[atributo_classe].unique()

    if len(classes_unicas) == 1:
        return classes_unicas[0]

    if len(atributos) == 0:
        return data_frame[atributo_classe].mode()[0]

    # Escolhe o melhor atributo com base no ganho de informação
    melhor_atributo = atributo_com_maior_ganho(data_frame, atributos, atributo_classe)

    arvore = {melhor_atributo: {}}

    for valor in data_frame[melhor_atributo].unique():
        subconjunto = data_frame[data_frame[melhor_atributo] == valor]

        if subconjunto.empty:
            arvore[melhor_atributo][valor] = data_frame[atributo_classe].mode()[0]
        else:
            novos_atributos = [a for a in atributos if a != melhor_atributo]
            arvore[melhor_atributo][valor] = id3(subconjunto, novos_atributos, atributo_classe)

    return arvore

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

df['Faixa Etária'] = pd.cut(df['Idade'], bins=[0, 25, 35, 50], labels=['Jovem', 'Adulto', 'Idoso'])
df['Faixa de Renda'] = pd.cut(df['Renda (R$)'], bins=[0, 3000, 4000, 5000], labels=['Baixa', 'Média', 'Alta'])

atributos = ['Gênero', 'Escolaridade', 'Estado Civil', 'Faixa Etária', 'Faixa de Renda']
atributo_classe = 'Comprou'

arvore_decisao = id3(df, atributos, atributo_classe)

import pprint
pprint.pprint(arvore_decisao)
