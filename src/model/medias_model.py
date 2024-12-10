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
