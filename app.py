# Importar as bibliotecas necessárias
import streamlit as st
import pandas as pd
from fractions import Fraction

# =====================================================================
# O "CÉREBRO" DO APP - AS FUNÇÕES DE CONVERSÃO (IGUAIS AO CÓDIGO DO COLAB)
# Nenhuma alteração é necessária aqui.
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
# A INTERFACE DO APP - A "CARA" DO NOSSO APLICATIVO (A PARTE DO STREAMLIT)
# É aqui que a mágica do Streamlit acontece!
# =====================================================================

# st.title() -> Cria um título principal para a página
st.title('Calculadora de Conversão de Odds 🎲')

# st.sidebar -> Cria uma barra lateral para colocarmos os controles
st.sidebar.header('Insira a Odd para Converter')

# st.selectbox -> Cria uma caixa de seleção para o usuário escolher uma opção
tipo_odd_selecionada = st.sidebar.selectbox(
    '1. Selecione o formato da sua odd:',
    ('Decimal', 'Americana', 'Fracionária')
)

# Agora, com base na escolha, mostramos o campo de input correto
if tipo_odd_selecionada == 'Decimal':
    # st.number_input -> Campo para inserir números
    valor_input = st.sidebar.number_input('2. Digite o valor da odd:',
                                          min_value=1.01,
                                          value=2.50, # Valor que já aparece por padrão
                                          step=0.1,
                                          format="%.2f")
    # Chama a função de conversão correspondente
    resultado = converter_a_partir_decimal(valor_input)

elif tipo_odd_selecionada == 'Americana':
    valor_input = st.sidebar.number_input('2. Digite o valor da odd:',
                                          value=150,
                                          step=10)
    resultado = converter_a_partir_americana(valor_input)

else: # Fracionária
    # st.text_input -> Campo para inserir texto
    valor_input = st.sidebar.text_input('2. Digite o valor da odd (ex: 5/2):', value='5/2')
    resultado = converter_a_partir_fracionaria(valor_input)


# st.subheader() -> Cria um título menor
st.subheader('Resultado da Conversão')

# Cria o DataFrame com o resultado (igual ao Colab)
df_resultado = pd.DataFrame([resultado])

# st.dataframe() -> Mostra a tabela de forma interativa e bonita
st.dataframe(
    df_resultado,
    hide_index=True, # Esconde o número da linha
    use_container_width=True # Faz a tabela usar toda a largura da página
)

st.markdown("---")
st.write("Desenvolvido para fins de estudo em Python e Streamlit.")