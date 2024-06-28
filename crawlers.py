import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
import streamlit as st
from aux_app import *
from jarowinkler import jarowinkler_similarity
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import re as regex
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# EMAIL E SENHA CONTA GMAIL PARA LAVORO

'joaopbatista1977@gmail.com'
'senha gmail: belagricola24'
'senha lavoro: Belagricola24!'
'CNPJ: 32611624000131'

def search_table(dataframe):

    dataframe = lower_names(dataframe)
    df_general_final = pd.DataFrame(columns=['PRODUTO', 'MAIOR_PRECO', 'LOJA_MAIOR_PRECO', 'MENOR_PRECO', 'LOJA_MENOR_PRECO', 'MEDIA_PRECOS', 'LINK_MAIOR_VALOR', 'LINK_MENOR_VALOR'])

    lojas = [
        ('Mercado Livre', mercado_livre),
        ('Agrosolo', agrosolo),
        ('Loja Agropecuária', loja_agropecuaria),
        ('Bom Cultivo', bom_cultivo),
        ('Agromania', agromania),
        ('DD Máquinas', ddmaquinas),
        ('Buscapé', search_product_buscape)
    ]

    for i in dataframe.index:
        product = str(dataframe['PRODUTO'][i])
        df_prices = pd.DataFrame(columns=['PRODUTO', 'PRECO_DESCONTO', 'DESCONTO_%', 'FORMA_PAGAMENTO', 'PRECO_ORIGINAL', 'DESCONTO', 'LOJA', 'VEJA_NO_SITE'])


        for store, function in lojas:
            if store == 'Mercado Livre':
                df_loja = function(product, gtin='off')
            else:
                df_loja = function(product)
                
            df_min_max_loja = min_max_dataframe(df_loja, store)
            df_prices = pd.concat([df_prices, df_min_max_loja]).reset_index(drop=True)


        try:
            df_prices['PRECO_DESCONTO'] = df_prices['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            df_prices['PRECO_DESCONTO'] = df_prices['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

        
        if df_prices.shape != (0,7):
            max_row = df_prices.loc[df_prices['PRECO_DESCONTO'].idxmax()]
            min_row = df_prices.loc[df_prices['PRECO_DESCONTO'].idxmin()]
            mean_price = df_prices['PRECO_DESCONTO'].mean()
            mean_price = 'R$ ' + str(round(round(mean_price, 2)))
            max_price = 'R$ ' + str(max_row['PRECO_DESCONTO'])
            min_price = 'R$ ' + str(min_row['PRECO_DESCONTO'])
            


            df_un_final = pd.DataFrame({
                'PRODUTO': [product],
                'MAIOR_PRECO': [max_price],
                'LOJA_MAIOR_PRECO': [max_row['LOJA']],
                'MENOR_PRECO': [min_price],
                'LOJA_MENOR_PRECO': [min_row['LOJA']],
                'MEDIA_PRECOS': [mean_price],
                'LINK_MAIOR_VALOR': max_row['VEJA_NO_SITE'],
                'LINK_MENOR_VALOR': min_row['VEJA_NO_SITE']
            })

            df_general_final = pd.concat([df_general_final, df_un_final], ignore_index=True)

        else:
            print('Nenhum produto encontrado!')

    return df_general_final


def mercado_livre(product, gtin):
    '''Responsible for getting the product's prices and payment conditions from mercado livre's website'''
    try:

        def create_url_mercado(key_word):
            key_word = str(key_word)
            url_search = key_word.replace(" ", "%20")
            search = key_word.replace(" ", "-")

            url = "https://lista.mercadolivre.com.br/" + str(search) + "#D[A:" + str(url_search) + "]"

            return url
        
        def create_url_gtin_mercado(product):
            gtin = str(product)
            url = "https://lista.mercadolivre.com.br/0" + str(product) + "#D[A:0" + str(product) + "]"

            return url

        if gtin == 'on':
            url = create_url_gtin_mercado(product)
        else:
            url = create_url_mercado(product)

        page = requests.get(url)
        
        # Creating the soup object
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Get the iformations from the classes: name, price, discount and payment method

        class1 = "ui-search-item__title"
        class2 = "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"
        class3 = "ui-search-price__discount"
        class4 = "ui-search-item__group__element ui-search-installments ui-search-color--BLACK"
        class5 = "ui-search-item__group__element ui-search-installments ui-search-color--LIGHT_GREEN"
        class6 = "ui-search-item__group__element ui-search-link__title-card ui-search-link"

        links_merc = []
        for link in soup.find_all(class_=[class6]): # finding the links at the title class in the code
            stringg = str(link)
            access_link = stringg.split('href')[1].split('"')[1]
            links_merc.append(access_link) 
        
        name_disc = []
        for link in soup.find_all(class_=[class1, class2, class3, class4, class5]): #finding the names at the title class in the code
            info = link.get_text()
            name_disc.append(info)
            
            
        i = 0
        for item in name_disc:
            info_payment = item.replace('em', '$em$')
            info_payment = info_payment.split('$')

            if np.isin('em', info_payment) == False:
                info_price = item.replace('$', '-$-')
                info_price = info_price.split('-')

                if np.isin('$', info_price) == True:
                    name_disc[i] = item + str('|price|')
                    i = i+1 
                else:
                    i = i+1
                    pass
            else:
                i = i+1
                pass
        
        # Creating a dictionary assigning the informations
        info_dict = {}
        j = 0
        for item in name_disc:

            info_payment = item.replace('em', '$em$')
            info_payment = info_payment.split('$')

            info_price = item.split('|')

            info_discount = item.split(' ')

            if (np.isin('em', info_payment) == False) & (np.isin('OFF', info_discount) == False) & (np.isin('price', info_price) == False):
                if item in info_dict.keys():
                    item_change = item + str(' OPÇÃO_2')
                    access_link = links_merc[j]
                    info_dict[item_change] = ['price', 'discount', '-', access_link]
                    prev_item = item_change
                    j = j+1
                else:
                    access_link = links_merc[j]
                    info_dict[item] = ['price', 'discount', '-', access_link]
                    prev_item = item
                    j = j+1

            elif np.isin('price', info_price) == True:
                price = info_price[0].split("$")
                try:
                    info_dict[prev_item][0] = price[1]
                except:
                    pass
                
            elif np.isin('OFF', info_discount) == True:
                splitted = item.split('%')
                try:
                    info_dict[prev_item][1] = splitted[0]
                except:
                    pass
                
            elif np.isin('em', info_payment) == True:
                try:
                    info_dict[prev_item][2] = item
                except:
                    pass
                

        # Constructing the dataframe with the data
        if len(info_dict) == 0:
            df_infos = "Produto não encontrado"
        else:
            df = pd.DataFrame.from_dict(info_dict, orient='index')
            df_infos = df.reset_index()
            df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'DESCONTO_%', 2:'FORMA_PAGAMENTO', 3:'VEJA_NO_SITE'})
            df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].replace('discount', 0)
            df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].astype(int)
            df_infos['PRECO_ORIGINAL'] = 0
                    
            for l in df_infos.index:
                discount = df_infos['DESCONTO_%'][l]
                price_dic = df_infos['PRECO_DESCONTO'][l]
                if discount != 0:
                    #num_disc = int(discount)
                    price_dic = price_dic.replace('.','')
                    price_final = price_dic.replace(',','.')
                    num_price_disc = float(price_final)

                    num_payment = 100 - discount
                    original_price = (num_price_disc * 100)/num_payment

                    df_infos['PRECO_ORIGINAL'][l] = original_price
                    
                else:
                    pass
            
            if gtin=='off':
                df_infos = words_similatiry(product, 0.6, df_infos)
                if df_infos.shape == (0, 6):
                    df_infos = "Nenhum produto encontrado!"
            else:
                if df_infos.shape == (0, 6):
                    df_infos = "Nenhum produto encontrado!"
                else:
                    try:
                        df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
                    except:
                        df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

    except:
        df_infos = "ERRO"
    
    return df_infos

