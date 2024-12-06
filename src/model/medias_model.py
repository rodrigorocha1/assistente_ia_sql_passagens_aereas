from src.model.conexao_banco import ConexaoBancoDuckdb
from src.model.config_base import Base


class Medida:

    def __init__(self):
        self.__db = ConexaoBancoDuckdb()
        self.__db.iniciar_banco()
