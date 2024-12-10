from typing import Tuple
import plotly.express as px
import pandas as pd
import streamlit as st


class ViewGrafico:
    def __init__(self):
        self.__altura = 500
        self.__largura = 600
        self.__fonte_tamanho_hover_lavel = 14
        self.__fonte_tamanho_titulo = 14
        self.__cores_turno = {
            'Manhã': 'rgb(255, 223, 0)',  # Amarelo
            'Tarde': 'rgb(255, 87, 34)',   # Laranja
            'Noite': 'rgb(33, 150, 243)'   # Azul
        }

    def gerar_grafico_destinos_procurados(
            self,
            dataframe: pd.DataFrame,
            coluna_x: str,
            coluna_y: str,
            texto: str,
            texto_template: Tuple,
            legenda_x: str,
            legenda_y: str,
            key: int
    ):
        fig = px.bar(
            dataframe,
            y=coluna_y,
            x=coluna_x,
            text=texto,
            category_orders={
                coluna_y: dataframe[coluna_y].tolist()
            }
        )
        fig.update_traces(
            textposition='outside',
            hovertemplate=texto_template,
            width=0.6
        )
        fig.update_layout(
            xaxis_title=legenda_x,
            yaxis_title=legenda_y,
            bargap=0.6,
            width=self.__largura,
            height=self.__altura,
            hoverlabel=dict(
                font_size=self.__fonte_tamanho_hover_lavel,
                font_family="Arial"
            )
        )
        st.plotly_chart(fig, key=key)
