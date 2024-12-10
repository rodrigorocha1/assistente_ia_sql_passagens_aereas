from src.model.medias_model import Medida
import pandas as pd


class Controller:

    def __init__(self):
        self.__medida = Medida()

    def obter_destinos_mais_procurados_mes(self, ano: int, mes: int, empresa: str) -> pd.DataFrame:
        dataframe = self.__medida.obter_destinos_mais_procurados(
            ano=ano,
            mes=mes,
            sigla_empresa=empresa
        )
        return dataframe
