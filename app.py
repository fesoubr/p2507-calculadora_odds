# Importar as bibliotecas necessárias
import streamlit as st
import pandas as pd
from fractions import Fraction

# =====================================================================
# O "CÉREBRO" DO APP - AS FUNÇÕES DE CONVERSÃO 
# =====================================================================

def converter_a_partir_decimal(odd_decimal):
    """Converte uma odd Decimal para os outros formatos."""
    if odd_decimal <= 1:
        return {'Decimal': 'Inválida', 'Americana': 'Inválida', 'Fracionária': 'Inválida'}

    if odd_decimal >= 2.0:
        odd_americana = (odd_decimal - 1) * 100
    else:
        odd_americana = -100 / (odd_decimal - 1)

    fracao = Fraction(odd_decimal - 1).limit_denominator(100)
    odd_fracionaria = f"{fracao.numerator}/{fracao.denominator}"

    return {
        'Decimal': f"{odd_decimal:.2f}",
        'Americana': f"{odd_americana:+.0f}",
        'Fracionária': odd_fracionaria
    }

def converter_a_partir_americana(odd_americana):
    """Converte uma odd Americana para os outros formatos."""
    if odd_americana == 0:
        return {'Decimal': 'Inválida', 'Americana': 'Inválida', 'Fracionária': 'Inválida'}

    if odd_americana > 0:
        odd_decimal = (odd_americana / 100) + 1
    else:
        odd_decimal = (100 / abs(odd_americana)) + 1

    return converter_a_partir_decimal(odd_decimal)

def converter_a_partir_fracionaria(odd_fracionaria):
    """Converte uma odd Fracionária (ex: '5/2') para os outros formatos."""
    try:
        numerador, denominador = map(int, odd_fracionaria.split('/'))
        if denominador == 0: raise ValueError
    except (ValueError, TypeError):
        return {'Decimal': 'Inválida', 'Americana': 'Inválida', 'Fracionária': 'Inválida'}

    odd_decimal = (numerador / denominador) + 1
    return converter_a_partir_decimal(odd_decimal)


# =====================================================================
# A INTERFACE DO APP - A "CARA" DO NOSSO APLICATIVO 
# =====================================================================

st.title('Calculadora de Conversão de Odds 🎲')

# Adicionando o st.expander com as descrições dos tipos de odds.
# Usamos st.markdown() para formatar o texto com negrito e parágrafos.
with st.expander("Clique aqui para entender os diferentes formatos de odds"):
    st.markdown("""
        **Decimal (Ex: 1.50, 2.75):** É o mais comum na Europa e no Brasil. O valor já inclui a sua aposta de volta. Se você aposta R$10 em uma odd de 2.50, seu retorno total é R$25 (R$15 de lucro + R$10 da aposta).

        **Fracionária (Ex: 1/2, 5/2):** Comum no Reino Unido. Mostra o lucro puro. Uma odd de 5/2 significa que para cada R$2 que você aposta, você lucra R$5.

        **Americana (Ex: +150, -120):** Comum nos EUA.
        - **Positiva (+150):** Mostra quanto você lucraria com uma aposta de R$100. (+150 significa que R$100 de aposta te dão R$150 de lucro).
        - **Negativa (-120):** Mostra quanto você precisa apostar para ter R$100 de lucro. (−120 significa que você precisa apostar R$120 para lucrar R$100).
    """)


st.sidebar.header('Insira a Odd para Converter')

tipo_odd_selecionada = st.sidebar.selectbox(
    '1. Selecione o formato da sua odd:',
    ('Decimal', 'Americana', 'Fracionária')
)

if tipo_odd_selecionada == 'Decimal':
    valor_input = st.sidebar.number_input('2. Digite o valor da odd:',
                                          min_value=1.01,
                                          value=2.50,
                                          step=0.1,
                                          format="%.2f")
    resultado = converter_a_partir_decimal(valor_input)

elif tipo_odd_selecionada == 'Americana':
    valor_input = st.sidebar.number_input('2. Digite o valor da odd:',
                                          value=150,
                                          step=10)
    resultado = converter_a_partir_americana(valor_input)

else: # Fracionária
    valor_input = st.sidebar.text_input('2. Digite o valor da odd (ex: 5/2):', value='5/2')
    resultado = converter_a_partir_fracionaria(valor_input)

st.subheader('Resultado da Conversão')
df_resultado = pd.DataFrame([resultado])
st.dataframe(
    df_resultado,
    hide_index=True,
    use_container_width=True
)

st.markdown("---")
st.write("Desenvolvido para fins de estudo em Python e Streamlit.")