def agrosolo(product):
    try: 
        def create_url(key_word):
            key_word = str(key_word)
            url_search = key_word.replace(" ", "%20")
            url = "https://www.agrosolo.com.br/busca?busca=" + str(url_search)

            return url

        # Accessing the section on mercado livre's website

        url = create_url(product)
        page = requests.get(url)
        
        # Creating the soup object
        soup = BeautifulSoup(page.text, 'html.parser') 
        
        class1 = 'spots__title' #product name
        class2 = 'product__price--installment' # price with PIX
        class3 = 'product__price--after' # price with credit card
        class4 = 'product__off uppercase flex align-center justify-center' #  discount
        class5 = 'product__price--before' # price before discount
        class6 = 'spots__title' #link

        links_agros = []
        for link in soup.find_all(class_=[class6]): #finding the names at the title class in the code
            link_str = str(link)
            link_str = link_str.split('href')[1].split('"')[1].split("/")[1]
            full_link = 'https://www.agrosolo.com.br/produto/' + str(link_str)
            links_agros.append(full_link) 
        
        name_disc = []
        for link in soup.find_all(class_=[class1,class2,class3,class5]): #finding the names at the title class in the code
            info = link.get_text()
            name_disc.append(info)
            
            
        i = 0
        for item in name_disc:
            info_payment = item.replace('PIX', '$PIX$')
            info_payment = info_payment.split('$')

            if np.isin('PIX', info_payment) == False:
                info_card = item.replace('ou', '-ou-')
                info_card = info_card.split('-')

                if np.isin('ou', info_card) == False:
                    price_before = item.replace('$', '-$-')
                    price_before = price_before.split('-')

                    if np.isin('$', price_before) == True:
                        name_disc[i] = item + str('|price_before|')
                        i = i+1 
                    else:
                        i = i+1
                        pass
                else:
                    i = i+1
                    pass
            else:
                i = i+1
                pass
        
        j = 0
        info_dict = {}
        for item in name_disc:

            info_payment = item.replace('PIX', '-PIX-')
            info_payment = info_payment.split('-')

            price_before = item.split('|')

            info_card = item.replace('ou', '-ou-')
            info_card = info_card.split('-')

            if (np.isin('PIX', info_payment) == False) & (np.isin('price_before', price_before) == False) & (np.isin('ou', info_card) == False):
                info_payment2 = item.replace('R$', '-R$-')
                info_payment2 = info_payment2.split('-')
                
                if (np.isin('R$', info_payment2) == False):
                    if item in info_dict.keys():
                        item_change = item + str(' OPÇÃO_2')
                        info_dict[item_change] = ['price_now', 'discount', 'credit_card', 'price_before', 'link']
                        prev_item = item_change
                    else:
                        info_dict[item] = ['price_now', 'discount', 'credit_card', 'price_before', 'link']
                        prev_item = item
                else:
                    continue

            elif np.isin('PIX', info_payment) == True:
                splitted = item.split(' ')
                first = splitted[1]
                if first != 'R$':
                    info_dict[prev_item][0] = splitted[1]
                else:
                    info_dict[prev_item][0] = splitted[2]
                
            elif np.isin('price_before', price_before) == True:
                price_before = price_before[0]
                splitted = price_before.split(' ')
                first = splitted[0]
                if first != 'R$':
                    info_dict[prev_item][3] = first
                else:
                    info_dict[prev_item][3] = splitted[1]
                
            elif np.isin('ou', info_card) == True:
                info_dict[prev_item][2] = item

        i = 0
        for item in info_dict.keys():
            link = links_agros[i]
            info_dict[item][4] = link
            i = i+1
            if i >= len(links_agros):
                break
        
        prod_discount = []
        for link in soup.find_all(class_=[class1,class4]): #finding the names at the title class in the code
            info = link.get_text()
            prod_discount.append(info)
            
        i = 0
        for item in prod_discount:
            info = item.split('%')

            if np.isin(' off', info) == True:
                product = prod_discount[i+1]

                if product in info_dict:
                    info_dict[product][1] = info[0]
                    i = i+1
                else:
                    i = i+1
                    pass
            else:
                i = i+1
                pass


        # Creating the dataframe
        if len(info_dict) == 0:
            df_infos = "Produto não encontrado"

        else:
            df = pd.DataFrame.from_dict(info_dict, orient='index')
            df_infos = df.reset_index()
            df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'DESCONTO_%', 2:'FORMA_PAGAMENTO', 3:'PRECO_ORIGINAL', 4:'VEJA_NO_SITE'})
            df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].replace('discount', 0)
            df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].astype(float)
            df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].replace('price_before', 0)

            try:
                df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].str.replace(',', '.')
                df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].astype(float)
            except:
                pass
            
            df_infos['PRECO_ORIGINAL'].fillna(0, inplace=True)
            mask = df_infos['PRECO_DESCONTO'] == 'price_now'
            df_infos = df_infos[~mask]

            df_infos = words_similatiry(product, 0.6, df_infos)
            if df_infos.shape == (0, 6):
                df_infos = "Nenhum produto encontrado!"
    
    except:
        df_infos = 'ERRO'
    
    
    return df_infos


