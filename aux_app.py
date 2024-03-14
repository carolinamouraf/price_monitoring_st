import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


def min_max_dataframe(df_infos, store):     
    df_red_max = df_infos[df_infos['PRECO_DESCONTO'] == df_infos['PRECO_DESCONTO'].max()]
    df_red_min = df_infos[df_infos['PRECO_DESCONTO'] == df_infos['PRECO_DESCONTO'].min()]
    df_prices = pd.concat([df_red_max, df_red_min]).reset_index(drop = True)
    df_prices['LOJA'] = store

    return df_prices



def mean_price_merc_livre(df_infos):
    if type(df_infos) != str:
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace(',', '.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)
            
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Mercado Livre'
        df_price = min_max_dataframe(df_infos, store)
    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price



def mean_price_agrosolo(df_infos):
    if type(df_infos) != str:
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.','')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)

        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Agrosolo'
        df_price = min_max_dataframe(df_infos, store)
    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price



def mean_price_loja_agropecuaria(df_infos):
    if type(df_infos) != str:
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.','')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)

        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Loja Agropecuária'
        df_price = min_max_dataframe(df_infos, store)
    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_bom_cultivo(df_infos):
    if type(df_infos) != str:
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)

        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Bom Cultivo'
        df_price = min_max_dataframe(df_infos, store)
    
    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price



def mean_price_agromania(df_infos):
    if type(df_infos) != str:
        try:
            df_infos["PRECO_DESCONTO"]=df_infos["PRECO_DESCONTO"].str.replace(',','.')
            df_infos["PRECO_DESCONTO"]=df_infos["PRECO_DESCONTO"].astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','.')
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].astype(float)

        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Agromania'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_loja_mecanico(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Loja do Mecânico'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_leroy_merlin(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Leroy Merlin'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

    