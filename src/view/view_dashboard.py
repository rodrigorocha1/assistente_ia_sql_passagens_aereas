import streamlit as st


class ViewDashboard:
    st.set_page_config(
        page_title='Dashboard dados Voos',
        layout='wide',

    )

    def gerar_layout_receita_origem(self):
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                'Geral',
                'Por Estado',
                'Total de passageiros por estado',
                'Variação de procura de destino em relação ao mês anterior'
            ]
        )
        with tab1:
            st.subheader('Geral')
        with tab2:
            st.subheader('Por Estado')
        with tab3:
            st.subheader('Total de passageiros por estado')
        with tab4:
            st.subheader(
                'Variação de procura de destino em relação ao mês anterior',

            )

    def rodar_dashboard(self):
        self.gerar_layout_receita_origem()
