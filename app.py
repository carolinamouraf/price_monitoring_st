import streamlit as st
import pandas as pd
import numpy as np
from crawlers import *
from aux_app import *
from PIL import Image
import time

# CREATING SIDE BAR

image = Image.open('assets/logo_vert.png')
st.sidebar.image(image)

option = st.sidebar.selectbox(
    'Escolha como pesquisar:',
    ('Produto único', 'Tabela de produtos', 'Procurar por GTIN'))
    
options_store = st.sidebar.multiselect(
    "Selecione as lojas em que deseja pesquisar",
    ["Mercado Livre", "Agrosolo", "Loja Agropecuária", "Bom Cultivo", "Agromania", 
     "DD Máquinas", "Buscapé", "Cocamar", "Orbia", "Conecta Basf", "Lavoro"],
     placeholder = "Selecione uma ou mais lojas")


if (option == 'Produto único') | (option == 'Procurar por GTIN'):

    if (option == 'Procurar por GTIN'):
        gtin = 'on'
        text_bar = 'Insira o GTIN'
    elif (option == 'Produto único'):
        gtin = 'off'
        text_bar = 'Insira o produto'

    st.sidebar.markdown('# Pesquisar novo produto:')

    st.sidebar.markdown('### Para começar, insira o nome de um produto ou GTIN e seu preço na loja Farmbits:')

    product = st.sidebar.text_input(text_bar)
    price_farm = st.sidebar.text_input('Preço Farmbits')

    butt1 = st.sidebar.button('Pesquisar')


    if butt1:
        price_farm = price_farm.replace(',', '.')
        price_farm = float(price_farm)

        st.subheader('Produtos encontrados:')

        # RUNNING THE CRAWLERS AND READING THE DATAFRAMES

        if np.isin("Mercado Livre", options_store) == True:
            df_mercado = mercado_livre(product, gtin)
            if type(df_mercado) == str:
                str_result_merc = 'Produto não encontrado no site Mercado Livre!'
            else:
                pass
        else:
            df_mercado = "null"

        # -----------------------------------------------------------
        if np.isin("Agrosolo", options_store) == True:
            df_agrosolo = agrosolo(product)
            if type(df_agrosolo) == str:
                str_result_agrosolo = 'Produto não encontrado no site Agrosolo!'
            else:
                pass
        else:
            df_agrosolo = "null"

        # -----------------------------------------------------------
        if np.isin("Loja Agropecuária", options_store) == True:
            df_lojagropecuaria = loja_agropecuaria(product)
            if type(df_lojagropecuaria) == str:
                str_result_lojagro = 'Produto não encontrado no site Loja Agropecuária!'
            else:
                pass
        else:
            df_lojagropecuaria = "null"
            
        # -----------------------------------------------------------
        if np.isin("Bom Cultivo", options_store) == True:
            df_bom_cultivo = bom_cultivo(product)
            if type(df_bom_cultivo) == str:
                str_result_bomcult = 'Produto não encontrado no site Bom Cultivo!'
            else:
                pass
        else:
            df_bom_cultivo = "null"

        # -----------------------------------------------------------
        if np.isin("Agromania", options_store) == True:
            df_agromania = agromania(product)
            if type(df_agromania) == str:
                str_result_agromania = 'Produto não encontrado no site Agromania!'
            else:
                pass
        else:
            df_agromania = "null"

        # -----------------------------------------------------------
        if np.isin("DD Máquinas", options_store) == True:
            df_ddmaquinas = ddmaquinas(product)
            if type(df_ddmaquinas) == str:
                str_result_ddmaquinas = 'Produto não encontrado no site DD Máquinas!'
            else:
                pass
        else:
            df_ddmaquinas = "null"

        # -----------------------------------------------------------
        if np.isin("Buscapé", options_store) == True:
            df_buscape = search_product_buscape(product)
            if type(df_buscape) == str:
                str_result_buscape = 'Produto não encontrado no site Buscapé!'
            else:
                pass
        else:
            df_buscape = "null"

        # -----------------------------------------------------------
        if np.isin("Cocamar", options_store) == True:
            df_cocamar = cocamar(product)
            if type(df_cocamar) == str:
                str_result_cocamar = 'Produto não encontrado no site Buscapé!'
            else:
                pass
        else:
            df_cocamar = "null"
        # -----------------------------------------------------------

        # 'annalgs30@gmail.com'
        # "Was2737!"
        if np.isin("Orbia", options_store) == True:
            login='32969111896'
            password='Carol280205!'

            df_orbia = orbia(product,login,password)
            if type(df_orbia) == str:
                str_result_orbia = 'Produto não encontrado no Orbia!'
            else:
                pass
        else:
            df_orbia = "null"
        
        # -----------------------------------------------------------
        if np.isin("Conecta Basf", options_store) == True:
            df_basf = conecta_basf(product)
            if type(df_basf) == str:
                str_result_basf = 'Produto não encontrado no Conecta Basf'
            else:
                pass
        else:
            df_basf = "null"

        # -----------------------------------------------------------
        if np.isin("Lavoro", options_store) == True:
            df_lavoro = lavoro(product)
            if type(df_lavoro) == str:
                str_result_lavoro = 'Produto não encontrado na Lavoro'
            else:
                pass
        else:
            df_lavoro = "null"


        # CREATING THE DATAFRAMES FOR EACH STORE

        dic_defs = {"Mercado Livre":[mean_price_merc_livre(df_mercado), "_mercado"], "Agrosolo":[mean_price_agrosolo(df_agrosolo), "_agrosolo"], 
                    "Loja Agropecuária":[mean_price_loja_agropecuaria(df_lojagropecuaria), "_lojagro"], 
                    "Bom Cultivo":[mean_price_bom_cultivo(df_bom_cultivo), "_bomcul"], "Agromania":[mean_price_agromania(df_agromania), "_agroman"], 
                    "DD Máquinas":[mean_price_dd_maquinas(df_ddmaquinas), "_ddmaq"], "Buscapé":[mean_price_buscape(df_buscape), "_buscap"], 
                    "Cocamar":[mean_price_cocamar(df_cocamar), "_coca"], "Orbia":[mean_price_orbia(df_orbia), "_orb"], 
                    "Conecta Basf":[mean_price_conecta_basf(df_basf), "_basf"], "Lavoro":[mean_price_lavoro(df_lavoro), "_lavoro"]}
        
        
        mean_prices_list = []
        df_prices = pd.DataFrame(columns = ['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO', 'LOJA'])
        for key in dic_defs.keys():
            if np.isin(key, options_store) == True:
                function = dic_defs[key][0]
                store = dic_defs[key][1]
                mean_pri = "mean_pri" + str(store)
                df_price = "df_price" + str(store)
                
                try:
                    mean_pri, df_price = function
                except:
                    mean_pri = 0
                    df_price = pd.DataFrame(columns = ['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL',
                                                                'DESCONTO', 'LOJA'])
                    
                df_prices = pd.concat([df_prices, df_price]).reset_index(drop=True)
                mean_prices_list.append(mean_pri)

    

        # COMPARING PRICES
            
        mean_price = sum(mean_prices_list)/len(mean_prices_list)

        mean_price = round(mean_price, 2)

        difference_to_mean = price_farm - mean_price
        difference_to_mean = round(difference_to_mean, 2)

        # Max Price
        if gtin == 'on':

            indice_max_price = df_mercado['PRECO_DESCONTO'].idxmax()
            max_prod = df_mercado.at[indice_max_price, 'PRODUTO']

            indice_min_price = df_mercado['PRECO_DESCONTO'].idxmin()
            min_prod = df_mercado.at[indice_min_price, 'PRODUTO']
            store_max = 'Mercado Livre'
            store_min = 'Mercado Livre'

            max_value = float(df_mercado['PRECO_DESCONTO'].max())
            min_value = float(df_mercado['PRECO_DESCONTO'].min())

            difference_to_max = price_farm - max_value
            difference_to_max = round(difference_to_max, 2)

            difference_to_min = price_farm - min_value
            difference_to_min = round(difference_to_min, 2)
        else:

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


        tabs = {f'tab_{i}': valor for i, valor in enumerate(options_store)}

        store_list = ["Mercado Livre", "Agrosolo", "Loja Agropecuária", "Bom Cultivo", "Agromania", 
                      "DD Máquinas", "Buscapé", "Cocamar", "Orbia", "Conecta Basf", "Lavoro"]
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(store_list)


        ### TENTAR FAZER DEPLOYYYY

        def find_key(store):
            for key, value in tabs.items():
                if value == store:
                    return key
                
        if np.isin("Mercado Livre", options_store) == False:
            with tab1:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab1:
                st.header("Mercado Livre")
                if type(df_mercado) == str:
                    st.write(str_result_merc)
                else:
                    df_mercado_one = round_func(df_mercado)
                    st.data_editor(df_mercado_one,
                                    column_config={
                                        "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                    },
                                    hide_index=True, key='mercado_one'
                                )
                    st.download_button(label="Baixar planilha", data=df_mercado_one.to_csv(index=False),
                                    file_name='mercado_livre.csv')
                    
        if np.isin("Agrosolo", options_store) == False:
            with tab2:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab2:
                st.header("Agrosolo")
                if type(df_agrosolo) == str:
                    st.write(str_result_agrosolo)
                else:
                    df_agrosolo_one = round_func(df_agrosolo)
                    st.data_editor(df_agrosolo_one,
                                    column_config={
                                        "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                    },
                                    hide_index=True, key='agrosolo_one'
                                )
                    st.download_button(label="Baixar planilha", data=df_agrosolo_one.to_csv(index=False),
                            file_name='agrosolo.csv')

        if np.isin("Loja Agropecuária", options_store) == False:
            with tab3:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab3:
                st.header("Loja Agropecuária")
                if type(df_lojagropecuaria) == str:
                    st.write(str_result_lojagro)
                else:
                    df_lojagropecuaria_one = round_func(df_lojagropecuaria)
                    st.data_editor(df_lojagropecuaria_one,
                        column_config={
                            "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                        },
                        hide_index=True, key='lojagro_one'
                    )
                    st.download_button(label="Baixar planilha", data=df_lojagropecuaria_one.to_csv(index=False),
                            file_name='loja_agropecuaria.csv')

        if np.isin("Bom Cultivo", options_store) == False:
            with tab4:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab4:
                st.header("Bom Cultivo")
                if type(df_bom_cultivo) == str:
                    st.write(str_result_bomcult)
                else:
                    df_bom_cultivo_one = round_func(df_bom_cultivo)
                    st.data_editor(df_bom_cultivo_one,
                        column_config={
                            "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                        },
                        hide_index=True, key='bomcultivo_one'
                    )
                    st.download_button(label="Baixar planilha", data=df_bom_cultivo_one.to_csv(index=False),
                            file_name='bom_cultivo.csv')
                    
        if np.isin("Agromania", options_store) == False:
            with tab5:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab5:
                st.header("Agromania")
                if type(df_agromania) == str:
                    st.write(str_result_agromania)
                else:
                    df_agromania_one = round_func(df_agromania)
                    st.data_editor(df_agromania_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='agromania_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_agromania_one.to_csv(index=False),
                        file_name='agromania.csv')

        if np.isin("DD Máquinas", options_store) == False:
            with tab6:  
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab6:
                st.header("DD Máquinas")
                if type(df_ddmaquinas) == str:
                    st.write(str_result_ddmaquinas)
                else:
                    df_ddmaq_one = round_func(df_ddmaquinas)
                    st.data_editor(df_ddmaq_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='ddmaq_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_ddmaq_one.to_csv(index=False),
                        file_name='ddmaquinas.csv')
        
        if np.isin("Buscapé", options_store) == False:
            with tab7:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab7:
                st.header("Buscapé")
                if type(df_buscape) == str:
                    st.write(str_result_buscape)
                else:
                    df_buscape_one = round_func(df_buscape)
                    st.data_editor(df_buscape_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='buscape_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_buscape_one.to_csv(index=False),
                        file_name='buscape.csv')
                    
        if np.isin("Cocamar", options_store) == False:
            with tab8:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab8:
                st.header("Cocamar")
                if type(df_cocamar) == str:
                    st.write(str_result_cocamar)
                else:
                    df_cocamar_one = round_func(df_cocamar)
                    st.dataframe(df_cocamar_one)
                    #st.data_editor(df_cocamar_one,
                    #            column_config={
                    #                "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                    #            },
                    #            hide_index=True, key='cocamar_one'
                    #        )
                    st.download_button(label="Baixar planilha", data=df_cocamar_one.to_csv(index=False),
                        file_name='cocamar.csv')

        if np.isin("Orbia", options_store) == False:
            with tab9:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab9:
                st.header("Orbia")
                if type(df_orbia) == str:
                    st.write(str_result_orbia)
                else:
                    df_orbia_one = round_func(df_orbia)
                    st.data_editor(df_orbia_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='orbia_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_orbia_one.to_csv(index=False),
                        file_name='orbia.csv')

        if np.isin("Conecta Basf", options_store) == False:
            with tab10:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")
        else:
            with tab10:
                st.header("Conecta Basf")
                if type(df_basf) == str:
                    st.write(str_result_basf)
                else:
                    df_basf_one = round_func(df_basf)
                    st.data_editor(df_basf_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='conecta_basf_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_basf_one.to_csv(index=False),
                        file_name='conecta_basf.csv')
                    
        if np.isin("Lavoro", options_store) == False:
            with tab11:
                st.write("Selecione a loja na barra lateral para ver seus resultados.")    
        else:
            with tab11:
                st.header("Lavoro")
                if type(df_lavoro) == str:
                    st.write(str_result_lavoro)
                else:
                    df_lavoro_one = round_func(df_lavoro)
                    st.data_editor(df_lavoro_one,
                                column_config={
                                    "VEJA_NO_SITE": st.column_config.LinkColumn("VEJA_NO_SITE")
                                },
                                hide_index=True, key='lavoro_one'
                            )
                    st.download_button(label="Baixar planilha", data=df_lavoro_one.to_csv(index=False),
                        file_name='lavoro.csv')
                
else:
    file = st.sidebar.file_uploader("Carregar tabela", type=['csv', 'xlsx'])

    if file is not None:
        if file.name.endswith('.csv'):
            dataframe = pd.read_csv(file)

        elif file.name.endswith(('.xls', '.xlsx')):
            dataframe = pd.read_excel(file, engine='openpyxl')

        df_result = search_table(dataframe)

        st.header("Resultados")
        if type(dataframe) == str:
            st.write(df_result)
        else:
            st.data_editor(df_result,
                        column_config={
                            "LINK_MAIOR_VALOR": st.column_config.LinkColumn("LINK_MAIOR_VALOR"),
                            "LINK_MENOR_VALOR": st.column_config.LinkColumn("LINK_MENOR_VALOR")
                        },
                        hide_index=True, key='max_value'
                    )
            
            st.download_button(label="Baixar planilha", data=df_result.to_csv(index=False),
                file_name='pesquisa_precos.csv')



            

    
    



        

    