def loja_agropecuaria(product):
    try:
        def create_url(key_word):
            key_word = str(key_word)
            url_search = key_word.replace(" ", "%20")
            
            url = "https://www.lojaagropecuaria.com.br/" + str(url_search)

            return url
        
        # Accessing the section on loja agropecuaria's website

        url = create_url(product)
        page = requests.get(url)

        # Creating the soup object
        soup = BeautifulSoup(page.text, 'html.parser')

        link_list = []
        for link in soup.find_all(class_ = 'title'):
            link_str = str(link)
            try:
                link_str = link_str.split('\n')[0].split('href="')[1].split('">')[0]
                link_str_list = link_str.split('/')
                if (np.isin('carrinho', link_str_list) == False):
                    url = 'https://www.lojaagropecuaria.com.br' + str(link_str)
                    link_list.append(url)
                else:
                    pass
            except:
                break

        divs = []
        name_disc = []
        for link in soup.find_all(class_='desc position-relative'): #finding the names at the title class in the code
            info = link.get_text()
            name_disc.append(info)

        for item in name_disc:
            info_list = item.split('\n')
            divs.append(info_list)

        j = 0
        dic_infos = {}
        for item in divs:
            product_name = item[1].split('                            ')[1]
            dic_infos[product_name] = ['price', 'payment', 'link_store']
            
            product_price = item[2].split('                        ')[1].split('R$ ')[2].split(' ')[0]
            dic_infos[product_name][0] = product_price
            
            payment = item[3].split('ou ')[1]
            dic_infos[product_name][1] = payment

            link_store = link_list[j]
            dic_infos[product_name][2] = link_store
            j = j+1

        if len(dic_infos) == 0:
            df_infos = "Produto não encontrado"
        else:
            df = pd.DataFrame.from_dict(dic_infos, orient='index')
            df_infos = df.reset_index()
            df_infos['DESCONTO_%'] = 0
            df_infos['PRECO_ORIGINAL'] = 0
            df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'FORMA_PAGAMENTO', 2:'VEJA_NO_SITE'})
            df_infos = df_infos[['PRODUTO', 'PRECO_DESCONTO', 'DESCONTO_%', 'FORMA_PAGAMENTO', 'PRECO_ORIGINAL', 'VEJA_NO_SITE']]

            df_infos = words_similatiry(product, 0.7, df_infos)
            if df_infos.shape == (0, 6):
                df_infos = "Nenhum produto encontrado!"

    except:
        df_infos = "ERRO"

    return df_infos

