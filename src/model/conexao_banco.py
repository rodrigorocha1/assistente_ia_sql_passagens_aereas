from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.config_base import Base
from sqlalchemy.orm.session import Session
import os


class ConexaoBancoDuckdb:
    def __init__(self):
        self.__CAMINHO_BANCO = os.path.join(
            os.getcwd(),
            'banco',
            'dados_passagens.duckdb'
        )
        self.__DATABASE_URL = 'duckdb:///' + self.__CAMINHO_BANCO
        self.__conexao = create_engine(
            self.__DATABASE_URL,
            echo=False
        )

        self.__Sessao = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.__conexao
        )

    def obter_conexao(self):
        return self.__conexao

    def obter_sessao(self):
        return self.__Sessao()
