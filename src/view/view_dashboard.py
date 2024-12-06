import streamlit as st


class ViewDashboard:
    st.set_page_config(
        page_title='Dashboard dados Voos',
        layout='wide',

    )

    def gerar_layout_receita_origem(self):
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.text(
                    'Geral'
                )
            with col2:
                st.text(
                    'Por Estado'
                )
            with col3:
                st.text(
                    'Total de passageiros por estado'
                )
            with col4:
                st.text(
                    'Variação de procura de destino em relação ao mês anterior',
                )

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

    def rodar_dashboard(self):
        self.gerar_layout_receita_origem()
        self.gerar_layout_assentos()
