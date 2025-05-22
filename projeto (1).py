import pandas as pd
import math

# Função para calcular a entropia de um conjunto
def calcular_entropia(dados, categorias, alvo):
    total = len(dados)
    entropia_total = 0
    for categoria in categorias:
        proporcao = len(dados[dados[alvo] == categoria]) / total
        if proporcao > 0:
            entropia_total -= proporcao * math.log2(proporcao)
    return entropia_total

# Função para calcular o ganho de informação de um atributo
def calcular_ganho(dados, atributo, alvo):
    valores_unicos = dados[atributo].unique()
    categorias_alvo = dados[alvo].unique()
    total = len(dados)

    entropia_condicional = 0

    for valor in valores_unicos:
        subconjunto = dados[dados[atributo] == valor]
        proporcao = len(subconjunto) / total
        entropia_sub = calcular_entropia(subconjunto, categorias_alvo, alvo)
        entropia_condicional += proporcao * entropia_sub

        print(f"Atributo: {atributo}, Valor: {valor}")
        print(f"Proporção: {proporcao:.2f}, Entropia parcial: {entropia_sub:.4f}")
        print(subconjunto, end="\n\n")

    entropia_inicial = calcular_entropia(dados, categorias_alvo, alvo)
    ganho = entropia_inicial - entropia_condicional
    print(f"Ganho de {atributo}: {ganho:.4f}\n{'-'*50}")
    return ganho

# Função para construir a árvore de decisão
def construir_arvore_decisao(dados, atributos, alvo):
    classes_unicas = dados[alvo].unique()

    # Caso base: todos os exemplos têm a mesma classe
    if len(classes_unicas) == 1:
        return classes_unicas[0]

    # Caso base: não há mais atributos
    if not atributos:
        return dados[alvo].mode()[0]

    # Escolhe o atributo com maior ganho de informação
    ganhos = {atrib: calcular_ganho(dados, atrib, alvo) for atrib in atributos}
    melhor_atributo = max(ganhos, key=ganhos.get)
    arvore = {melhor_atributo: {}}

    for valor in dados[melhor_atributo].unique():
        subconjunto = dados[dados[melhor_atributo] == valor]
        atributos_restantes = [a for a in atributos if a != melhor_atributo]
        arvore[melhor_atributo][valor] = construir_arvore_decisao(
            subconjunto, atributos_restantes, alvo
        )

    return arvore

# Função para exibir a árvore
def exibir_arvore(arvore, nivel=""):
    if not isinstance(arvore, dict):
        print(f"{nivel}→ {arvore}")
        return
    for atributo, ramos in arvore.items():
        for valor, subarvore in ramos.items():
            print(f"{nivel}{atributo} = {valor}:")
            exibir_arvore(subarvore, nivel + "    ")


dados_exemplo = {
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

df_dados = pd.DataFrame(dados_exemplo)

atributos_disponiveis = [col for col in df_dados.columns if col != 'Comprou']


print("Calculando árvore de decisão...\n")
arvore_final = construir_arvore_decisao(df_dados, atributos_disponiveis, 'Comprou')

print("\nÁrvore de Decisão Construída:")
exibir_arvore(arvore_final)
