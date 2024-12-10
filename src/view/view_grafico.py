import plotly.express as px
import pandas as pd


class ViewGrafico:
    def __init__(self):
        self.__altura = 500
        self.__largura = 800
        self.__fonte_tamanho_hover_lavel = 14
        self.__fonte_tamanho_titulo = 14
        self.__cores_turno = {
            'Manhã': 'rgb(255, 223, 0)',  # Amarelo
            'Tarde': 'rgb(255, 87, 34)',   # Laranja
            'Noite': 'rgb(33, 150, 243)'   # Azul
        }

    def gerar_grafico_destinos_procurados_geral(self, dataframe: pd.DataFrame):
        pass