def bom_cultivo(product):
    try:
        def create_url(key_word):
            key_word = str(key_word)
            url_search = key_word.replace(" ", "%20")
            
            url = "https://www.bomcultivo.com/busca?q=" + str(url_search)
            
            return url
        
        def splitting(lista, n):
            for i in range(0, len(lista), n):
                yield lista[i:i + n]


        final_link_list = []
        def get_link(link_list):
            for i in link_list:
                full_link = 'https://www.bomcultivo.com' + str(i)
                final_link_list.append(full_link)
    
            return final_link_list

        url = create_url(product)
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')

        name_disc = []
        for link in soup.find_all('a'):
            name_disc.append(link.get('href'))

        i = 0
        link_list = []
        for item in name_disc:
            elemnt = name_disc[i]
            elemnt = str(elemnt)
            slement_split = elemnt.split('.')

            slement_split_sec = elemnt.split(':')

            if (np.isin('https://www', slement_split) == False) & (np.isin('//www', slement_split) == False) & (np.isin('pinterest', slement_split) == False) & (np.isin('whatsapp', slement_split) == False) & (np.isin('None', slement_split) == False) & (np.isin('#', slement_split) == False) & (np.isin('google', slement_split) == False):
                if (np.isin('mailto', slement_split_sec) == False) & (np.isin('tel', slement_split_sec) == False):
                    link_list.append(item)
                    i = i+1
            else:
                i = i+1
                pass

        final_link_list = get_link(link_list)

        class1 = "product-name" 
        class2 = "price-big" 
        class3 = "type-payment-condiction"

        name_disc = []
        for link in soup.find_all(class_=[class1, class2, class3]): #finding the names at the title class in the code
            info = link.get_text()
            name_disc.append(info)

        j = 0
        info_dict = {}
        list_of_lists = splitting(name_disc, 3)
        for item in list_of_lists:
            prod_name = item[0]
            try:
                price = item[1].split('R$  ')[1].split('   ')[0]
                payment = item[2].split('ou ')[1]
                link = final_link_list[j]
                j = j+1
            except:
                j = j+1
                pass
            
            info_dict[prod_name] = [price, payment, link]


        if len(info_dict) == 0:
            df_infos = "Produto não encontrado"
        else:
            df_infos = pd.DataFrame.from_dict(info_dict, orient='index')
            df_infos = df_infos.reset_index()
            df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'FORMA_PAGAMENTO', 2:'VEJA_NO_SITE'})
            df_infos['DESCONTO_%'] = 0
            df_infos['PRECO_ORIGINAL'] = 0
            df_infos = df_infos[['PRODUTO', 'PRECO_DESCONTO', 'DESCONTO_%', 'FORMA_PAGAMENTO', 'PRECO_ORIGINAL', 'VEJA_NO_SITE']]

            df_infos = words_similatiry(product, 0.7, df_infos)
            if df_infos.shape == (0, 6):
                df_infos = "Nenhum produto encontrado!"
    except:
        df_infos = "ERRO"


    return df_infos

def agromania(product):
    try:
        def create_url(key_word):
            key_word = str(key_word)
            url_search = key_word.replace(" ", "+")
            
            url = "https://www.agromania.com.br/busca?q=" + str(url_search)
            
            return url

        url = create_url(product)
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')

        links_list = []
        for link in soup.find_all(class_ = 'in_stock flex justify-center'):
            link_store = link.get('href')
            link_store = link_store.split('//')[1]
            links_list.append(link_store)

        name_disc = []
        for link in soup.find_all(class_= 'product-info'): #finding the names at the title class in the code
            info = link.get_text()
            name_disc.append(info)

        j = 0
        info_dict = {}
        for item in name_disc:
            product_name = item.split('\n')[0]
            try:
                price = item.split('\n')[3].split('                                                        ')[1].split(' ')[1]
                payment = item.split('\n')[5].split('                                                      ')[1]
                link = "https://" + str(links_list[j])
                info_dict[product_name] = [price, payment, link]
                j = j+1
            except:
                j = j+1
                pass
            
        if len(info_dict) == 0:
            df_infos = "Produto não encontrado"
        else:
            df_infos = pd.DataFrame.from_dict(info_dict, orient='index')
            df_infos = df_infos.reset_index()
            df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'FORMA_PAGAMENTO', 2:'VEJA_NO_SITE'})
            df_infos['DESCONTO_%'] = 0
            df_infos['PRECO_ORIGINAL'] = 0

            df_infos = words_similatiry(product, 0.65, df_infos)


            if df_infos.shape == (0, 6):
                df_infos = "Nenhum produto encontrado!"
    except:
        df_infos = "ERRO"

    return df_infos


