import math
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("🔥 Palpite Certeiro - Matriz Poisson")

# =========================
# FUNÇÕES
# =========================
def poisson(gols: int, media: float) -> float:
    return (math.exp(-media) * (media ** gols)) / math.factorial(gols)

def prob_casa_por_odd(odd: float) -> float:
    return (1 / odd) if odd > 0 else 0

def odd_justa(prob: float) -> float:
    return (1 / prob) if prob > 0 else 0

def status_valor(valor: float) -> str:
    if valor > 0.10:
        return "VALOR MUITO FORTE"
    elif valor > 0.05:
        return "VALOR FORTE"
    elif valor > 0.02:
        return "VALOR LEVE"
    elif valor > 0:
        return "VALOR POSITIVO"
    elif valor < -0.10:
        return "CASA MUITO FORTE"
    elif valor < -0.05:
        return "CASA FORTE"
    elif valor < 0:
        return "CASA LEVE"
    else:
        return "CONFLITO"

def erro_casa(valor: float) -> str:
    if valor > 0:
        return "CASA ERRADA"
    elif valor < 0:
        return "CASA CERTA"
    else:
        return "CONFLITO"

# =========================
# BLOCO 1 - ENTRADA DE DADOS
# =========================
st.subheader("Entrada de Dados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### CASA")
    gols_marcados_casa = st.number_input("Gols marcados casa", min_value=0.0, value=1.64, step=0.01)
    gols_sofridos_casa = st.number_input("Gols sofridos casa", min_value=0.0, value=1.26, step=0.01)
    xg_casa = st.number_input("xG casa (0 se não tiver)", min_value=0.0, value=0.0, step=0.01)
    xg_sofrido_casa = st.number_input("xG sofrido casa (0 se não tiver)", min_value=0.0, value=0.0, step=0.01)

with col2:
    st.markdown("### FORA")
    gols_marcados_fora = st.number_input("Gols marcados fora", min_value=0.0, value=1.19, step=0.01)
    gols_sofridos_fora = st.number_input("Gols sofridos fora", min_value=0.0, value=2.10, step=0.01)
    xg_fora = st.number_input("xG fora (0 se não tiver)", min_value=0.0, value=0.0, step=0.01)
    xg_sofrido_fora = st.number_input("xG sofrido fora (0 se não tiver)", min_value=0.0, value=0.0, step=0.01)

# =========================
# BLOCO 2 - FORÇA DOS TIMES
# =========================
ataque_casa = (gols_marcados_casa + xg_casa) / 2 if xg_casa > 0 else gols_marcados_casa
defesa_casa = (gols_sofridos_casa + xg_sofrido_casa) / 2 if xg_sofrido_casa > 0 else gols_sofridos_casa

ataque_fora = (gols_marcados_fora + xg_fora) / 2 if xg_fora > 0 else gols_marcados_fora
defesa_fora = (gols_sofridos_fora + xg_sofrido_fora) / 2 if xg_sofrido_fora > 0 else gols_sofridos_fora

st.subheader("Força dos Times")

f1, f2, f3, f4 = st.columns(4)
f1.metric("Ataque Casa", round(ataque_casa, 3))
f2.metric("Defesa Casa", round(defesa_casa, 3))
f3.metric("Ataque Fora", round(ataque_fora, 3))
f4.metric("Defesa Fora", round(defesa_fora, 3))

# =========================
# LEITURA DO JOGO
# =========================
dif_ataque = ataque_casa - ataque_fora

if abs(dif_ataque) > 0.50:
    status_jogo = "JOGO DESEQUILIBRADO"
else:
    status_jogo = "JOGO EQUILIBRADO"

st.subheader("Leitura do Jogo")
st.write("Status:", status_jogo)

# =========================
# BLOCO 3 - MATRIZ OCULTA
# =========================
lambda_casa = ataque_casa * defesa_fora
lambda_fora = ataque_fora * defesa_casa

matriz = []
for i in range(0, 11):
    linha = []
    for j in range(0, 11):
        prob = poisson(i, lambda_casa) * poisson(j, lambda_fora)
        linha.append(prob)
    matriz.append(linha)

# =========================
# BLOCO 4 - ODDS DA CASA
# =========================
st.subheader("Odds da Casa")

st.markdown("### 1X2")
m1, m2, m3 = st.columns(3)
with m1:
    odd_vitoria_casa = st.number_input("Odd Vitória Casa", min_value=0.0, value=1.70, step=0.01)
with m2:
    odd_empate = st.number_input("Odd Empate", min_value=0.0, value=4.25, step=0.01)
