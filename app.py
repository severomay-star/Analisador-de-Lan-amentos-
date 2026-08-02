import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Detector de Lançamentos", page_icon="📈", layout="wide")

st.title("🚀 Analisador de Infoprodutos e Lançamentos")
st.write("Painel Inteligente conectado ao OnlyOffice com Links Diretos.")

# --- BARRA LATERAL DE FILTROS ---
st.sidebar.header("🎛️ Configurações e Filtros")
tema = st.sidebar.text_input("Qual o nicho/filtro?", "Geral")
temperatura_minima = st.sidebar.slider("Temperatura mínima (Hotmart)", 0, 200, 50)
ordenar_por = st.sidebar.selectbox("Ordenar ranking por:", ["Score de Escala", "Temperatura (Hotmart)", "Anúncios Ativos (Meta)"])

if st.sidebar.button("🔍 Carregar e Analisar Dados"):
    with st.spinner("Lendo base de dados do OnlyOffice e processando links..."):
        
        # Procura o arquivo na pasta
        possiveis_nomes = ["dados_cursos.csv", "dados cursos.csv"]
        nome_encontrado = None
        
        for nome in possiveis_nomes:
            if os.path.exists(nome):
                nome_encontrado = nome
                break
        
        if nome_encontrado:
            # Lê os dados direto do CSV gerado no OnlyOffice
            df_cursos = pd.read_csv(nome_encontrado)
            
            # --- BLINDAÇÃO: Garante que temperatura e anúncios são números reais ---
            df_cursos["Temperatura (Hotmart)"] = pd.to_numeric(df_cursos["Temperatura (Hotmart)"], errors="coerce").fillna(0)
            df_cursos["Anúncios Ativos (Meta)"] = pd.to_numeric(df_cursos["Anúncios Ativos (Meta)"], errors="coerce").fillna(0)
            
            # Calcula o Score de Escala automaticamente para cada linha com segurança
            lista_scores = []
            for index, row in df_cursos.iterrows():
                score = int((row["Temperatura (Hotmart)"] * 0.4) + (row["Anúncios Ativos (Meta)"] * 0.8))
                if score > 100: 
                    score = 99
                lista_scores.append(score)
            
            df_cursos["Score de Escala"] = lista_scores
            
            # Aplica os filtros escolhidos na barra lateral
            df_filtrado = df_cursos[df_cursos["Temperatura (Hotmart)"] >= temperatura_minima]
            df_filtrado = df_filtrado.sort_values(by=ordenar_por, ascending=False)
            
            st.success(f"Dados carregados com sucesso do arquivo: `{nome_encontrado}`!")
            
            # --- MÉTRICAS DE DESTAQUE (KPIs) ---
            if not df_filtrado.empty:
                melhor_score = df_filtrado.loc[df_filtrado["Score de Escala"].idxmax()]
                maior_anunciante = df_filtrado.loc[df_filtrado["Anúncios Ativos (Meta)"].idxmax()]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(label="Total de Produtos Monitorados", value=len(df_filtrado))
                with col2:
                    st.metric(label="🔥 Maior Score de Escala", value=f"{melhor_score['Score de Escala']} pts", delta=melhor_score['Nome do Curso'])
                with col3:
                    st.metric(label="📢 Líder em Anúncios (Meta)", value=f"{maior_anunciante['Anúncios Ativos (Meta)']} ads", delta=maior_anunciante['Produtor'])
                
                st.markdown("---")
            
            # Exibe o ranking interativo configurando links clicáveis
            st.subheader(f"📊 Ranking de Inteligência de Mercado")
            
            configuracao_colunas = {}
            if "Link Meta Ads" in df_filtrado.columns:
                configuracao_colunas["Link Meta Ads"] = st.column_config.LinkColumn("Biblioteca de Anúncios (Meta)")
            
            st.dataframe(
                df_filtrado, 
                column_config=configuracao_colunas,
                use_container_width=True
            )
            
            st.info("💡 **Dica:** O sistema agora converte automaticamente qualquer número digitado na planilha, evitando erros de leitura.")
        else:
            st.error(f"⚠️ O arquivo CSV não foi encontrado na pasta do projeto!")
else:
    st.info("👈 Use o menu lateral e clique em **Carregar e Analisar Dados** para abrir sua base de infoprodutos.")