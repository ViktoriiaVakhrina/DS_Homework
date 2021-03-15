#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 10:33:28 2021

@author: viktoriia_vakhrina
"""
import requests
from bs4 import BeautifulSoup

def get_soup_obj(href):
    '''
    
    Parameters
    ----------
    href : string (link of page to parse (get soup object))

    Raises
    ------
    Exception: if responce code is not 200 (page was not opened)

    Returns
    -------
    BeautifulSoup object - if no exceptions
    
    Bool (False) - if exception raised (text of exception is printed)

    '''
    try:
        r = requests.get(href, 'html')
        if r.ok:
            return BeautifulSoup(r.text, 'html.parser')
        else:
            print('Error occured')
            raise Exception
    except Exception as e:
        print(e)
        return False
    
def get_id_from_href(href):
    '''

    Parameters
    ----------
    href : string (link with 'id' at the end, 
                   f.e. 'https://apps.apple.com/us/genre/ios-games-word/id7019)

    Returns
    -------
    string: part of link after 'id'

    '''
    i = href.rfind('/id')+3
    return href[i:]