def ddmaquinas(key_word):
    def create_url(key_word):
        key_word = str(key_word)
        url_search = key_word.replace(" ", "%20")

        url = "https://ddmaquinas.com.br/" + str(url_search)

        return url
    
    """
    Function to search price by product name from ddmaquinas.com.br.
    :param key_word: product name
    :return:
    """
    
    url = create_url(key_word)
    page = requests.get(url)

    # Creating the soup object
    soup = BeautifulSoup(page.content, 'html.parser')
    
    product_name_class = "ui-search-item__title shops__item-title"
    product_names = soup.find_all("h2", attrs={"class": product_name_class})
    product_names = [e.text.strip() for e in product_names]
    
    product_class_price = "andes-money-amount ui-search-price__part ui-search-price__part--medium shops__price-part andes-money-amount--cents-superscript"
    product_prices = soup.find_all("span", attrs={"class": product_class_price})
    product_prices = [e.text.strip() for e in product_prices]
    
    payment_method_class = "ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--BLACK"
    payment_methods = soup.find_all("span", attrs={"class": payment_method_class})
    payment_methods = [e.text.strip().replace("em", "").replace("x", "x de")  for e in payment_methods]
    installments_price = []
    regex_quantity = r"\d+x"
    regex_value = r"R\$\d+[,]?\d+"

    for item in payment_methods:
        quantity = re.findall(regex_quantity, item)[0].replace("x", "")
        value = re.findall(regex_value, item)[0].replace("R$", "").replace(",", ".")
        total = float(quantity) * float(value)
        total = '{0:.2f}'.format(total)
        installments_price.append("R$ " + total.replace(".", ","))

    product_link_class = "ui-search-item__group__element ui-search-link__title-card shops__items-group-details ui-search-link"
    links_ddmaq = []
    for link in soup.find_all(attrs={"class": product_link_class}):
        link_str = str(link)
        link_str = link_str.split(' ')[5].split('"')[1]
        links_ddmaq.append(link_str)
    
    lists = [product_names, product_prices, payment_methods, installments_price, links_ddmaq]
    
    for index,product_class in enumerate(lists):
        if len(product_class) == 0:
            product_class = [str() for c in 'c' * len(product_names)]
            lists[index] = product_class
        if len(product_class) < len(product_names):
            product_class.extend([""] *(len(product_names) - len(product_class)))
            
    if all(len(lists[0]) == len(l) for l in lists[1:]):
        products_df = pd.DataFrame({
            'PRODUTO': lists[0],
            'PRECO_DESCONTO': lists[1],
            'PARCELAS': lists[2],
            'PRECO_TOTAL_PARCELAS': lists[3],
            'VEJA_NO_SITE': lists[4]
        })
        products_df = words_similatiry(key_word, 0.65, products_df)
        products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].apply(lambda x: x.split('R$')[1])
        try:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

        if products_df.shape == (0, 5):
            products_df = "Nenhum produto encontrado!"

    else:
        products_df = pd.DataFrame()
        products_df = "Error creating dataframe!"

    
    
    return products_df


def search_product_buscape(key_word):
    """
    Function to search price by product name from buscapé.com.br.
    :param key_word: product name
    :return:
    """
    url = f"https://www.buscape.com.br/search?q={key_word}"
    page = requests.get(url)

    # Creating the soup object
    soup = BeautifulSoup(page.content, 'html.parser')

    product_name_class = "Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_DesktopLabelSAtLarge__wWsED ProductCard_ProductCard_Name__U_mUQ"
    product_price_class = "Text_Text__ARJdp Text_MobileHeadingS__HEz7L"

    product_lowest_price = "Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_MobileLabelSAtLarge__m0whD ProductCard_ProductCard_BestMerchant__JQo_V"
    product_payment_method = "Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_MobileLabelSAtLarge__m0whD ProductCard_ProductCard_Installment__XZEnD"

    product_link = "ProductCard_ProductCard_Inner__gapsh"

    links_buscape = []
    for link in soup.find_all(attrs={"class": product_link}):
        link_str = str(link)
        link_str = str(link_str.split(' ')[3].split('"')[1])
        #link_result = "https://www.buscape.com.br/" + str(link_str)
        links_buscape.append(link_str)

    body = "ProductCard_ProductCard_Body__bnVUn"
    product_full = soup.find_all("div",  attrs={"class": body})
    product_full = [e.text.strip() for e in product_full ]

    product_names = soup.find_all("h2",  attrs={"class": product_name_class})
    product_names = [e.text.strip() for e in product_names ]

    product_prices = soup.find_all("p",  attrs={"class": product_price_class, "data-testid" : "product-card::price"})
    product_prices = [e.text.strip() for e in product_prices ]

    product_lowests = soup.find_all("h3",  attrs={"class": product_lowest_price})
    product_lowests = [e.text.strip() for e in product_lowests ]

    payment_method = soup.find_all("span",  attrs={"class": product_payment_method})
    payment_method = [e.text.strip() for e in payment_method ]


    lists = [product_names, product_prices, product_lowests, payment_method, links_buscape]


    for index,product_class in enumerate(lists):
        if len(product_class) == 0:
            product_class = [str() for c in 'c' * len(product_names)]
            lists[index] = product_class
        if len(product_class) < len(product_names):
            product_class.extend([""] *(len(product_names) - len(product_class)))


    if all(len(lists[0]) == len(l) for l in lists[1:]):
        products_df = pd.DataFrame(
                            {'PRODUTO': lists[0],
                                'PRECO_DESCONTO': lists[1],
                                'MENOR_PREÇO_EM': lists[2],
                            'MÉTODO_PAGAMENTO': lists[3],
                            'VEJA_NO_SITE': lists[4]
                            })
        
    
        products_df = words_similatiry(key_word, 0.55, products_df)
        products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].apply(lambda x: x.split(' ')[1])
        try:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

        if products_df.shape == (0, 5):
            products_df = "Nenhum produto encontrado!"

    else:
        products_df = pd.DataFrame()
        products_df = "Error creating dataframe!"


    return products_df


