import pandas as pd
import streamlit as st
from pytrends.request import TrendReq

# Configuração inicial da página
st.set_page_config(
    page_title="Painel de Inteligência de Mercado - Google Trends",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Painel Automatizado de Inteligência de Mercado (Google Trends)")
st.write(
    "Este painel utiliza um robô para buscar o interesse de busca em tempo"
    " real direto do Google Trends."
)


# Função para buscar dados do Google Trends de forma automatizada
@st.cache_data(
    ttl=3600
)  # Salva em cache por 1 hora para não sobrecarregar a API do Google
def buscar_dados_trends(termos):
  try:
    # Conectando ao Google Trends (idioma PT, fuso do Brasil)
    pytrends = TrendReq(hl="pt-BR", tz=360)

    # Construindo a carga dos termos para o Brasil nos últimos 3 meses
    pytrends.build_payload(
        termos, cat=0, timeframe="today 3-m", geo="BR", gprop=""
    )

    # Pegando o interesse ao longo do tempo
    df_trends = pytrends.interest_over_time()

    if not df_trends.empty:
      # Remove a coluna 'isPartial' se existir
      if "isPartial" in df_trends.columns:
        df_trends = df_trends.drop(columns=["isPartial"])
      return df_trends
    else:
      return None
  except Exception as e:
    st.error(f"Erro ao buscar dados do Google Trends: {e}")
    return None


# 1. Defina aqui os termos que você quer monitorar automaticamente
# (Você pode mudar para os termos do seu nicho!)
termos_para_monitorar = [
    "tráfego pago",
    "lançamento de infoprodutos",
    "hotmart",
    "marketing digital",
]

st.sidebar.header("🔍 Configuração do Robô")
st.sidebar.info(
    "O robô está monitorando automaticamente os termos configurados no código."
)

# 2. Executando a busca com o robô
with st.spinner(
    "🤖 Robô buscando dados atualizados no Google Trends... Aguarde um"
    " momento..."
):
  df_dados = buscar_dados_trends(termos_para_monitorar)

# 3. Exibindo os resultados no painel
if df_dados is not None:
  st.markdown("---")
  st.subheader("📈 Evolução do Interesse de Busca (Últimos 3 Meses)")
  st.write(
    "Escala de 0 a 100 indicando o interesse relativo de busca pelo termo no"
    " Brasil."
  )

  # Exibindo o Gráfico de Linhas do Streamlit nativo (perfeito para o Trends)
  st.line_chart(df_dados)

  # Exibindo a Tabela com os dados mais recentes
  st.markdown("---")
  st.subheader("📋 Dados Brutos Recentes")
  st.dataframe(df_dados.tail(10), use_container_width=True)

else:
  st.warning(
    "⚠️ Não foi possível carregar os dados no momento. O Google Trends pode"
    " ter bloqueado temporariamente as requisições (muito comum em testes"
    " rápidos). Tente recarregar a página em alguns instantes."
  )