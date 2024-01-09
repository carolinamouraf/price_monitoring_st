import streamlit as st
import pandas as pd
import numpy as np
from crawlers import *
from aux_app import *
from PIL import Image
import time


# CREATING SIDE BAR

image = Image.open('assets/farmbits-logo-alt2.png')
st.sidebar.image(image)
st.sidebar.markdown('# Pesquisar novo produto:')

st.sidebar.markdown('### Para começar, insira o nome de um produto e seu preço na loja Farmbits:')

product = st.sidebar.text_input('Insira o produto')

price_farm = st.sidebar.text_input('Preço Farmbits')
butt1 = st.sidebar.button('Buscar produto')
help_str = 'Adicionar o produto na lista de itens que devem ficar salvos para futuras pesquisas. Caso não deseje salvar, desative a opção antes de procurar pelo item.'
on = st.sidebar.checkbox(label='Salvar produto', value = False, key='saving_prod', help = help_str)

dictionary_items_prices = open_item_list()
st.sidebar.markdown('# Pesquisar produtos salvos:')
option = st.sidebar.selectbox(
    'Produtos', dictionary_items_prices.keys())

if on:
    save_item(product, price_farm)

butt2 = st.sidebar.button('Buscar produto da lista')

if butt1:
    price_farm = price_farm.replace(',', '.')
    price_farm = float(price_farm)

    st.subheader('Produtos encontrados:')

    # RUNNING THE CRAWLERS AND READING THE DATAFRAMES

    df_mercado = mercado_livre(product)
    if type(df_mercado) == str:
        str_result_merc = 'Produto não encontrado no site Mercado Livre!'
    else:
        pass

    # -----------------------------------------------------------

    df_agrosolo = agrosolo(product)
    if type(df_agrosolo) == str:
        str_result_agrosolo = 'Produto não encontrado no site Agrosolo!'
    else:
        pass

    # -----------------------------------------------------------

    df_lojagropecuaria = loja_agropecuaria(product)
    if type(df_lojagropecuaria) == str:
        str_result_lojagro = 'Produto não encontrado no site Loja Agropecuária!'
    else:
        pass

    # -----------------------------------------------------------

    df_bom_cultivo = bom_cultivo(product)
    if type(df_bom_cultivo) == str:
        str_result_bomcult = 'Produto não encontrado no site Bom Cultivo!'
    else:
        pass

    # -----------------------------------------------------------

    df_agromania = agromania(product)
    if type(df_agromania) == str:
        str_result_agromania = 'Produto não encontrado no site Agromania!'
    else:
        pass



    # CREATING THE DATAFRAMES FOR EACH STORE

    mean_price_mercado, df_price_mercado = mean_price_merc_livre(df_mercado)
    mean_pric_agrosolo, df_price_agrosolo = mean_price_agrosolo(df_agrosolo)
    mean_price_lojagro, df_price_lojagro = mean_price_loja_agropecuaria(df_lojagropecuaria)
    mean_price_bomcult, df_price_bomcul = mean_price_bom_cultivo(df_bom_cultivo)
    mean_price_agroman, df_price_agroman = mean_price_agromania(df_agromania)


    df_prices = pd.DataFrame(columns = ['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO', 'LOJA'])
    df_prices = df_prices.append(df_price_mercado).reset_index(drop = True)
    df_prices = df_prices.append(df_price_agrosolo).reset_index(drop = True)
    df_prices = df_prices.append(df_price_lojagro).reset_index(drop = True)
    df_prices = df_prices.append(df_price_bomcul).reset_index(drop = True)
    df_prices = df_prices.append(df_price_agroman).reset_index(drop = True)


    # COMPARING PRICES
        
    mean_price = (mean_price_mercado + mean_pric_agrosolo + mean_price_lojagro + mean_price_bomcult
                + mean_price_agroman)/5

    mean_price = round(mean_price, 2)

    difference_to_mean = price_farm - mean_price
    difference_to_mean = round(difference_to_mean, 2)

    # Max Price
    df_max = df_prices[df_prices['PRECO_DESCONTO'] == df_prices['PRECO_DESCONTO'].max()]
    max_prod = df_max.iloc[0, 0]
    max_value = float(df_max.iloc[0, 1])
    store_max = df_max.iloc[0, 6]

    difference_to_max = price_farm - max_value
    difference_to_max = round(difference_to_max, 2)

    # Min Price
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Mercado Livre", "Agrosolo", "Loja Agropecuária", "Bom Cultivo", "Agromania"])

    with tab1:
        st.header("Mercado Livre")
        if type(df_mercado) == str:
                st.write(str_result_merc)
        else:
                st.dataframe(df_mercado)

        st.download_button(label="Baixar planilha", data=df_mercado.to_csv(index=False),
                        file_name='mercado_livre.csv')

    with tab2:
        st.header("Agrosolo")
        if type(df_agrosolo) == str:
            st.write(str_result_agrosolo)
        else:
            st.dataframe(df_agrosolo)
        
        st.download_button(label="Baixar planilha", data=df_agrosolo.to_csv(index=False),
                file_name='agrosolo.csv')

    with tab3:
        st.header("Loja Agropecuária")
        if type(df_lojagropecuaria) == str:
            st.write(str_result_lojagro)
        else:
            st.dataframe(df_lojagropecuaria)

        st.download_button(label="Baixar planilha", data=df_lojagropecuaria.to_csv(index=False),
                file_name='loja_agropecuaria.csv')

    with tab4:
        st.header("Bom Cultivo")
        if type(df_bom_cultivo) == str:
            st.write(str_result_bomcult)
        else:
            st.dataframe(df_bom_cultivo)

        st.download_button(label="Baixar planilha", data=df_bom_cultivo.to_csv(index=False),
                file_name='bom_cultivo.csv')

    with tab5:
        st.header("Agromania")
        if type(df_agromania) == str:
            st.write(str_result_agromania)
        else:
            st.dataframe(df_agromania)
        
        st.download_button(label="Baixar planilha", data=df_agromania.to_csv(index=False),
            file_name='agromania.csv')