def cocamar(key_word):
    def create_url(key_word):
        key_word = str(key_word)
        url_search = key_word.replace(" ", "%20")

        url = "https://www.lojacocamar.com.br/" + str(url_search) + "?_q=" + str(url_search) + "&map=ft"

        return url
    
    def existeElemento(driver, path):
        try:
            driver.find_element(By.CSS_SELECTOR, path)
        except NoSuchElementException:
            return False
        
        return True


    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('-disable-infobars')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    chrome_driver_path = '../chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = create_url(key_word)
    driver.get(url)

    sleep(5) 

    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

    while existeElemento(driver, ".cocamarstore-search-result-custom-8-x-buttonShowMore button"):
        button = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cocamarstore-search-result-custom-8-x-buttonShowMore button")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });", button)
        driver.execute_script("arguments[0].click();", button)
        sleep(1)

    sleep(2.5)

    product_name_class = ".vtex-product-summary-2-x-brandName"
    product_names = driver.find_elements(By.CSS_SELECTOR, product_name_class)
    product_names = [item.get_attribute('innerText').strip() for item in product_names]

    product_price_class = ".vtex-product-price-1-x-sellingPriceValue"
    product_prices = driver.find_elements(By.CSS_SELECTOR, product_price_class)
    product_prices = [item.get_attribute('innerText').replace('\xa0', ' ').strip() for item in product_prices]

    product_payment_method_class = ".devcocamar-theme-2-x-shelfPriceContainer"
    product_payment_methods = driver.find_elements(By.CSS_SELECTOR, product_payment_method_class)
    product_payment_methods = [item.get_attribute('innerText').replace('\xa0', ' ').strip() for item in product_payment_methods]

    product_price_box_class = ".vtex-product-summary-2-x-SKUSelectorContainer"
    product_price_box = driver.find_elements(By.CSS_SELECTOR, product_price_box_class)
    product_price_box = [item for item in product_price_box]
    product_units_box = []
    for item in product_price_box:
        unit = ''
        if "Caixa" in item.get_attribute('innerText'):
            elements = item.find_elements(By.CSS_SELECTOR, ".vtex-store-components-3-x-skuSelectorOptionsList .vtex-product-summary-2-x-skuSelectorItemTextValue--summary-sku-selector")
            element = [itemElement for itemElement in elements if "Caixa" in itemElement.get_attribute('innerText')]
            driver.execute_script("arguments[0].click();", element[0]);
            unit = regex.findall(r"\d+", element[0].get_attribute('innerText'))[0]

        product_units_box.append(unit)

    sleep(1)

    product_price_box = driver.find_elements(By.CSS_SELECTOR, product_price_class)
    product_price_box = [item.get_attribute('innerText').replace('\xa0', ' ').strip() for item in product_price_box]

    product_payment_methods_box = driver.find_elements(By.CSS_SELECTOR, product_payment_method_class)
    product_payment_methods_box = [item.get_attribute('innerText').replace('\xa0', ' ').strip() for item in product_payment_methods_box]
    
    for index, item in enumerate(product_price_box):
        if item == product_prices[index]:
            product_price_box[index] = '' 

    for index, item in enumerate(product_payment_methods_box):
        if item == product_payment_methods[index]:
            product_payment_methods_box[index] = '' 

    links_list = []
    lists = [product_names, product_prices, product_payment_methods, product_price_box, product_payment_methods_box, product_units_box, links_list]

    for index,product_class in enumerate(lists):
        if len(product_class) == 0:
            product_class = [str() for c in 'c' * len(product_names)]
            lists[index] = product_class
        if len(product_class) < len(product_names):
            product_class.extend([""] *(len(product_names) - len(product_class)))


    if all(len(lists[0]) == len(l) for l in lists[1:]):
        products_df = pd.DataFrame({
            'PRODUTO': lists[0],
            'PRECO_DESCONTO': lists[1],
            'PRECO_PIX_BOLETO': lists[2],
            'PRECO_CAIXA': lists[3],
            'UNID_CAIXA': lists[5],
            'PRECO_PIX_BOLETO_CAIXA': lists[4],
            'VEJA_NO_SITE': lists[6]
        })
    else:
        products_df = pd.DataFrame()
        print("Error creating dataframe!")

    products_df = words_similatiry(key_word,0.4,products_df)

    driver.quit()

    if products_df.shape == (0, 7):
        products_df = "Nenhum produto encontrado!"
    else:
        products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].apply(lambda x: x.split(' ')[1])
        try:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)


    return products_df

