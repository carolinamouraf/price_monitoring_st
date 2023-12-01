import streamlit as st
import pandas as pd
import numpy as np
from aux import *
from PIL import Image

# Creating side bar

image = Image.open('assets/farmbits-logo-alt2.png')
st.sidebar.image(image)
st.sidebar.markdown('# Pesquisar novo produto:')

product = st.sidebar.text_input('Insira o produto')

price_farm = st.sidebar.text_input('Preço Farmbits')

help_str = 'Adicionar o produto na lista de itens que devem ficar salvos para futuras pesquisas. Caso não deseje salvar, desative a opção antes de procurar pelo item.'
on = st.sidebar.checkbox(label='Salvar produto', value = False, key='saving_prod', help = help_str)

dictionary_items_prices = open_item_list()
st.sidebar.markdown('# Pesquisar produtos salvos:')
option = st.sidebar.selectbox(
    'Produtos', dictionary_items_prices.keys())

if on:
    save_item(product, price_farm)

butt2 = st.sidebar.button('Buscar produto')

if butt2:
    product = option
    price_farm = dictionary_items_prices[option]
    print(price_farm)
    try:
        price_farm = price_farm.replace(',', '.')
        price_farm = float(price_farm)
    except:
        pass
    
else:
    price_farm = price_farm.replace(',', '.')
    price_farm = float(price_farm)

# Displaying the data

st.subheader('Produtos encontrados:')

# Running the crawlers and reading the dataframes
df_merc = mercado_livre(product)
if type(df_merc) == str:
    str_result_merc = 'Produto não encontrado no site Mercado Livre!'
else:
    #df_merc.to_csv("../data/merc_livre_" + str(product) + ".csv", index = False)
    pass

df_agros = agrosolo(product)
if type(df_agros) == str:
    str_result = 'Produto não encontrado no site Agrosolo!'
else:
    #df_agros.to_csv("../data/agrosolo_" + str(product) + ".csv", index = False)
    pass
    
df_lojagro = loja_agropecuaria(product)
if type(df_lojagro) == str:
    str_result_lojagro = 'Produto não encontrado no site Loja Agropecuária!'
else:
    #df_lojagro.to_csv("../data/loja_agropecuaria_" + str(product) + ".csv", index = False)
    pass

max_prices = []
min_prices = []

#df_mercado_livre = pd.read_csv("../data/merc_livre_" + str(product) + ".csv")
try:
    df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].str.replace('.', '')
    df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].str.replace(',', '.')
    df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].astype(float)
except:
    #df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].replace('.','')
    df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].replace(',','.')
    df_merc['PRECO_DESCONTO'] = df_merc['PRECO_DESCONTO'].astype(float)
mean_price_merc_livre = df_merc['PRECO_DESCONTO'].mean()
df_red_livre_max = df_merc[df_merc['PRECO_DESCONTO'] == df_merc['PRECO_DESCONTO'].max()]
df_red_livre_min = df_merc[df_merc['PRECO_DESCONTO'] == df_merc['PRECO_DESCONTO'].min()]
df_price_merc_livre = df_red_livre_max.append(df_red_livre_min).reset_index(drop = True)
df_price_merc_livre['LOJA'] = 'Mercado Livre'

if type(df_agros) != str:
    #df_agros = pd.read_csv("../data/agrosolo_" + str(product) + ".csv")
    try:
        df_agros['PRECO_DESCONTO'] = df_agros['PRECO_DESCONTO'].str.replace('.','')
        df_agros['PRECO_DESCONTO'] = df_agros['PRECO_DESCONTO'].str.replace(',','.')
        df_agros['PRECO_DESCONTO'] = df_agros['PRECO_DESCONTO'].astype(float)
    except:
        df_agros['PRECO_DESCONTO'] = df_agros['PRECO_DESCONTO'].replace(',','.')
        df_agros['PRECO_DESCONTO'] = df_agros['PRECO_DESCONTO'].astype(float)

    if type(df_agros['PRECO_ORIGINAL']) == str:
        df_agros['PRECO_ORIGINAL'] = df_agros['PRECO_ORIGINAL'].str.replace(',','.')
        df_agros['PRECO_ORIGINAL'] = df_agros['PRECO_ORIGINAL'].astype(float)
    else:
        pass
    mean_price_agrosolo = df_agros['PRECO_DESCONTO'].mean()
    mean_price_agrosolo = df_agros['PRECO_DESCONTO'].mean()
    df_red_agrosolo_max = df_agros[df_agros['PRECO_DESCONTO'] == df_agros['PRECO_DESCONTO'].max()]
    df_red_agrosolo_min = df_agros[df_agros['PRECO_DESCONTO'] == df_agros['PRECO_DESCONTO'].min()]
    df_price_agrosolo = df_red_agrosolo_max.append(df_red_agrosolo_min).reset_index(drop = True)
    df_price_agrosolo['LOJA'] = 'Agrosolo'
