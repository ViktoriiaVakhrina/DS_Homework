#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing the appstore page:
    1. Get names and links for all categories.
    2. Save name and category id to database. 
    3. Get names and links of all applications in every category.

@author: viktoriia_vakhrina
"""


# Get all categories with subcategories
import csv
import parsing_functions
import sqlite3
from config import DB_NAME, FILE_WITH_APPS

soup = parsing_functions.get_soup_obj('https://apps.apple.com/us/genre/ios/id36')

list_of_categories = soup.find('div', {'class':'grid3-column'}).find_all('li')
dict_of_categories = {}
for i in list_of_categories:
    name = i.a.text
    href = i.a['href']
    category_id = parsing_functions.get_id_from_href(href)
    dict_of_categories[category_id] = {'name': name, 'href': href}

#Delete categories with no or little apps:
# 6021 - id of category 'Magazines & Newspapers' (empty category)
# 6025 - id of category 'Stickers' (not relevant for analysis)
categories_to_delete = ['6021', '6025']

#ids of subcategories of Magazines & Newspapers' and 'Stickers'
subcats_to_delete = [k for k in dict_of_categories.keys() if len(k)==5]
categories_to_delete.extend(subcats_to_delete)
for k in categories_to_delete:
    del dict_of_categories[k]

# Write dict_of_cats to database:

conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()

for k, v in dict_of_categories.items():
    print(k,v)
    curs.execute('INSERT INTO Category VALUES(?,?,?)', (k, v['name'], v['href']))
conn.commit()
conn.close()



def get_all_apps(r, *dict_of_apps):
    '''
    Get id, name and links of all applications for each category
    
    Parameters
    ----------
    r: string, link to page category
    dict_of_apps: dictionary, where information should be saved. 
                If not given - creates new dictionary
    
    Returns
    ---------
    dictionary: key - app_id, value {'name':app_name, 'href':link of app}
    
    '''
    # if dictionary is given - add there, else - start new
    if dict_of_apps is ():
        apps_dict = {}
    else:
        apps_dict = dict_of_apps[0]
    soup = parsing_functions.get_soup_obj(r)
    # get list of tags that contain href and name of app
    list_of_tags = soup.find('div', {'id' : "selectedcontent"}).find_all('li')
    for el in list_of_tags:
        app_id = parsing_functions.get_id_from_href(el.a['href'])
        apps_dict[app_id]={'name': el.a.text ,'href': el.a['href']}
    return apps_dict

# Execution: getting apps dict for all categories
apps_dict = {}
for i in dict_of_categories.values():
    r = i['href']
    dict_app_ids = get_all_apps(r, apps_dict)
len(apps_dict)


# save ids, names and hrefs to csv


with open(FILE_WITH_APPS, mode = 'w') as f:
    fieldnames = ['app_id', 'name', 'href']
    writer = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    
    
    writer.writeheader()
    for i in dict_app_ids.items():
        i[1]['app_id']=i[0]
        writer.writerow(i[1])


