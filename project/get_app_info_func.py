#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:18:48 2021

@author: viktoriia_vakhrina
"""



import parsing_functions
    
    
def get_devices(s, list_of_devs):
    '''
    get list of devices from text
    returns string
    '''
    devs = []
    for d in list_of_devs:
        if s.find(d) > -1:
            devs.append(d)
    return ' '.join(devs)


def get_app_info(link):
    '''
    Returns dictionary
    '''
    try:
        soup = parsing_functions.get_soup_obj(link)


        all_app_info = {} # where all information will be stored
        app_info = soup.find_all('dd', {'class':'information-list__item__definition'})
        
        
        #size -> string (number and measure)
        
        size_parent = soup.find('dt', string = 'Size')
        size = size_parent.findNext('dd').string
        all_app_info['app_size'] = size
        
        # category -> string
        category_parent = soup.find('dt', string = 'Category')
        category = category_parent.findNext('dd').text.strip()
        all_app_info['app_cat'] = category  

        # devices -> string ('iPhone', 'iPad', 'iPod')
        list_of_devices = ['iPhone', 'iPad', 'iPod', 'Mac']
        s = app_info[3].text
        devs = get_devices(s, list_of_devices)
        all_app_info['devices'] = devs 

        # languages -> string
        lang_parent = soup.find('dt', string = 'Languages')
        lang = lang_parent.findNext('p').string
        all_app_info['languages'] = lang
        
        
        # Age -> str
        age_parent = soup.find('dt', string = 'Age Rating')
        age = age_parent.findNext('dd').text
        all_app_info['age'] = age 
        
        # Price -> float
                
        price_parent = soup.find('dt', string = 'Price')
        price = price_parent.findNext('dd').string      
        if price == 'Free':
            price = 0
        else:
            price = price[1:]
            price = float(price)  
        all_app_info['price'] = price 
        
        
        # supports 
        supports_info = soup.find('ul', {'class':'supports-list l-row'}).find_all('li')
        support_list = []
        for i in supports_info:
            sup_item = i.h3.text.strip()
            support_list.append(sup_item)
        all_app_info['supports'] = ','.join(support_list)
        
        # rating
        try:
            rating = soup.find('span', {'class':'we-customer-ratings__averages__display'}).text
            all_app_info['rating'] = rating
        except:
            all_app_info['rating'] = 0
        
        
        # Number of reviews
        try:
            total_reviews = soup.find('div', {'class':'we-customer-ratings__count small-hide medium-show'}).text
            total_reviews = total_reviews.rstrip(' Ratings')
            all_app_info['num_reviews'] = total_reviews 
        except:
            all_app_info['num_reviews'] = 0
        
        
        # Description
        description = soup.find('div', {'class':"section__description"}).p.text
        description = description.replace('\\', "\'\'")
        description = description.replace("'", "\'\'")
        all_app_info['description'] = description 
        
        # in-app purch
        # Page contains 'more' button for in-app purchases if there are more than 3 of them
        
        if soup.find('button', {'class':'we-truncate__button we-truncate__button--top-offset link'}) is None:
            list_of_purchases = soup.find('ol', {'class':'list-with-numbers'})
            if list_of_purchases is None :
                number_of_purchases = '0'
            else:
                number_of_purchases = len(list_of_purchases.find_all('li'))
        else:
            number_of_purchases = '3+'
        all_app_info['number_of_purch'] = number_of_purchases     
        
        # developer name and href
        developer_tag = soup.find('h2',{'class':'product-header__identity app-header__identity'})
        developer_name = developer_tag.a.text.strip()
        if len(developer_name) > 0:
            developer_href = developer_tag.a['href']
        else:
            developer_name = soup.find('dt', string = 'Seller').findNext('dd').string.strip()
            developer_href = ''
        all_app_info['dev_name'] = developer_name 
        all_app_info['dev_href'] = developer_href
        return all_app_info
    
    except Exception as e:
        f = open('log.txt', 'a')
        f.write(link +' '+str(e) + '\n')
        f.close()
        all_app_info = {}
        return None
    
    