def orbia(key_word,email,password):

    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('-disable-infobars')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--log-level=3')
    chrome_driver_path = '../chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.maximize_window()
    driver.get("https://www.orbia.ag/")

    try:
        close_window_form = "/html/body/div[3]/div/div/a"   
        close_window_button = driver.find_element(By.XPATH, close_window_form)
        close_window_button.click()

    except NoSuchElementException:
        pass

    except:
        close_window_form = "/html/body/div[2]/div/div/a"   
        close_window_button = driver.find_element(By.XPATH, close_window_form)
        close_window_button.click()

    buy_button_form = "/html/body/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/nav/div/div/div/div/ul[1]/li[3]/a"
    buy_button = driver.find_element(By.XPATH, buy_button_form)
    buy_button.click()

    get_it_form = "/html/body/div[1]/section/div[2]/div/div/div[3]/button"
    get_it_button = driver.find_element(By.XPATH, get_it_form)
    get_it_button.click()
        
    login_bt = "/html/body/div/div[1]/div[1]/div[2]/div/div[2]/div/nav/div/div/div/div/ul[2]/li[2]/a/span/span"
    element_login = driver.find_element(By.XPATH, login_bt)
    element_login.click()

    driver.implicitly_wait(10)

    email_form = "/html/body/div[1]/section/div[1]/div[2]/div[1]/div/form/div[1]/div[2]/div[1]/div/input"
    element_email = driver.find_element(By.XPATH, email_form)
    element_email.send_keys(email)

    pass_form = "/html/body/div[1]/section/div[1]/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div/input"
    element_pass = driver.find_element(By.XPATH, pass_form)
    element_pass.send_keys(password)

    submit_bt = "/html/body/div[1]/section/div[1]/div[2]/div[1]/div/form/div[2]/button"
    element_sub = driver.find_element(By.XPATH, submit_bt)
    element_sub.click()

    driver.implicitly_wait(10)

    try:
        close_window_form = "/html/body/div[3]/div/div/a"   
        close_window_button = driver.find_element(By.XPATH, close_window_form)
        close_window_button.click()

    except NoSuchElementException:
        pass
    
    except:
        close_window_form = "/html/body/div[2]/div/div/a"   
        close_window_button = driver.find_element(By.XPATH, close_window_form)
        close_window_button.click()

    search_form = "/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/form/div/input"
    search = driver.find_element(By.XPATH, search_form)
    search.send_keys(key_word)  

    search_button_form = "/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/form/div/div[2]/button"
    search_button = driver.find_element(By.XPATH, search_button_form)
    search_button.click()

    elements_product_name = driver.find_elements(By.CSS_SELECTOR, ".title")
    new_product_list = []
    for item in elements_product_name:
        if "R$" in item.get_attribute("innerHTML"):
            new_product_list.append(item.get_attribute("innerHTML"))

    product_list ={}
    for product in new_product_list:

        soup = BeautifulSoup(product, 'html.parser')
        p = soup.select_one('div.item-name h3') # or select()
        p2 = soup.select_one('div.prices') # or select()

        product_list[p.text] = p2.text.replace("\n", " ")

    driver.quit()

    cols = ["PRODUTO","PRECO_DESCONTO"]
    products_df = pd.DataFrame(product_list.items(), columns=cols)

    if products_df.shape == (0, 2):
        products_df = "Nenhum produto encontrado!"
    else:
        products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].apply(lambda x: x.split(' ')[6])
        try:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            products_df['PRECO_DESCONTO'] = products_df['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)


    return products_df


def conecta_basf(key_word):

    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('-disable-infobars')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--log-level=3')
    chrome_driver_path = '../chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    
    def create_url(key_word):
        key_word = str(key_word)
        url_search = key_word.replace(" ", "+")
        url = "https://conecta.ag/catalogsearch/result/?q=" + str(url_search)

        return url
    
    url = create_url(key_word)
    driver.get(url)

    driver.implicitly_wait(10)

    first_bt = "/html/body/div[7]/aside[1]/div[2]/footer/button/span"
    element_bt = driver.find_element(By.XPATH, first_bt)
    element_bt.click()

    second_bt = "/html/body/div[3]/div[2]/div[3]/div[2]/button/span"
    element_bt2 = driver.find_element(By.XPATH, second_bt)
    element_bt2.click()

    login_bt = "/html/body/div[4]/header/div[2]/div/ul/li/span/span"
    element_lg = driver.find_element(By.XPATH, login_bt)
    element_lg.click()

    driver.implicitly_wait(10)

    email = "Ka061106@hotmail.com"
    passw = "Carol110696!"

    email_form = "/html/body/div[7]/aside[2]/div[2]/div/div/div[2]/div[3]/form/div/div[1]/div/input"
    element_email = driver.find_element(By.XPATH, email_form)
    element_email.send_keys(email)

    passw_form = "/html/body/div[7]/aside[2]/div[2]/div/div/div[2]/div[3]/form/div/div[2]/div/input"
    element_passw = driver.find_element(By.XPATH, passw_form)
    element_passw.send_keys(passw)

    login_ok = "/html/body/div[7]/aside[2]/div[2]/div/div/div[2]/div[3]/form/div/div[3]/div[1]/button/span"
    element_lg_ok = driver.find_element(By.XPATH, login_ok)
    element_lg_ok.click()

    driver.implicitly_wait(20)

    elements_product_name = driver.find_elements(By.CSS_SELECTOR, ".product-item-link")
    title_dic = {}
    for element in elements_product_name:
        element_str = str(element.text)
        link = element.get_attribute('href')
        title_dic[element_str] = ['price', 'brand', link]


    elements_product_price = driver.find_elements(By.CSS_SELECTOR, ".price")
    i = 0
    for prod in title_dic.keys():
        price = elements_product_price[i]
        price = str(price.text)

        title_dic[prod][0] = price

        i = i+1
        if i == len(title_dic):
            break
        else:
            pass


    elements_product_brand = driver.find_elements(By.CSS_SELECTOR, ".manufacturer")
    i = 0
    for prod in title_dic.keys():
        brand = elements_product_brand[i]
        brand = str(brand.text)

        title_dic[prod][1] = brand

        i = i+1
        if i == len(title_dic):
            break
        else:
            pass

    driver.quit()
    

    if len(title_dic) == 0:
        df_infos = "Produto não encontrado"
    else:
        df_infos = pd.DataFrame.from_dict(title_dic, orient='index')
        df_infos = df_infos.reset_index()

        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'MARCA', 2:'VEJA_NO_SITE'})
        df_infos['DESCONTO_%'] = 0
        df_infos['PRECO_ORIGINAL'] = 0

        df_infos = words_similatiry(key_word,0.4,df_infos)
        

        df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].apply(lambda x: x.split(' ')[1])
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

        if df_infos.shape == (0, 6):
            df_infos = "Nenhum produto encontrado!"

    return df_infos
    

