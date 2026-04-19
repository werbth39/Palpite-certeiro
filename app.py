import streamlit as st

st.title("🔥 Palpite Certeiro")

st.header("Análise de jogo")

# Inputs
time_casa = st.text_input("Time da casa")
time_fora = st.text_input("Time visitante")

odd_over = st.number_input("Odd Over 2.5", value=1.80)
odd_btts = st.number_input("Odd Ambas Marcam", value=1.90)

# Botão
if st.button("Analisar jogo"):
    st.subheader("Resultado da análise")

    if odd_over < 2.0:
        st.write("🔵 Tendência de jogo com gols (+2.5)")
    else:
        st.write("⚠️ Linha alta, cuidado com over")

    if odd_btts < 2.0:
        st.write("🟢 Ambas marcam com valor")
    else:
        st.write("🔴 BTTS arriscado")
