#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:22:34 2021

@author: viktoriia_vakhrina
"""


import pandas as pd
import parsing_functions
import sqlite3
import random
from config import DB_NAME, FILE_WITH_APPS
from  get_app_info_func import get_app_info


# read file with information about all apps (id, href, name)
df = pd.read_csv(FILE_WITH_APPS)
df.head()
df.set_index('app_id', inplace=True)
print(df.shape)

# create connection and cursor objects
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()


# get list of columns in App table
curs.execute('pragma table_info(App)')
table_info = curs.fetchall()
table_columns = [i[1] for i in table_info]


# create list of apps in datapase
curs.execute('SELECT app_id FROM App')
list_of_saved_apps = curs.fetchall()
list_of_saved_apps  = [i[0] for i in list_of_saved_apps]


# delete from dataframe applications that are already in database
for el in list_of_saved_apps:
    df.drop(el, inplace = True)


def insert_dev_into_db(d, curs, conn):
    if len(d['dev_href'])>0:
        '''
        If developer is not known - we use seller name
        sellers do not have unique id, so we use random number
        '''
        dev_id = parsing_functions.get_id_from_href(d['dev_href'])
        if dev_id.find('?') > -1:
            dev_id = dev_id[:dev_id.find('?')]      
    else:
        dev_id = random.randint(0, 9000)
        # curs.execute('SELECT * FROM Developer WHERE dev_id = (?,)', (dev_id,))
        # while len(curs.fetchall())>0:
        #     dev_id = random.randint(0, 9000)
        #     curs.execute('SELECT * FROM Developer WHERE dev_id = (?)', (dev_id,))
    dev_name = d['dev_name']
    dev_href = d['dev_href']
    curs.execute('''INSERT INTO Developer (dev_id, dev_name, dev_href)
                  VALUES(?,?,?)''', (dev_id, dev_name,dev_href))
    conn.commit()
    return dev_id
# Get list of column names from table App



def insert_app_into_db(d, curs, table_cols):
    '''
    Add new row to db with app information
    '''
    try:
        values = [d[i] for i in table_cols]
        values[13] = values[13].replace('\\', "\'\'")
        values[13] = values[13].replace("'", "\'\'")
        curs.execute('INSERT INTO App VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', \
                         tuple(values))
    
    # in case of error - write error to file db_log2.txt
    except Exception as e:
        f = open('db_log2.txt', 'a')
        f.write(str(e) + '\n')
        f.close()
    




def get_foreign_key(col1, table, col2, val):
    '''

    Parameters
    ----------
    val : value to match 
    col1 : primary key column name
    table : name of table
    col2 : column where to look for match

    Returns
    -------
    

    '''
    query = "SELECT "+ col1 +" FROM " + table + " WHERE "+ col2 + " = '" + val + "'"
    curs.execute(query)
    result = curs.fetchone()
    if result is None:
        return None
    else:
        return result[0]


counter = 0

# df.iterrows: iterate through rows in df
# row(app_id, {'href:'app_href', name:'app_name')

for r in df.iterrows():
    if counter % 10 == 0:
        print(counter)
        curs.execute('SELECT COUNT(*) FROM App')
        print(curs.fetchone())
    app_href = r[1]['href']
    parsed_info = get_app_info(app_href) 
    if parsed_info is not None:
        dev_name = parsed_info['dev_name']
        
        # If developer name contains "  or ' it results in error in queries - replace
        if dev_name.find('"') >= 0:
            dev_name = dev_name.replace('"', '')
        if dev_name.find("'") >= 0:
            dev_name = dev_name.replace("'", "")
        
        # check if developer is already in database:
        parsed_info['developer'] = get_foreign_key('dev_id', 'Developer', \
                                                   'dev_name', dev_name)
        
        # if developer is not in database - add new row to Developer table
        if parsed_info['developer'] is None:
            parsed_info['developer'] = insert_dev_into_db(parsed_info, curs, conn)
            
        parsed_info['app_id'] = r[0]
        parsed_info['app_name'] = r[1]['name']
        parsed_info['app_href'] = app_href
        parsed_info['app_cat'] = get_foreign_key('cat_id', 'Category', \
                                                   'cat_name', parsed_info['app_cat'])
        insert_app_into_db(parsed_info, curs, table_columns)
        conn.commit()
    else:
        continue
    counter = counter+1

    
 
conn.close()
