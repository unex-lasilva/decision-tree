import math
import pandas as pd

# Função para calcular entropia
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

# Função para calcular ganho de informação
def ganho(data_frame, atributo, atributo_classe):
    values = data_frame[atributo].unique()
    classes = data_frame[atributo_classe].unique()
    qtd_total = len(data_frame[atributo])
    soma = 0
    for value in values:
        sub_set = data_frame[data_frame[atributo] == value]
        qtd_value = len(sub_set)
        p_v = qtd_value / qtd_total
        entropia_subset = entropia(data_frame=sub_set, classes=classes,
                                   atributo_classe=atributo_classe)
        soma += p_v * entropia_subset
    return entropia(data_frame, classes, atributo_classe) - soma

# Função para construir a árvore de decisão recursivamente
def construir_arvore(data_frame, atributos, atributo_classe):
    classes = data_frame[atributo_classe].unique()

    # Caso 1: todas as instâncias têm a mesma classe
    if len(classes) == 1:
        return classes[0]

    # Caso 2: não há mais atributos para dividir
    if len(atributos) == 0:
        return data_frame[atributo_classe].mode()[0]

    # Caso geral: escolher o melhor atributo
    ganhos = {atributo: ganho(data_frame, atributo, atributo_classe) for atributo in atributos}
    melhor_atributo = max(ganhos, key=ganhos.get)

    arvore = {melhor_atributo: {}}
    novos_atributos = atributos.copy()
    novos_atributos.remove(melhor_atributo)

    for valor in data_frame[melhor_atributo].unique():
        subset = data_frame[data_frame[melhor_atributo] == valor]
        if subset.empty:
            arvore[melhor_atributo][valor] = data_frame[atributo_classe].mode()[0]
        else:
            arvore[melhor_atributo][valor] = construir_arvore(
                subset, novos_atributos, atributo_classe)
    return arvore

# Função para converter idade em faixas
def categorizar_idade(idade):
    if idade < 25:
        return 'Jovem'
    elif idade < 35:
        return 'Adulto Jovem'
    elif idade < 45:
        return 'Meia Idade'
    else:
        return 'Idoso'

# Dados
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

# Converter idade para categorias
df['Faixa Etária'] = df['Idade'].apply(categorizar_idade)

# Remover coluna original 'Idade'
df = df.drop(columns=['Idade'])

# Mostrar DataFrame atualizado
print("DataFrame atualizado com faixas etárias:\n")
print(df)

# Construir árvore de decisão
atributos = list(df.columns)
atributos.remove('Comprou')  # atributo alvo

arvore_decisao = construir_arvore(df, atributos, 'Comprou')

# Impressão formatada da árvore
import pprint
print("\nÁrvore de Decisão (ID3):\n")
pprint.pprint(arvore_decisao)
