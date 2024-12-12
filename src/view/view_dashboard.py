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
            col1, col2, col3 = st.columns(3)
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
                    horizontal=True,
                    key=1
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    ),
                    key=2
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
                    ),
                    key=3
                )
                dataframe = self.__controler.obter_destinos_mais_procurados_mes(
                    ano=ano,
                    mes=int(mes.split('-')[0]),
                    empresa=empresa.split('-')[0]
                )

                tab_tabela, tab_grafico = st.tabs(['Tabela', 'Grafico'])
                with tab_grafico:
                    self.__grafico.gerar_grafico_destinos_procurados(
                        dataframe=dataframe,
                        coluna_x='municipio',
                        coluna_y='total_passageiros',
                        texto='total_passageiros',
                        texto_template=(
                            "<b>Total Passageiros:</b> %{x}<br>"
                            "<b>Município:</b> %{y}<br>"
                            "<extra></extra>"
                        ),
                        key=4,

                        legenda_x='Município',
                        legenda_y='Total de passageiros'

                    )
                with tab_tabela:
                    trofeus = ["🥇", "🥈", "🥉"]
                    for i in range(min(3, len(dataframe))):
                        dataframe.iloc[i,
                                       1] = f"{trofeus[i]} {dataframe.iloc[i, 1]}"
                    st.table(dataframe)

            with col2:
                st.text(
                    'Destinos mais procurados no mês-Por Estado'
                )
                ano = st.radio(
                    'Escolha o ano',
                    (2023, 2024),
                    horizontal=True,
                    key=5
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    ),
                    key=6
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
                    ),
                    key=7
                )

                dataframe = self.__controler.obter_destinos_mais_procurados_mes_por_uf(

                    ano=ano,
                    mes=int(mes.split('-')[0]),
                    empresa=empresa.split('-')[0],
                )

                tab_tabela, tab_grafico = st.tabs(['Tabela', 'Grafico'])

                with tab_grafico:
                    self.__grafico.gerar_grafico_destinos_procurados(
                        dataframe=dataframe,
                        coluna_x='total_passageiros',
                        coluna_y='estado',
                        texto='total_passageiros',
                        texto_template=(
                            "<b>Total Passageiros:</b> %{x}<br>"
                            "<b>Estado:</b> %{y}<br>"
                            "<extra></extra>"
                        ),
                        key=9,

                        legenda_x='Estado',
                        legenda_y='Total de passageiros'
                    )
                with tab_tabela:
                    trofeus = ["🥇", "🥈", "🥉"]
                    for i in range(min(3, len(dataframe))):
                        dataframe.iloc[i,
                                       1] = f"{trofeus[i]} {dataframe.iloc[i, 1]}"
                    st.table(dataframe)

            with col3:
                st.text(
                    'Destinos mais procurados no mês-Total de passageiros por estado'
                )

                ano = st.radio(
                    'Escolha o ano',
                    (2023, 2024),
                    horizontal=True,
                    key=10
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    ),
                    key=11
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
                    ),
                    key=12
                )

                dataframe = self.__controler.obter_estados_destinos_mais_procurados_mes(

                    ano=ano,
                    mes=int(mes.split('-')[0]),
                    sigla_empresa=empresa.split('-')[0]
                )

                tab_tabela, tab_grafico = st.tabs(['Tabela', 'Grafico'])

                with tab_grafico:
                    self.__grafico.gerar_grafico_destinos_procurados(
                        dataframe=dataframe,
                        coluna_x='total_passageiros',
                        coluna_y='estado',
                        texto='total_passageiros',
                        texto_template=(
                            "<b>Total Passageiros:</b> %{x}<br>"
                            "<b>Estado:</b> %{y}<br>"
                            "<extra></extra>"
                        ),
                        key=13,

                        legenda_x='Estado',
                        legenda_y='Total de passageiros'
                    )
                with tab_tabela:
                    trofeus = ["🥇", "🥈", "🥉"]
                    for i in range(min(3, len(dataframe))):
                        dataframe.iloc[i,
                                       1] = f"{trofeus[i]} {dataframe.iloc[i, 1]}"
                    st.table(dataframe)

            # with col4:
            #     st.text(
            #         'Destinos mais procurados no mês-Variação de procura de destino em relação ao mês anterior',
            #     )

    def gerar_layout_receita(self):
        with st.container(border=True):
            col5, col6, col7 = st.columns(3)
            with col5:
                st.text('Receita por destino ')
                ano = st.radio(
                    'Escolha o ano',
                    (2023, 2024),
                    horizontal=True,
                    key=14
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    ),
                    key=15
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
                    ),
                    key=16
                )

                dataframe = self.__controler.obter_receita_destino(
                    ano=ano, mes=int(mes.split('-')[0]), empresa=empresa.split('-')[0])

                self.__grafico.gerar_grafico_destinos_procurados(
                    dataframe=dataframe,
                    coluna_x='FATURAMENTO',
                    coluna_y='DESTINO',
                    texto='FATURAMENTO',
                    texto_template=(
                        "<b>Faturamento:</b> %{x}<br>"
                        "<b>Destino:</b> %{y}<br>"
                        "<extra></extra>"
                    ),
                    key=17,

                    legenda_x='Faturamento',
                    legenda_y='Destino'
                )
            with col6:
                st.text('Receita por origem')
                ano = st.radio(
                    'Escolha o ano',
                    (2023, 2024),
                    horizontal=True,
                    key=18
                )
                mes = st.selectbox(
                    'Escolha o mês',
                    (
                        '1-Janeiro', '2-Fevereiro', '3-Março', '4-Abril', '5-Maio', '6-Junho', '7-Julho', '8-Agosto', '9-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'
                    ),
                    key=19
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
                    ),
                    key=20
                )
                dataframe = self.__controler.obter_receita_origem(
                    ano=ano, mes=int(mes.split('-')[0]), empresa=empresa.split('-')[0]
                )

                self.__grafico.gerar_grafico_destinos_procurados(
                    dataframe=dataframe,
                    coluna_x='FATURAMENTO',
                    coluna_y='ORIGEM',
                    texto='FATURAMENTO',
                    texto_template=(
                        "<b>Faturamento:</b> %{x}<br>"
                        "<b>Origem:</b> %{y}<br>"
                        "<extra></extra>"
                    ),
                    key=21,

                    legenda_x='Faturamento',
                    legenda_y='Origem'
                )
            with col7:
                st.text('Faturamento Acumulado')
                empresa = st.selectbox(
                    'Selecione a empresa',
                    (
                        'CQB-APUÍ TÁXI AÉREO S/A',
                        'ABJ-ATA AEROTÁXI ABAETÉ LTDA.',
                        'AZU-AZUL LINHAS AÉREAS BRASILEIRAS S/A',
                        'GLO-GOL LINHAS AÉREAS S.A. (EX - VRG LINHAS AÉREAS S.A.)',
                        'PTB-PASSAREDO TRANSPORTES AÉREOS S.A.',
                        'TAM-TAM LINHAS AÉREAS S.A.'
                    ),
                    key=22
                )
                dataframe = self.__controler.obter_faturamento_acumulado(
                    empresa=empresa.split('-')[0]
                )
                self.__grafico.gerar_grafico_acumulado(
                    dataframe=dataframe,
                    key=23
                )

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
