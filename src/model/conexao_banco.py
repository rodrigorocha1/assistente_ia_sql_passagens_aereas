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
        self.__engine = create_engine(
            self.__DATABASE_URL,
            echo=False,
            isolation_level='AUTOCOMMIT',
            connect_args={'timeout': 30}
        )

        self.__session_local = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.__engine
        )

    def obter_sessao(self) -> Session:
        session = self.__session_local()
        try:
            return session
        except Exception:
            session.rollback()
            raise

    def iniciar_banco(self):
        Base.metadata.create_all(bind=self.__engine)
