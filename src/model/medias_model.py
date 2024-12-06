from src.model.conexao_banco import ConexaoBancoDuckdb
from src.model.config_base import Base
import pandas as pd


class Medida:

    def __init__(self):
        self.__db = ConexaoBancoDuckdb()
        self.__db.iniciar_banco()

    def obter_destinos_mais_procurados(self, ano: int, mes: int, sigla_empresa: str):
        sql = """
            SELECT 
                da.municipio as municipio, 
                SUM(ft.ASSENTOS) as total_passageiros
            from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
            INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
            WHERE ft.ANO = %s
            AND ft.MES = %s
            AND ft.EMPRESA = %s
            GROUP BY da.municipio
            order by 2 desc
            LIMIT  10
        """
        tipos = {
            'municipio': 'string',
            'total_passageiros': 'int64'
        }
        parametros = (ano, mes, sigla_empresa)
        try:
            dataframe = pd.read_sql_query(
                sql=sql,
                con=self.__db.obter_conexao(),
                params=parametros,
                dtype=tipos
            )

        finally:
            self.__db.obter_sessao().close()

        return dataframe
