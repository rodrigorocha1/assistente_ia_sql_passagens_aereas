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

    def gerar_grafico_destinos_procurados(self, dataframe: pd.DataFrame, chave: int):
        fig = px.bar(
            dataframe,
            y='municipio',
            x='total_passageiros',
            category_orders={
                "municipio": dataframe['municipio'].tolist()
            },
            text='total_passageiros'
        )
        fig.update_traces(
            textposition='outside',
            hovertemplate=(
                "<b>Total Passageiros:</b> %{x}<br>"
                "<b>Município:</b> %{y}<br>"
                "<extra></extra>"
            ),
            width=0.6
        )
        fig.update_layout(
            xaxis_title='Total de passageiros',
            yaxis_title='Município',
            bargap=0.6,
            width=self.__largura,
            height=self.__altura,
            hoverlabel=dict(
                font_size=self.__fonte_tamanho_hover_lavel,
                font_family="Arial"
            )
        )
        st.plotly_chart(fig, key=chave)
