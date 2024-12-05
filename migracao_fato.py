import os
import pandas as pd

# Lista de caminhos
caminhos = [
    '/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/dados_voos/anac_231215421',
    '/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/docs/dados_voos/anac_231334778'
]

# Lista para armazenar todos os DataFrames
dataframes = []

# Iterar pelos caminhos e arquivos
for caminho in caminhos:
    arquivos = os.listdir(caminho)
    for arquivo in arquivos:
        # Ler o arquivo CSV
        df = pd.read_csv(
            os.path.join(caminho, arquivo), sep=';'
        )

        # Criar a coluna 'ano_mes'
        df['ano_mes'] = df['ANO'].astype(str) + '-' + df['MES'].astype(str)

        # Selecionar as colunas desejadas
        df = df[['ano_mes', 'ANO', 'MES', 'ORIGEM',
                 'DESTINO', 'TARIFA', 'ASSENTOS']]

        # Adicionar o DataFrame à lista
        dataframes.append(df)


df_concatenado = pd.concat(dataframes, ignore_index=True)

df_concatenado.to_csv('docs/fato_reformulado.csv',
                      index=False, sep=';', encoding='ISO-8859-1')
