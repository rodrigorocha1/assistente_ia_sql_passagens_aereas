from src.model.conexao_banco import ConexaoBancoDuckdb
from src.model.config_base import Base
import pandas as pd


class Medida:

    def __init__(self):
        self.__db = ConexaoBancoDuckdb()
        self.__conexao = self.__db.obter_conexao()
        self.__Sessao = self.__db.obter_sessao()
        Base.metadata.create_all(self.__conexao)

    def obter_destinos_mais_procurados(self, ano: int, mes: int, sigla_empresa: str, estado: str = None,  opcao: int = 1) -> pd.DataFrame:
        """_summary_

        Args:
            ano (int): ano  
            mes (int): mês 
            sigla_empresa (str): Sigla da empresa áerea

        Returns:
            pd.DataFrame: Dataframe com o resultado
        """
        if opcao == 1:
            sql = """
                SELECT 
                    da.municipio as municipio, 
                    SUM(ft.ASSENTOS) as total_passageiros
                from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
                INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
                WHERE ft.ANO = ?
                AND ft.MES = ?
                AND ft.EMPRESA = ?
                GROUP BY da.municipio
                order by 2 desc
                LIMIT  10
            """
            tipos = {
                'municipio': 'string',
                'total_passageiros': 'int64'
            }
            parametros = (ano, mes, sigla_empresa)
        else:
            sql = """
                SELECT 
                    da.municipio as municipio , 
                    SUM(ft.ASSENTOS) as total_passageiros
                from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
                INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
                WHERE ft.ANO = ?
                AND ft.MES = ?
                AND ft.EMPRESA = ?
                AND da.UF = ?
                GROUP BY da.municipio
                order by 2 desc;

            """
            tipos = {
                'municipio': 'string',
                'total_passageiros': 'int64'
            }
            parametros = (ano, mes, sigla_empresa, estado)
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

    def obter_destinos_mais_procurados_por_estado(self, ano: int, mes: int, sigla_empresa: str) -> pd.DataFrame:
        """_summary_

        Args:
            ano (int): _description_
            mes (int): _description_
            sigla_empresa (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        sql = """
            SELECT 
                da.UF AS estado, 
                SUM(ft.ASSENTOS) as total_passageiros
            from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
            INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
            WHERE ft.ANO = ?
            AND ft.MES = ?
            AND ft.EMPRESA = ?
            GROUP BY da.UF
            order by 2 desc
            LIMIT 10
        """

        tipos = {
            'estado': 'string',
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

    def obter_estados_mais_procurados(self, ano: int, mes: int, sigla_empresa: str) -> pd.DataFrame:

        sql = """
                SELECT 
                da.UF as UF, 
                SUM(ft.ASSENTOS) as total_passageiros
            from read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
            INNER JOIN main.dim_aeroporto da on da.oaci = ft.DESTINO
            WHERE ft.ANO = ?
            AND ft.MES = ?
            AND ft.EMPRESA = ?
            GROUP BY da.UF
            order by 2 desc 
            LIMIT 10

        """

        tipos = {
            'UF': 'string',
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

    def gerar_dataframe_receita_destino(self, ano: int, mes: int, empresa: str) -> pd.DataFrame:
        sql = """
        SELECT   
            da_destino.MUNICIPIO AS DESTINO,
            ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) AS FATURAMENTO
        FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
        INNER JOIN main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
        WHERE ft.ANO = ?
        AND ft.MES = ?
        AND ft.EMPRESA = ?
        GROUP BY  da_destino.MUNICIPIO
        ORDER BY 2 DESC
        LIMIT 10
        """
        tipos = {
            'DESTINO': 'string',
            'FATURAMENTO': 'float64'
        }
        parametros = (ano, mes, empresa)

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

    def gerar_dataframe_receita_origem(self, ano: int, mes: int, empresa: str) -> pd.DataFrame:
        sql = """
        SELECT   
            da_origem.MUNICIPIO AS ORIGEM,
            ROUND(SUM(ft.TARIFA * FT.ASSENTOS), 2) AS FATURAMENTO
        FROM read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
        INNER JOIN main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
        WHERE ft.ANO = ?
        AND ft.MES = ?
        AND ft.EMPRESA = ?
        GROUP BY  da_origem.MUNICIPIO
        ORDER BY 2 DESC
        LIMIT 10
        """
        tipos = {
            'ORIGEM': 'string',
            'FATURAMENTO': 'float64'
        }
        parametros = (ano, mes, empresa)

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

    def gerar_dataframe_faturamento_acumulado(self, empresa: str):
        sql = """
            WITH faturamento_mensal AS (
            SELECT 
                ft.ANO,
                ft.MES,
                ROUND(SUM(ft.TARIFA * ft.ASSENTOS), 2) AS total_faturamento
            FROM 
                read_csv('/home/rodrigo/Documentos/projetos/assistente_ia_sql_passagens_aereas/banco/fato.csv') ft
            INNER JOIN 
                main.dim_aeroporto da_destino ON da_destino.oaci = ft.DESTINO
            INNER JOIN 
                main.dim_aeroporto da_origem ON da_origem.oaci = ft.ORIGEM
            WHERE  
                ft.EMPRESA = 'GLO'
                AND ft.ANO IN (2023, 2024) -- Inclui dados de ambos os anos
            GROUP BY 
                ft.ANO, ft.MES
        )
        SELECT 
            ANO,
            MES,
            total_faturamento,
            ROUND(SUM(total_faturamento) OVER (PARTITION BY ANO ORDER BY MES ASC), 2) AS faturamento_acumulado -- Calcula acumulado por ano
        FROM 
            faturamento_mensal
        ORDER BY 
            ANO ASC, MES ASC
        """