with m3:
    odd_vitoria_fora = st.number_input("Odd Vitória Fora", min_value=0.0, value=4.90, step=0.01)

st.markdown("### Dupla Chance")
d1, d2, d3 = st.columns(3)
with d1:
    odd_1x = st.number_input("Odd 1X", min_value=0.0, value=1.21, step=0.01)
with d2:
    odd_12 = st.number_input("Odd 12", min_value=0.0, value=1.23, step=0.01)
with d3:
    odd_2x = st.number_input("Odd 2X", min_value=0.0, value=2.25, step=0.01)

st.markdown("### Over / Under")
o1, o2, o3 = st.columns(3)
with o1:
    odd_over05 = st.number_input("Odd Mais 0.5", min_value=0.0, value=1.04, step=0.01)
    odd_under05 = st.number_input("Odd Menos 0.5", min_value=0.0, value=11.25, step=0.01)
    odd_over15 = st.number_input("Odd Mais 1.5", min_value=0.0, value=1.21, step=0.01)
    odd_under15 = st.number_input("Odd Menos 1.5", min_value=0.0, value=4.45, step=0.01)

with o2:
    odd_over25 = st.number_input("Odd Mais 2.5", min_value=0.0, value=1.62, step=0.01)
    odd_under25 = st.number_input("Odd Menos 2.5", min_value=0.0, value=2.30, step=0.01)
    odd_over35 = st.number_input("Odd Mais 3.5", min_value=0.0, value=2.52, step=0.01)
    odd_under35 = st.number_input("Odd Menos 3.5", min_value=0.0, value=1.53, step=0.01)

with o3:
    odd_over45 = st.number_input("Odd Mais 4.5", min_value=0.0, value=4.35, step=0.01)
    odd_under45 = st.number_input("Odd Menos 4.5", min_value=0.0, value=1.22, step=0.01)
    odd_over55 = st.number_input("Odd Mais 5.5", min_value=0.0, value=7.80, step=0.01)
    odd_under55 = st.number_input("Odd Menos 5.5", min_value=0.0, value=1.08, step=0.01)

st.markdown("### Ambas Marcam")
b1, b2 = st.columns(2)
with b1:
    odd_btts_sim = st.number_input("Odd BTTS Sim", min_value=0.0, value=1.62, step=0.01)
with b2:
    odd_btts_nao = st.number_input("Odd BTTS Não", min_value=0.0, value=2.20, step=0.01)

st.markdown("### BTTS Sim ou +2.5")
c1, c2 = st.columns(2)
with c1:
    odd_btts_ou_over25_sim = st.number_input("Odd BTTS Sim ou +2.5 - Sim", min_value=0.0, value=1.38, step=0.01)
with c2:
    odd_btts_ou_over25_nao = st.number_input("Odd BTTS Sim ou +2.5 - Não", min_value=0.0, value=2.87, step=0.01)

# =========================
# BLOCO 5 - CRUZAMENTO
# =========================
prob_vitoria_casa = 0
prob_empate = 0
prob_vitoria_fora = 0

prob_mais05 = 0
prob_menos05 = 0
prob_mais15 = 0
prob_menos15 = 0
prob_mais25 = 0
prob_menos25 = 0
prob_mais35 = 0
prob_menos35 = 0
prob_mais45 = 0
prob_menos45 = 0
prob_mais55 = 0
prob_menos55 = 0

prob_btts_sim = 0
prob_btts_nao = 0

prob_btts_ou_mais25_sim = 0
prob_btts_ou_mais25_nao = 0

for i in range(0, 11):
    for j in range(0, 11):
        p = matriz[i][j]
        total = i + j

        if i > j:
            prob_vitoria_casa += p
        elif i == j:
            prob_empate += p
        else:
            prob_vitoria_fora += p

        if total >= 1:
            prob_mais05 += p
        else:
            prob_menos05 += p

        if total >= 2:
            prob_mais15 += p
        else:
            prob_menos15 += p

        if total >= 3:
            prob_mais25 += p
        else:
            prob_menos25 += p

        if total >= 4:
            prob_mais35 += p
        else:
            prob_menos35 += p

        if total >= 5:
            prob_mais45 += p
        else:
            prob_menos45 += p

        if total >= 6:
            prob_mais55 += p
        else:
            prob_menos55 += p

        if i > 0 and j > 0:
            prob_btts_sim += p
        else:
            prob_btts_nao += p

        if (i > 0 and j > 0) or (total >= 3):
            prob_btts_ou_mais25_sim += p
        else:
            prob_btts_ou_mais25_nao += p

