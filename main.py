# Custo de tempo de atendimento (Abertura e fechamento de chamados)
# Coleta de dados via excel
import pandas as pd
import streamlit as st
import time
from datetime import datetime

# Inicializa o estado da aplicação
if 'chamados' not in st.session_state:
    st.session_state.chamados = []

# Função para adicionar um chamado
def adicionar_chamado():
    aberto = datetime.now()
    st.session_state.chamados.append({"abertura": aberto, "fechamento": None})
    st.success("Chamado aberto com sucesso!")

# Função para fechar um chamado
def fechar_chamado(index):
    st.session_state.chamados[index]['fechamento'] = datetime.now()
    st.success(f"Chamado {index + 1} fechado com sucesso!")

# Interface simples
st.title("Monitoramento de Tempo Médio de Atendimento")
st.button("Abrir Chamado", on_click=adicionar_chamado)

# Exibe os chamados e permite fechá-los
for i, ch in enumerate(st.session_state.chamados):
    if ch['fechamento'] is None:
        if st.button(f"Fechar Chamado {i + 1}", key=f'fechar_{i}'):
            fechar_chamado(i)

# DataFrame e cálculo
df = pd.DataFrame(st.session_state.chamados)
df = df.dropna()

if not df.empty:
    # Calcula o tempo de atendimento em minutos
    df['tempo'] = (df['fechamento'] - df['abertura']).dt.total_seconds() / 60

    # Exibe o gráfico de linha
    st.line_chart(df['tempo'], use_container_width=True)

    # Exibe o tempo médio de atendimento
    st.write(f"Tempo médio: {df['tempo'].mean():.2f} minutos")

    # Botão para exportar os dados como CSV
    st.download_button(
        label="Baixar Dados",
        data=df.to_csv(index=False),
        file_name="chamados.csv",
        mime="text/csv"
    )
else:
    st.write("Nenhum chamado fechado ainda.")
    streamlit_app.py