else:
    mean_price_agrosolo = 0
    df_price_agrosolo = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

if type(df_lojagro) != str:
# df_lojagro = pd.read_csv("../data/loja_agropecuaria_" + str(product) + ".csv")
    try:
        df_lojagro['PRECO_DESCONTO'] = df_lojagro['PRECO_DESCONTO'].str.replace('.','')
        df_lojagro['PRECO_DESCONTO'] = df_lojagro['PRECO_DESCONTO'].str.replace(',','.')
        df_lojagro['PRECO_DESCONTO'] = df_lojagro['PRECO_DESCONTO'].astype(float)
    except:
        df_lojagro['PRECO_DESCONTO'] = df_lojagro['PRECO_DESCONTO'].replace(',','.')
        df_lojagro['PRECO_DESCONTO'] = df_lojagro['PRECO_DESCONTO'].astype(float)

    mean_price_lojagro = df_lojagro['PRECO_DESCONTO'].mean()
    mean_price_lojagro = round(mean_price_lojagro, 2)
    mean_price_lojagro = df_lojagro['PRECO_DESCONTO'].mean()
    mean_price_lojagro = round(mean_price_lojagro, 2)
    df_red_lojagro_max = df_lojagro[df_lojagro['PRECO_DESCONTO'] == df_lojagro['PRECO_DESCONTO'].max()]
    df_red_lojagro_min = df_lojagro[df_lojagro['PRECO_DESCONTO'] == df_lojagro['PRECO_DESCONTO'].min()]
    df_price_lojagro = df_red_lojagro_max.append(df_red_lojagro_min).reset_index(drop = True)
    df_price_lojagro['LOJA'] = 'Loja Agropecuária'

else:
    mean_price_lojagro = 0
    df_price_lojagro = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

mean_price = (mean_price_merc_livre + mean_price_agrosolo + mean_price_lojagro)/3
mean_price = round(mean_price, 2)
difference_to_mean = price_farm - mean_price
difference_to_mean = round(difference_to_mean, 2)

df_prices = pd.DataFrame(columns = ['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO', 'LOJA'])
df_prices = df_prices.append(df_price_merc_livre).reset_index(drop = True)
df_prices = df_prices.append(df_price_agrosolo).reset_index(drop = True)
df_prices = df_prices.append(df_price_lojagro).reset_index(drop = True)

#max_value = max(max_prices)
df_max = df_prices[df_prices['PRECO_DESCONTO'] == df_prices['PRECO_DESCONTO'].max()]
max_prod = df_max.iloc[0, 0]
max_value = float(df_max.iloc[0, 1])
#max_value = float(df_max['PRECO_DESCONTO'])
store_max = df_max.iloc[0, 6]
difference_to_max = price_farm - max_value
difference_to_max = round(difference_to_max, 2)

#min_value = min(min_prices)
df_min = df_prices[df_prices['PRECO_DESCONTO'] == df_prices['PRECO_DESCONTO'].min()]
min_prod = df_min.iloc[0, 0]
min_value = float(df_min.iloc[0, 1])
store_min = df_min.iloc[0, 6]
difference_to_min = price_farm - min_value
difference_to_min = round(difference_to_min, 2)

col1, col2, col3 = st.columns(3)
col1.metric("Média de preços", mean_price, difference_to_mean)
col2.metric("Maior preço", max_value, difference_to_max)
col3.metric("Menor preço", min_value, difference_to_min)

st.markdown('**Maior preço:**')
st.markdown(max_prod)
st.markdown('**Loja com maior preço:**')
st.markdown(store_max)
st.markdown('**Menor preço:**')
st.markdown(min_prod)
st.markdown('**Loja com menor preço:**')
st.markdown(store_min)

if type(df_merc) == str:
    st.markdown('#### Mercado Livre')
    st.write(str_result_merc)
else:
    st.markdown('#### Mercado Livre')
    st.dataframe(df_merc)
    #st.download_button(label="Download", data=csv, file_name='mercado_livre' + str(product) + '.csv')


if type(df_agros) == str:
    st.markdown('#### Agrosolo')
    st.write(str_result)
else:
    #df_agrosolo = pd.read_csv("../data/agrosolo_" + str(product) + ".csv")
    st.markdown('#### Agrosolo')
    st.dataframe(df_agros)


if type(df_lojagro) == str:
    st.markdown('#### Loja Agropecuária')
    st.write(str_result_lojagro)
else:
    #df_lojagro = pd.read_csv("../data/loja_agropecuaria_" + str(product) + ".csv")
    st.markdown('#### Loja Agropecuária')
    st.dataframe(df_lojagro)



    

