import pandas as pd
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Painel de Inteligência de Mercado", page_icon="📊", layout="wide"
)

st.title("📊 Painel de Inteligência de Mercado - Infoprodutos")
st.write(
    "Monitore a temperatura de produtos na Hotmart e o volume de anúncios dos concorrentes."
)

# 1. Carregando os dados da planilha local (certifique-se de que o arquivo está na mesma pasta)
try:
  df = pd.read_csv("dados_cursos.csv")
except FileNotFoundError:
  st.error(
    "⚠️ O arquivo 'dados_cursos.csv' não foi encontrado na pasta. Por favor,"
    " adicione-o ao repositório."
  )
  st.stop()

# 2. Barra Lateral (Sidebar) para os Filtros
st.sidebar.header("🔍 Filtros de Análise")

# Verificando se a coluna 'nicho' existe na planilha
if "nicho" in df.columns:
  # Criando a opção de "Todos" + os nichos únicos encontrados na planilha
  nichos_disponiveis = ["Todos"] + list(df["nicho"].unique())
  nicho_selecionado = st.sidebar.selectbox(
    "Selecione o Nicho", nichos_disponiveis
  )

  # Filtrando o DataFrame com base na escolha do usuário
  if nicho_selecionado != "Todos":
    df_filtrado = df[df["nicho"] == nicho_selecionado]
  else:
    df_filtrado = df
else:
  st.sidebar.warning(
    "A coluna 'nicho' não foi encontrada na sua planilha 'dados_cursos.csv'."
  )
  df_filtrado = df

# 3. Exibindo Métricas Principais (KPIs) com base nos dados filtrados
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
  total_cursos = len(df_filtrado)
  st.metric("Total de Produtos Monitorados", total_cursos)

with col2:
  if "temperatura" in df_filtrado.columns and not df_filtrado.empty:
    media_temp = round(df_filtrado["temperatura"].mean(), 1)
    st.metric("Temperatura Média", f"{media_temp}°")
  else:
    st.metric("Temperatura Média", "0°")

with col3:
  if "anuncios" in df_filtrado.columns and not df_filtrado.empty:
    total_anuncios = int(df_filtrado["anuncios"].sum())
    st.metric("Total de Anúncios Ativos (Meta)", total_anuncios)
  else:
    st.metric("Total de Anúncios Ativos (Meta)", 0)

# 4. Tabela de Dados Detalhada
st.markdown("---")
st.subheader("📋 Detalhamento dos Concorrentes / Produtos")

if not df_filtrado.empty:
  # Se houver coluna de link da meta, podemos formatar ou apenas exibir a tabela
  st.dataframe(df_filtrado, use_container_width=True)
else:
  st.info("Nenhum dado encontrado para este filtro.")