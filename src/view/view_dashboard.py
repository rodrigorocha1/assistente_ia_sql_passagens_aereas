import streamlit as st
from src.view.view_grafico import ViewGrafico
from src.controller.controller import Controller


class ViewDashboard:
    st.set_page_config(
        page_title='Dashboard dados Voos',
        layout='wide',

    )

    def __init__(self):
        self.__grafico = ViewGrafico()
        self.__controler = Controller()

    def gerar_layout_receita_origem(self):
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    """
                    <h4 style='font-size:16px; margin:0; text-align: center;'>Destinos mais procurados no mês</h4>
                    """,
                    unsafe_allow_html=True,
                )
                ano = st.radio(
                    'Escolha o ano',
                    (2023, 2024),
                    horizontal=True
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    )
                )

                empresa = st.selectbox(
                    'Selecione a empresa',
                    (
                        'CQB-APUÍ TÁXI AÉREO S/A',
                        'ABJ-ATA AEROTÁXI ABAETÉ LTDA.',
                        'AZU-AZUL LINHAS AÉREAS BRASILEIRAS S/A',
                        'GLO-GOL LINHAS AÉREAS S.A. (EX - VRG LINHAS AÉREAS S.A.)',
                        'PTB-PASSAREDO TRANSPORTES AÉREOS S.A.',
                        'TAM-TAM LINHAS AÉREAS S.A.'
                    )
                )
                dataframe = self.__controler.obter_destinos_mais_procurados_mes(
                    ano=ano,
                    mes=int(mes.split('-')[0]),
                    empresa=empresa.split('-')[0]
                )

                tab_tabela, tab_grafico = st.tabs(['Tabela', 'Grafico'])
                with tab_tabela:
                    trofeus = ["🥇", "🥈", "🥉"]
                    for i in range(min(3, len(dataframe))):
                        dataframe.iloc[i,
                                       1] = f"{trofeus[i]} {dataframe.iloc[i, 1]}"
                    st.table(dataframe)
                with tab_grafico:
                    self.__grafico.gerar_grafico_destinos_procurados_geral(
                        dataframe=dataframe
                    )
            with col2:
                st.text(
                    'Destinos mais procurados no mês-Por Estado'
                )
            with col3:
                st.text(
                    'Destinos mais procurados no mês-Total de passageiros por estado'
                )
            with col4:
                st.text(
                    'Destinos mais procurados no mês-Variação de procura de destino em relação ao mês anterior',
                )

    def gerar_layout_receita(self):
        with st.container(border=True):
            col5, col6, col7 = st.columns(3)
            with col5:
                st.text('Receita por destino ')
            with col6:
                st.text('Receita por origem')
            with col7:
                st.text('Faturamento Acumulado')

    def gerar_layout_assentos(self):
        with st.container(border=True):
            st.markdown('Total de Assentos Vendidos por rota')
            col1, col2, col3 = st.columns(3)

            with col1:
                st.text('Rota Geral')
            with col2:
                st.text('Período por rota')
            with col3:
                st.text('Taxa de Crescimento de Assentos Vendidos')

    def gerar_layout_participacao_mercado(self):
        with st.container(border=True):
            st.markdown('Participação de Mercado por Origem/Destino')

    def rodar_dashboard(self):
        self.gerar_layout_receita_origem()
        self.gerar_layout_receita()
        self.gerar_layout_assentos()
        self.gerar_layout_participacao_mercado()
