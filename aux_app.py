import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
#from difflib import SequenceMatcher
from jarowinkler import jarowinkler_similarity
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from crawlers import *


def words_similatiry(search, percent, dataframe):
    """
    Function to remove all products that are very differente than the product name of search.
    :param search: input of the user
    :param percent: similarity tolerance percentage
    :param dataframe: products dataframe
    :return:
    """

    words_similarity = {}
    for index,produto in enumerate(dataframe["PRODUTO"]):

        words_similarity[produto] = jarowinkler_similarity(f"{search}", f"{produto}")

    value_key_pairs = ((value, key) for (key,value) in words_similarity.items())
    sorted_value_key_pairs = dict(sorted(value_key_pairs, reverse=True))

    for key, value in list(sorted_value_key_pairs.items()):
        if key <percent:
            sorted_value_key_pairs.pop(key)


    list_items = sorted_value_key_pairs.values()
    # Filtering out rows where line_race is not in the list_items
    df = dataframe[dataframe['PRODUTO'].isin(list_items)]

    return df


def round_func(df_infos):
    for i in df_infos.index:
        price = 'R$ ' + str(df_infos['PRECO_DESCONTO'][i])
        df_infos['PRECO_DESCONTO'][i] = price

        try:
            round_price = 'R$ ' + str(round(df_infos['PRECO_ORIGINAL'][i], 2))
            df_infos['PRECO_ORIGINAL'][i] = round_price
        except:
            pass
    
    return df_infos


def lower_names(dataframe):

    dic_prods = {}
    for n in dataframe.index:
        prod = dataframe['PRODUTO'][n]
        prod = prod.lower()
        prod_list = prod.split(' ')

        for word in prod_list:
            if (word == 'fert') or (word == 'fert.'):
                prod = prod.replace(word, 'fertilizante')
                
            if (word == 'c/') or (word == 'c'):
                prod = prod.replace(word, 'com')
                
            if (word == 'cx.') or (word == 'cx'):
                prod = prod.replace(word, 'caixa')

            if (word == 'pct.') or (word == 'pct'):
                prod = prod.replace(word, 'pacote')
        
        dataframe['PRODUTO'][n] = prod
    
    return dataframe


def min_max_dataframe(df_infos, store):
    if type(df_infos) != str:
        df_red_max = df_infos[df_infos['PRECO_DESCONTO'] == df_infos['PRECO_DESCONTO'].max()]
        df_red_min = df_infos[df_infos['PRECO_DESCONTO'] == df_infos['PRECO_DESCONTO'].min()]
        df_prices = pd.concat([df_red_max, df_red_min]).reset_index(drop=True)

        df_prices['LOJA'] = store
        return df_prices
    
    else:
        pass

def mean_price_lavoro(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Lavoro'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_conecta_basf(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Conecta Basf'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_cocamar(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Cocamar'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_orbia(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Orbia'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_dd_maquinas(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'DD Máquinas'
        df_price = min_max_dataframe(df_infos, store)

    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price

def mean_price_buscape(df_infos):
    if type(df_infos) != str:
        mean_price = df_infos['PRECO_DESCONTO'].mean()
        mean_price = round(mean_price, 2)
        store = 'Buscapé'
        df_price = min_max_dataframe(df_infos, store)
        
    else:
        mean_price = 0
        df_price = pd.DataFrame(columns=['PRODUTO','PRECO_DESCONTO','DESCONTO_%','FORMA_PAGAMENTO','PRECO_ORIGINAL','DESCONTO','LOJA'])

    return mean_price, df_price


def mean_price_merc_livre(df_infos):
    if type(df_infos) != str:
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)
            
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
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

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
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace(',','')
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


    