import math
import pandas as pd
import numpy as np

data = {
    'Comprou': ['NÃO', 'SIM', 'SIM', 'SIM', 'NÃO', 'NÃO', 'SIM', 'NÃO', 'SIM', 'NÃO'],
    'Estado Civil': ["Solteiro", "Casado", "Solteiro", "Divorciado", 'Solteiro', 'Casado', 'Casado', 'Solteiro',
                     'Divorciado', 'Solteiro'],
    'Genero': ['F', 'M', 'F', 'M', 'F', 'M', 'M', 'F', 'M', 'F'],
    'Idade': [22, 35, 28, 40, 23, 30, 36, 27, 50, 24],
    'Renda': [2500, 4000, 3200, 4100, 2700, 3000, 4200, 2900, 4500, 2600],
    'Escolaridade': ['Medio', 'Sup. Completo', 'Sup. Incompleto', 'Sup. Completo', 'Medio', 'Medio', 'Pos Graduação',
                     'Sup. Completo', 'Pos Graduação', 'Sup. Incompleto']
}

df = pd.DataFrame(data)

print("Dataset original:")
print(df)
print("\n")

media_renda = df['Renda'].mean()
print(f"Média da renda: {media_renda}")

def classificar_renda(x):
    if x > media_renda:
        return 'Acima'
    else:
        return 'Abaixo'

df['Renda_Categoria'] = df['Renda'].apply(classificar_renda)

def categorizar_idade(idade):
    if idade < 25:
        return '18-24'
    elif idade < 35:
        return '25-34'
    elif idade < 45:
        return '35-44'
    else:
        return '45+'

df['Idade_Categoria'] = df['Idade'].apply(categorizar_idade)

print("Dataset com categorias adicionadas:")
print(df)
print("\n")


def calcular_entropia(df, classes, coluna_alvo):
    qtd_total = len(df)
    if qtd_total == 0:
        return 0

    soma = 0
    for classe in classes:
        qtd_classe = len(df[df[coluna_alvo] == classe])
        p_i = qtd_classe / qtd_total
        if p_i > 0:
            log = math.log2(p_i)
            soma += p_i * log

    return -1 * soma


def ganho(df, atributo, atributo_classe):
    values = df[atributo].unique()
    qtd_total = len(df)
    classes = df[atributo_classe].unique()

    entropia_total = calcular_entropia(df, classes, atributo_classe)
    soma_ponderada = 0

    for value in values:
        sub_set = df[df[atributo] == value]
        qtd_subset = len(sub_set)
        p_v = qtd_subset / qtd_total
        entropia_subset = calcular_entropia(sub_set, classes, atributo_classe)
        soma_ponderada += p_v * entropia_subset

    return entropia_total - soma_ponderada

colunas = [column for column in df.columns]
colunas.remove('Comprou')
ganhos = {}

for coluna in colunas:
    ganhos[coluna] = ganho(df, coluna, 'Comprou')

print("\nGanho de informação para cada atributo:")
for coluna, valor in ganhos.items():
    print(f"{coluna}: {valor:.4f}")


def decision_tree(df, atributo_classe, attributes, depth=0, max_depth=3):

    if len(df[atributo_classe].unique()) == 1:
        return {"decisao": df[atributo_classe].iloc[0]}

    if len(attributes) == 0 or depth >= max_depth:
        return {"decisao": df[atributo_classe].value_counts().idxmax()}

    ganhos = {attr: ganho(df, attr, atributo_classe) for attr in attributes}

    if all(g <= 0 for g in ganhos.values()):
        return {"decisao": df[atributo_classe].value_counts().idxmax()}

    melhor_atributo = max(ganhos, key=ganhos.get)

    tree = {"atributo": melhor_atributo, "ganho": ganhos[melhor_atributo], "ramos": {}}

    remaining_attributes = [a for a in attributes if a != melhor_atributo]

    for valor in df[melhor_atributo].unique():
        subset = df[df[melhor_atributo] == valor]
        if len(subset) == 0:
            tree["ramos"][valor] = {"decisao": df[atributo_classe].value_counts().idxmax()}
        else:
            tree["ramos"][valor] = decision_tree(subset, atributo_classe, remaining_attributes, depth + 1, max_depth)

    return tree


atributos_para_divisao = ['Estado Civil', 'Genero', 'Idade_Categoria', 'Renda_Categoria', 'Escolaridade']
arvore = decision_tree(df, 'Comprou', atributos_para_divisao)


def print_tree(tree, indent=""):
    if "decisao" in tree:
        print(f"{indent}→ {tree['decisao']}")
        return

    print(f"{indent}[{tree['atributo']}] (Ganho: {tree['ganho']:.4f})")
    for valor, subtree in tree["ramos"].items():
        print(f"{indent}├── {valor}")
        print_tree(subtree, indent + "│   ")


print("\nÁrvore de Decisão Otimizada:")
print_tree(arvore)