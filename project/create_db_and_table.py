#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create database and tables

@author: viktoriia_vakhrina
"""




import sqlite3
from config import DB_NAME


try:
    conn = sqlite3.connect(DB_NAME)
    curs = conn.cursor()
    
    sql_drop_if_exists = '''
                        DROP TABLE IF EXISTS Developer;
                        DROP TABLE IF EXISTS Category;
                        DROP TABLE IF EXISTS App
                        '''
    
    curs.executescript(sql_drop_if_exists)
    conn.commit()
    
    sql_text = '''CREATE TABLE Developer (
                          dev_id INTEGER PRIMARY KEY,
                          dev_name TEXT,
                          dev_href TEXT,
                          dev_rating REAL              
                          );
                          
                CREATE TABLE Category (
                    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cat_name TEXT NOT NULL,
                    cat_href TEXT NOT NULL
                        );
                
                CREATE TABLE App (
                    app_id INTEGER PRIMARY KEY,
                    app_name TEXT NOT NULL,
                    app_href TEXT NOT NULL,
                    app_size REAL NOT NULL,
                    app_cat INTEGER NOT NULL,
                    developer TEXT NOT NULL,
                    devices TEXT NOT NULL,
                    languages INTEGER NOT NULL,
                    age TEXT,
                    price REAL NOT NULL,
                    supports TEXT,
                    rating REAL NOT NULL,
                    num_reviews INTEGER,
                    description TEXT,
                    number_of_purch TEXT,
                    
                    FOREIGN KEY (app_cat) REFERENCES Category (cat_id),
                    FOREIGN KEY (developer) REFERENCES Developer (dev_id)
                    )'''
    curs.executescript(sql_text)
    conn.commit()
    conn.close()
except Exception as e:
    print(e)
    conn.close()
    