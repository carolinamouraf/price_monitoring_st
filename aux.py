import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



def save_item(product, price_farm):
    with open('../data/saved_products.txt', 'a') as file:
        file.write(str(product) + "@" + str(price_farm) + '\n')
        # adicionar opção de checar se o produto já existe no arquivo e, caso exista, oferecer substituição
        # OBS: criar função de atualizar txt

def open_item_list():
    search_dic = {}
    with open('../data/saved_products.txt', 'r') as file:
        items_list = file.readlines()

        for line in items_list:
            splitted = line.split('@')
            if len(splitted) == 2:
                prod = splitted[0]
                price = splitted[1]

                price = price.replace(',','.')
                price = float(price)
                
                search_dic[prod] = price

    return search_dic


def mercado_livre(product):
    '''Responsible for getting the product's prices and payment conditions from mercado livre's website'''
    
    def create_url(key_word):
        key_word = str(key_word)
        url_search = key_word.replace(" ", "%20")
        search = key_word.replace(" ", "-")

        url = "https://lista.mercadolivre.com.br/" + str(search) + "#D[A:" + str(url_search) + "]"

        return url

    
    # Accessing the section on mercado livre's website

    url = create_url(product)
    page = requests.get(url)
    
    # Creating the soup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get the iformations from the classes: name, price, discount and payment method

    class1 = "ui-search-item__title"
    class2 = "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"
    class3 = "ui-search-price__discount"
    class4 = "ui-search-item__group__element ui-search-installments ui-search-color--BLACK"
    class5 = "ui-search-item__group__element ui-search-installments ui-search-color--LIGHT_GREEN"
    
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
    for item in name_disc:

        info_payment = item.replace('em', '$em$')
        info_payment = info_payment.split('$')

        info_price = item.split('|')

        info_discount = item.split(' ')

        if (np.isin('em', info_payment) == False) & (np.isin('OFF', info_discount) == False) & (np.isin('price', info_price) == False):
            if item in info_dict.keys():
                item_change = item + str(' OPÇÃO_2')
                info_dict[item_change] = ['price', 'discount', 'payment']
                prev_item = item_change
            else:
                info_dict[item] = ['price', 'discount', 'payment']
                prev_item = item

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
        df_infos = "nulo"
    else:
        df = pd.DataFrame.from_dict(info_dict, orient='index')
        df_infos = df.reset_index()
        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'DESCONTO_%', 2:'FORMA_PAGAMENTO'})
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
    
    return df_infos

def agrosolo(product):
    
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
        
    info_dict = {}
    for item in name_disc:

        info_payment = item.replace('PIX', '-PIX-')
        info_payment = info_payment.split('-')

        price_before = item.split('|')

        info_card = item.replace('ou', '-ou-')
        info_card = info_card.split('-')

        if (np.isin('PIX', info_payment) == False) & (np.isin('price_before', price_before) == False) & (np.isin('ou', info_card) == False):
            if item in info_dict.keys():
                item_change = item + str(' OPÇÃO_2')
                info_dict[item_change] = ['price_now', 'discount', 'credit_card', 'price_before']
                prev_item = item_change
            else:
                info_dict[item] = ['price_now', 'discount', 'credit_card', 'price_before']
                prev_item = item

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
    
    prod_discount = []
    for link in soup.find_all(class_=[class1,class4]): #finding the names at the title class in the code
        info = link.get_text()
        prod_discount.append(info)
         
    i = 0
    for item in prod_discount:
        info = item.split('%')
        if np.isin(' off', info) == True:
            product = prod_discount[i+1]
            info_dict[product][1] = info[0]
            i = i+1
        else:
            i = i+1
            pass
        
    # Creating the dataframe
    if len(info_dict) == 0:
        df_infos = "nulo"

    else:
        df = pd.DataFrame.from_dict(info_dict, orient='index')
        df_infos = df.reset_index()
        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'DESCONTO_%', 2:'FORMA_PAGAMENTO', 3:'PRECO_ORIGINAL'})
        df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].replace('discount', 0)
        df_infos['DESCONTO_%'] = df_infos['DESCONTO_%'].astype(float)
        df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].replace('price_before', 0)

        try:
            df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].str.replace(',', '.')
            df_infos['PRECO_ORIGINAL'] = df_infos['PRECO_ORIGINAL'].astype(float)
        except:
            pass

        mask = df_infos['PRECO_DESCONTO'] == 'price_now'
        df_infos = df_infos[~mask]
    
    
    return df_infos