elif butt2:
    product = option
    price_farm = dictionary_items_prices[option]
    try:
        price_farm = price_farm.replace(',', '.')
        price_farm = float(price_farm)
    except:
        pass
    st.subheader('Produtos encontrados:')

    # RUNNING THE CRAWLERS AND READING THE DATAFRAMES

    df_mercado = mercado_livre(product)
    if type(df_mercado) == str:
        str_result_merc = 'Produto não encontrado no site Mercado Livre!'
    else:
        pass

    # -----------------------------------------------------------

    df_agrosolo = agrosolo(product)
    if type(df_agrosolo) == str:
        str_result_agrosolo = 'Produto não encontrado no site Agrosolo!'
    else:
        pass

    # -----------------------------------------------------------

    df_lojagropecuaria = loja_agropecuaria(product)
    if type(df_lojagropecuaria) == str:
        str_result_lojagro = 'Produto não encontrado no site Loja Agropecuária!'
    else:
        pass

    # -----------------------------------------------------------

    df_bom_cultivo = bom_cultivo(product)
    if type(df_bom_cultivo) == str:
        str_result_bomcult = 'Produto não encontrado no site Bom Cultivo!'
    else:
        pass

    # -----------------------------------------------------------

    df_agromania = agromania(product)
    if type(df_agromania) == str:
        str_result_agromania = 'Produto não encontrado no site Agromania!'
    else:
        pass



    # CREATING THE DATAFRAMES FOR EACH STORE

    mean_price_mercado, df_price_mercado = mean_price_merc_livre(df_mercado)
    mean_pric_agrosolo, df_price_agrosolo = mean_price_agrosolo(df_agrosolo)
    mean_price_lojagro, df_price_lojagro = mean_price_loja_agropecuaria(df_lojagropecuaria)
    mean_price_bomcult, df_price_bomcul = mean_price_bom_cultivo(df_bom_cultivo)
    mean_price_agroman, df_price_agroman = mean_price_agromania(df_agromania)


    df_prices = pd.DataFrame(columns = ['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO', 'LOJA'])
    df_prices = df_prices.append(df_price_mercado).reset_index(drop = True)
    df_prices = df_prices.append(df_price_agrosolo).reset_index(drop = True)
    df_prices = df_prices.append(df_price_lojagro).reset_index(drop = True)
    df_prices = df_prices.append(df_price_bomcul).reset_index(drop = True)
    df_prices = df_prices.append(df_price_agroman).reset_index(drop = True)


    # COMPARING PRICES
        
    mean_price = (mean_price_mercado + mean_pric_agrosolo + mean_price_lojagro + mean_price_bomcult
                + mean_price_agroman)/5

    mean_price = round(mean_price, 2)

    difference_to_mean = price_farm - mean_price
    difference_to_mean = round(difference_to_mean, 2)

    # Max Price
    df_max = df_prices[df_prices['PRECO_DESCONTO'] == df_prices['PRECO_DESCONTO'].max()]
    max_prod = df_max.iloc[0, 0]
    max_value = float(df_max.iloc[0, 1])
    store_max = df_max.iloc[0, 6]

    difference_to_max = price_farm - max_value
    difference_to_max = round(difference_to_max, 2)

    # Min Price
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Mercado Livre", "Agrosolo", "Loja Agropecuária", "Bom Cultivo", "Agromania"])

    with tab1:
        st.header("Mercado Livre")
        if type(df_mercado) == str:
            st.write(str_result_merc)
        else:
            st.dataframe(df_mercado)
        
        st.download_button(label="Baixar planilha", data=df_mercado.to_csv(index=False),
                            file_name='mercado_livre.csv')

    with tab2:
        st.header("Agrosolo")
        if type(df_agrosolo) == str:
            st.write(str_result_agrosolo)
        else:
            st.dataframe(df_agrosolo)
        
        st.download_button(label="Baixar planilha", data=df_agrosolo.to_csv(index=False),
                    file_name='agrosolo.csv')

    with tab3:
        st.header("Loja Agropecuária")
        if type(df_lojagropecuaria) == str:
            st.write(str_result_lojagro)
        else:
            st.dataframe(df_lojagropecuaria)
        
        st.download_button(label="Baixar planilha", data=df_lojagropecuaria.to_csv(index=False),
            file_name='loja_agropecuaria.csv')

    with tab4:
        st.header("Bom Cultivo")
        if type(df_bom_cultivo) == str:
            st.write(str_result_bomcult)
        else:
            st.dataframe(df_bom_cultivo)

        st.download_button(label="Baixar planilha", data=df_bom_cultivo.to_csv(index=False),
            file_name='bom_cultivo.csv')

    with tab5:
        st.header("Agromania")
        if type(df_agromania) == str:
            st.write(str_result_agromania)
        else:
            st.dataframe(df_agromania)

        st.download_button(label="Baixar planilha", data=df_agromania.to_csv(index=False),
        file_name='agromania.csv')

    
    



        

    



