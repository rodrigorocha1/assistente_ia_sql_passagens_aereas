import duckdb
import logging
import time
import pandas as pd


base_aeroporto_privados = pd.read_csv(
    'docs/aeroportos/aeroportos_privados/AerodromosPrivados.csv',
    sep=';')

base_aeroporto_privados.columns

base_aeroporto_privados = base_aeroporto_privados[[
    'Código OACI', 'Nome', 'Município', 'UF']]
# print(base_aeroporto_privados)

base_aeroporto_privados = base_aeroporto_privados.rename(
    columns={
        'Código OACI': 'OACI',
        'Nome': 'NOME',
        'Município': 'MUNICIPIO',

    }
)

base_aeroporto_privados_v2 = pd.read_csv(
    'docs/aeroportos/aeroportos_privados/AerodromosPrivadosv2.csv',
    sep=';', encoding='ISO-8859-1')


base_aeroporto_privados_v2 = base_aeroporto_privados_v2[[
    'Código OACI', 'Nome', 'Município', 'UF']]


base_aeroporto_privados_v2 = base_aeroporto_privados_v2.rename(
    columns={
        'Código OACI': 'OACI',
        'Nome': 'NOME',
        'Município': 'MUNICIPIO',

    }
)

caminho_arquivo = 'docs/aeroportos/aeroportos_publicos/ar_publ_v2.json'

# Carregar o arquivo JSON em um DataFrame
df_aeroportos_publicos_v2 = pd.read_json(caminho_arquivo)


df_aeroportos_publicos_v2 = df_aeroportos_publicos_v2.rename(
    columns={
        'CódigoOACI': 'OACI',
        'Nome': 'NOME',
        'Município': 'MUNICIPIO',
    }
)

df_aeroportos_publicos_v2 = df_aeroportos_publicos_v2[[
    'OACI', 'NOME', 'MUNICIPIO', 'UF']]
print(df_aeroportos_publicos_v2)

df_aeroportos_publicos = pd.read_csv(
    'docs/aeroportos/aeroportos_publicos/aerodromospublicosv1.csv', sep=';')


df_aeroportos_publicos = df_aeroportos_publicos.rename(
    columns={
        'CÓDIGO OACI': 'OACI',
        'Nome': 'NOME',
        'MUNICÍPIO ATENDIDO': 'MUNICIPIO',
    }
)

df_aeroportos_publicos = df_aeroportos_publicos[[
    'OACI', 'NOME', 'MUNICIPIO', 'UF']]


estado_para_sigla = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM',
    'Bahia': 'BA', 'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES',
    'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG', 'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR',
    'Pernambuco': 'PE', 'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC',
    'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO',
    # Incluindo siglas para evitar erros
    'AC': 'AC', 'AL': 'AL', 'AP': 'AP', 'AM': 'AM', 'BA': 'BA', 'CE': 'CE',
    'DF': 'DF', 'ES': 'ES', 'GO': 'GO', 'MA': 'MA', 'MT': 'MT', 'MS': 'MS',
    'MG': 'MG', 'PA': 'PA', 'PB': 'PB', 'PR': 'PR', 'PE': 'PE', 'PI': 'PI',
    'RJ': 'RJ', 'RN': 'RN', 'RS': 'RS', 'RO': 'RO', 'RR': 'RR', 'SC': 'SC',
    'SP': 'SP', 'SE': 'SE', 'TO': 'TO'
}

# Função para padronizar os valores


def padronizar_estado(valor):
    return estado_para_sigla.get(valor, valor)


base_aeroporto_completa = pd.concat(
    [df_aeroportos_publicos, df_aeroportos_publicos_v2], ignore_index=True)

base_aeroporto_completa['UF'] = base_aeroporto_completa['UF'].apply(
    padronizar_estado)
base_aeroporto_completa = base_aeroporto_completa.sort_values(by='OACI')

base_aeroporto_completa = base_aeroporto_completa.dropna()
base_aeroporto_completa = base_aeroporto_completa.drop_duplicates(subset=[
                                                                  'OACI'])
print(base_aeroporto_completa.query('UF == "PA"'))
conn = duckdb.connect('banco/dados_passagens.duckdb')
base_aeroporto_completa.to_sql(
    'dim_aeroporto', conn, if_exists='replace', index=False)
conn.close()
