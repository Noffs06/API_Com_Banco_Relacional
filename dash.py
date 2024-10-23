import streamlit as st
import pandas as pd
import plotly.express as px 
from streamlit_option_menu import option_menu
from query import conexao

# ******** PRIMEIRA CONSULTA / ATUALIZAÇÕES DE DADOS ********

query = "SELECT * FROM tb_carros"


df = conexao(query)



if st.button("Atualizar Dados"):
    df = conexao(query)


# ******** ESTRUTURA LATERAL DE FILTROS ********
st.sidebar.header("Selecione o Filtro")


marca = st.sidebar.multiselect("Marca Selecionada",
                               options=df["marca"].unique(),
                               default=df["marca"].unique()
                               )


modelo = st.sidebar.multiselect("Modelo Selecionado",
                                options=df["modelo"].unique(),
                                default=df["modelo"].unique()
                                )




valor = st.sidebar.multiselect("Valor Selecionado",
                                options=df["valor"].unique(),
                                default=df["valor"].unique()
                                )


cor = st.sidebar.multiselect("Cor Selecionada",
                                options=df["cor"].unique(),
                                default=df["cor"].unique()
                                )



numero_vendas = st.sidebar.multiselect("Número de Vendas Selecionado",
                                options=df["numero_vendas"].unique(),
                                default=df["numero_vendas"].unique()
                                )




ano = st.sidebar.multiselect("Ano Selecionado",
                                options=df["ano"].unique(),
                                default=df["ano"].unique()
                                )




# Aplicar od filtros selecionados

df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas)) &
    (df["ano"].isin(ano)) 

]


# ******** EXIBIR VALORES MÉDIOS - ESTÁSTISTICA ********

def Home():
    with st.expander("Valores"): #Cria uma caixa expansivel com um título
     mostrarDados = st.multiselect('Filter:', df_selecionado, default=[])


     if mostrarDados:
        st.write(df_selecionado[mostrarDados]) 



    if not df_selecionado.empty:
       venda_total = df_selecionado["numero_vendas"].sum()
       venda_media = df_selecionado["numero_vendas"].mean()
       venda_mediana = df_selecionado["numero_vendas"].median()

       total1, total2, total3 = st.columns(3, gap="large")

       with total1:
          st.info("Valor Total de Vendas dos Carros", icon="🐯")
          st.metric(label="Total1", value=f"{venda_total:,.0f}")
          
       with total2:
          st.info("Valor Médio das Vendas", icon="🐯")
          st.metric(label="Total2", value=f"{venda_media:,.0f}")
          
       with total3:
          st.info("Valor Mediano dos Carros", icon="🐯")
          st.metric(label="Total3", value=f"{venda_mediana:,.0f}")

    else:
       st.warning("Nenhum dado disponivel com os filtros selecionados")

    
    st.markdown("""-------------""")






# ****************** GRAFICOS *******************
def graficos(df_selecionado):
   if df_selecionado.empty:
      st.warning("Nenhum dado disponivel para gerar gráficos")
      return 
   


   graf1, graf2, graf3, graf4 = st.tabs(["Gráfico de Barras", "Gráfico de Linhas","Gráfico de Pizza", "Gráfico de Dispersão3"])


   with graf1:
      st.write("Gráfico de Barras") # Titulo

      investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
      
      fig_valores = px.bar(investimento,
                           x=investimento.index,
                           y="valor",
                           orientation="h",
                           title="Valores de Carros</b>",
                           color_discrete_sequence=["#0083b3"] )
      

      st.plotly_chart(fig_valores, use_container_width=True)                      

   with graf2:
      st.write("Gráfico de Linhas")
      dados = df_selecionado.groupby("marca").count()[["valor"]]

      fig_valores2 = px.line(dados,
                             x=dados.index,
                             y="valor",
                             title="Valores por Marca</b>",
                             color_discrete_sequence=["#0083b8"] )


      st.plotly_chart(fig_valores2, use_container_width=True)      


   with graf3:
      st.write("Gráfico de Pizza")
      dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

      fig_valores3 = px.pie(dados2,
                            values="valor",
                            names=dados2.index,
                            title="<b>Distribuição de Valores por Marca<b>")
      st.plotly_chart(fig_valores3,use_container_width=True)

   
   with graf4:
      st.write("Gráfico de Dispersão")
      dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])
      
      fig_valores4 =px.scatter(dados3,
                                x="marca",
                                y="value",
                                color="variable",
                                title="</b>Dispersão de Valores por Marca</b>")

      st.plotly_chart(fig_valores4, use_container_width=True)




def barraProgresso():
   objetivo = 1000000
   valorAtual = df_selecionado["numero_vendas"].sum()
   percentual = round((valorAtual / objetivo *100))
   

   if percentual >= 100:
      st.subheader("Valores Atingidos")
   else:
      st.write(f"Você tem {percentual}% de {objetivo}")
      mybar = st.progress(0)
      for percentualCompleto in range(percentual):
         mybar.progress(percentualCompleto + 1, text= "Alvo %")




def menuLateral():
   with st.sidebar:
      selecionado = option_menu(menu_title="Menu", options=["Home",
      "Progresso"], icons=["house", "eye"], menu_icon="cast", 
      default_index= 0)

   if selecionado == "Home":
      st.subheader(f"Página: {selecionado}")
      Home()
      graficos(df_selecionado)

   if selecionado == "Progresso":
      st.subheader(f"Página: {selecionado}")
      barraProgresso()
      graficos(df_selecionado)
      



menuLateral()