prob_1x = prob_vitoria_casa + prob_empate
prob_12 = prob_vitoria_casa + prob_vitoria_fora
prob_2x = prob_empate + prob_vitoria_fora

mercados = [
    ("VITORIA CASA", prob_vitoria_casa, odd_vitoria_casa),
    ("EMPATE", prob_empate, odd_empate),
    ("VITORIA FORA", prob_vitoria_fora, odd_vitoria_fora),
    ("1X", prob_1x, odd_1x),
    ("12", prob_12, odd_12),
    ("2X", prob_2x, odd_2x),
    ("MAIS 0.5", prob_mais05, odd_over05),
    ("MENOS 0.5", prob_menos05, odd_under05),
    ("MAIS 1.5", prob_mais15, odd_over15),
    ("MENOS 1.5", prob_menos15, odd_under15),
    ("MAIS 2.5", prob_mais25, odd_over25),
    ("MENOS 2.5", prob_menos25, odd_under25),
    ("MAIS 3.5", prob_mais35, odd_over35),
    ("MENOS 3.5", prob_menos35, odd_under35),
    ("MAIS 4.5", prob_mais45, odd_over45),
    ("MENOS 4.5", prob_menos45, odd_under45),
    ("MAIS 5.5", prob_mais55, odd_over55),
    ("MENOS 5.5", prob_menos55, odd_under55),
    ("BTTS SIM", prob_btts_sim, odd_btts_sim),
    ("BTTS NAO", prob_btts_nao, odd_btts_nao),
    ("BTTS SIM OU +2.5 SIM", prob_btts_ou_mais25_sim, odd_btts_ou_over25_sim),
    ("BTTS SIM OU +2.5 NAO", prob_btts_ou_mais25_nao, odd_btts_ou_over25_nao),
]

linhas_resultado = []
for nome, minha_prob, odd in mercados:
    prob_casa = prob_casa_por_odd(odd)
    oddjusta = odd_justa(minha_prob)
    valor = minha_prob - prob_casa
    prob_invertida = 1 - minha_prob

    linhas_resultado.append({
        "mercado": nome,
        "minha_prob": minha_prob,
        "odd_justa": oddjusta,
        "odd_casa": odd,
        "prob_casa": prob_casa,
        "valor": valor,
        "prob_invertida": prob_invertida,
        "status_valor": status_valor(valor),
        "erro_casa": erro_casa(valor),
    })

# =========================
# BLOCO 6 - RESULTADO FINAL
# =========================
df_resultado = pd.DataFrame(linhas_resultado)
df_exibir = df_resultado.copy()

df_exibir["MINHA PROB"] = (df_exibir["minha_prob"] * 100).round(2).astype(str) + "%"
df_exibir["ODD JUSTA"] = df_exibir["odd_justa"].round(2)
df_exibir["ODD CASA"] = df_exibir["odd_casa"].round(2)
df_exibir["PROB CASA"] = (df_exibir["prob_casa"] * 100).round(2).astype(str) + "%"
df_exibir["VALOR CALCULADO"] = (df_exibir["valor"] * 100).round(2).astype(str) + "%"
df_exibir["PROB INVERTIDA"] = (df_exibir["prob_invertida"] * 100).round(2).astype(str) + "%"

df_exibir = df_exibir.sort_values(by="valor", ascending=False)

st.subheader("Cruzamento das Odds com as Probabilidades")
st.dataframe(
    df_exibir[
        [
            "mercado",
            "MINHA PROB",
            "ODD JUSTA",
            "ODD CASA",
            "PROB CASA",
            "VALOR CALCULADO",
            "PROB INVERTIDA",
            "status_valor",
            "erro_casa",
        ]
    ].rename(
        columns={
            "mercado": "MERCADO",
            "status_valor": "STATUS",
            "erro_casa": "STATUS CASA",
        }
    ),
    use_container_width=True,
    hide_index=True
)

st.subheader("Melhores Mercados")
df_validos = df_resultado[df_resultado["odd_casa"] > 0].copy()
df_validos = df_validos.sort_values(by="valor", ascending=False)

if not df_validos.empty:
    melhor = df_validos.iloc[0]
    st.success(
        f'MELHOR MERCADO: {melhor["mercado"]} | '
        f'Minha Prob: {round(melhor["minha_prob"] * 100, 2)}% | '
        f'Odd Justa: {round(melhor["odd_justa"], 2)} | '
        f'Odd Casa: {round(melhor["odd_casa"], 2)} | '
        f'Valor: {round(melhor["valor"] * 100, 2)}% | '
        f'{melhor["status_valor"]} | {melhor["erro_casa"]}'
    )