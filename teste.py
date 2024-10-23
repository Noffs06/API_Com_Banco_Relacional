#    with graf2:
#       st.write("Gráfico de Linhas")
#       dados = df_selecionado.groupby("marca").count()[["valor"]]

#       fig_valores2 = px.line(dados,
#                              x=dados.index,
#                              y="valor",
#                              title="Valores por Marca</b>",
#                              color_discrete_sequence=["#0083b8"] )


#       st.plotly_chart(fig_valores2, use_container_width=True)      

import streamlit as st
import pandas as pd
import numpy as np
from query import conexao
import plotly.express as px 


# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# st.line_chart(chart_data)



query = """
SELECT c.marca , h.data_modificacao, h.valor_anterior, h.valor_novo
FROM historico_preco h
INNER JOIN tb_carros as c ON h.id = c.id_carro
"""
df_hist = conexao(query)

graf = px.line(df_hist,
                x="data_modificacao",
                y=["valor_anterior", "valor_novo"],
                title= "Comparação de Valores (Antigo e Atual)",
                labels={"value": "Valor", "variable": "Tipo"} 
                 )

st.plotly_chart(graf, use_container_width= True)