def loja_agropecuaria(product):

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

    divs = []
    name_disc = []
    for link in soup.find_all(class_='desc position-relative'): #finding the names at the title class in the code
        info = link.get_text()
        name_disc.append(info)

    for item in name_disc:
        info_list = item.split('\n')
        divs.append(info_list)

    dic_infos = {}

    for item in divs:
        product_name = item[1].split('                            ')[1]
        dic_infos[product_name] = ['price', 'payment']
        
        product_price = item[2].split('                        ')[1].split('R$ ')[2].split(' ')[0]
        dic_infos[product_name][0] = product_price
        
        payment = item[3].split('ou ')[1]
        dic_infos[product_name][1] = payment

    # Creating the dataframe

    if len(dic_infos) == 0:
        df_infos = "nulo"
    else:
        df = pd.DataFrame.from_dict(dic_infos, orient='index')
        df_infos = df.reset_index()
        df_infos['DESCONTO_%'] = 0
        df_infos['PRECO_ORIGINAL'] = 0
        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'FORMA_PAGAMENTO'})
        df_infos = df_infos[['PRODUTO', 'PRECO_DESCONTO', 'DESCONTO_%', 'FORMA_PAGAMENTO', 'PRECO_ORIGINAL']]

        '''for i in df_infos.index:
            info = df_infos['PRECO_DESCONTO'][i]
            splitted = info.split('R')
            if np.isin('$', splitted) == True:
                price = splitted[0]
                df_infos['PRECO_DESCONTO'][i] = price
            else:
                pass'''

        #df_infos["PRECO_DESCONTO"]=df_infos["PRECO_DESCONTO"].str.replace(',','.')
        #df_infos["PRECO_DESCONTO"]=df_infos["PRECO_DESCONTO"].astype(float)
    
    return df_infos

def bom_cultivo(product):

    def create_url(key_word):
        key_word = str(key_word)
        url_search = key_word.replace(" ", "%20")
        
        url = "https://www.bomcultivo.com/busca?q=" + str(url_search)
        
        return url
    
    def splitting(lista, n):
        for i in range(0, len(lista), n):
            yield lista[i:i + n]
    
    url = create_url(product)
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    class1 = "product-name" 
    class2 = "price-big" 
    class3 = "type-payment-condiction"

    name_disc = []
    for link in soup.find_all(class_=[class1, class2, class3]): #finding the names at the title class in the code
        info = link.get_text()
        name_disc.append(info)


    info_dict = {}
    list_of_lists = splitting(name_disc, 3)
    for item in list_of_lists:
        prod_name = item[0]
        price = item[1].split('R$  ')[1].split('   ')[0]
        payment = item[2].split('ou ')[1]
        
        info_dict[prod_name] = [price, payment]

    if len(info_dict) == 0:
        df_infos = "nulo"
    else:
        df_infos = pd.DataFrame.from_dict(info_dict, orient='index')
        df_infos = df_infos.reset_index()
        df_infos = df_infos.rename(columns = {'index':'PRODUTO', 0:'PRECO_DESCONTO', 1:'FORMA_PAGAMENTO'})
        df_infos['DESCONTO_%'] = 0
        df_infos['PRECO_ORIGINAL'] = 0
        df_infos = df_infos[['PRODUTO', 'PRECO_DESCONTO', 'DESCONTO_%', 'FORMA_PAGAMENTO', 'PRECO_ORIGINAL']]

    return df_infos