def lavoro(key_word):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('-disable-infobars')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--log-level=3')
    chrome_driver_path = '../chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    
    url = "https://www.comprelavoro.com/home"
    driver.get(url)

    cnpj = 32611163240100
    passw = 'Belagricola24!'

    email_form = 'login-form-cpfcnpj'
    element_email = driver.find_element(By.ID, email_form)
    element_email.send_keys(cnpj)

    passw_form = "login-form-password-cpfcnpj"
    element_passw = driver.find_element(By.ID, passw_form)
    element_passw.send_keys(passw)

    login_bt = "/html/body/wainclude/wainclude/wainclude/wainclude/div[1]/header/div[1]/div[1]/div[3]/form/button"
    element_lg = driver.find_element(By.XPATH, login_bt)
    element_lg.click()

    driver.implicitly_wait(10)

    search_form = "/html/body/wainclude/wainclude/div[1]/header/div[1]/div[2]/div[4]/form/input[1]"
    element_search = driver.find_element(By.XPATH, search_form)
    element_search.send_keys(key_word)

    ok_but = "/html/body/wainclude/wainclude/div[1]/header/div[1]/div[2]/div[4]/form/button[2]"
    element_ok = driver.find_element(By.XPATH, ok_but)
    element_ok.click()

    driver.implicitly_wait(10)

    elements_product_name = driver.find_elements(By.CSS_SELECTOR, ".link")

    title_dic = {}
    for element in elements_product_name:
        element_str = str(element.text)
        href = element.get_attribute('href')
        link = "https://www.comprelavoro.com/" + str(href)
        title_dic[element_str] = ['price_discount', link]

    elements_product_price = driver.find_elements(By.CSS_SELECTOR, ".sales")

    i = 0
    for prod in title_dic.keys():
        price = str(elements_product_price[i].text)

        price_list = price.split(' ')
        price = price_list[1]

        title_dic[prod][0] = price

        i = i+1
        if i == len(elements_product_price):
            break
        else:
            pass

    driver.quit()

    if len(title_dic) == 0:
        df_infos = "Produto não encontrado"
    else:
        df_infos = pd.DataFrame.from_dict(title_dic, orient='index')
        df_infos = df_infos.reset_index()

        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'VEJA_NO_SITE'})
        df_infos['DESCONTO_%'] = 0
        df_infos['PRECO_ORIGINAL'] = 0


        #df_infos = words_similatiry(key_word,0.4,df_infos)
        

        #df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].apply(lambda x: x.split(' ')[1])
        try:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].str.replace('.', '').str.replace(',', '.').astype(float)
        except:
            df_infos['PRECO_DESCONTO'] = df_infos['PRECO_DESCONTO'].replace('.', '').replace(',', '.').astype(float)

        if df_infos.shape == (0, 5):
            df_infos = "Nenhum produto encontrado!"

    return df_infos

    
    
