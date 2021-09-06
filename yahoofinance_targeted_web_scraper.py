# -*- coding: utf-8 -*-
"""YaHooFinance_Targeted_Web_Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18e5YKvH2G0T_1oLnXXuSCPMXdIi8Jvic

#Dependencies
---
"""

import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import numpy as np

"""#Functions to gather stock information
---
"""

def web_content_div(web_content, class_path):
  web_content_div = web_content.find_all('div', {'class': class_path})#similar to finding tr
  '''
    This searches through all the div elements for the specific acompanying class_path attribute
  '''
  #print(web_content_div)
  try:
    spans = web_content_div[0].find_all('span')#similar to finding td, the list brackets are a formality as there is only one element in the list anyway.
    '''
      Once the specific div has been found, all span elements within that div (even if they are found within further nested divs) will be extracted
    '''
    texts = [span.get_text() for span in spans]#list of information from web page, for the example of the price and change, price is on the first span and change is the second span
  
  except IndexError as e:
    print(e)
    texts = []

  return texts

def price_scraper(web_content):
  texts = web_content_div(web_content, 'My(6px) Pos(r) smartphone_Mt(6px)')#This extracts the price and change in price
  if texts != []:
    price, change = texts[0], texts[1]
  else:
    price, change = [], []
  return price, change

'''def table_of_info_scraper(web_content):
  print('entered function')
  left_texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')#Class path of the table of information
  right_texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)')#Class path of the table of information
  texts = left_texts + right_texts
  if texts != []:
    print('entered if statement')
    for count, elem in enumerate(texts):
      if elem == 'Earnings Date':
        print(texts[count+1])'''
      

def real_time_price(stock_code):
  url: str = 'https://finance.yahoo.com/quote/'+stock_code+'?p='+stock_code+'&.tsrc=fin-srch'
  try: 
    page = requests.get(url)
    web_content = BeautifulSoup(page.text, 'html.parser')#soup
    
    price, change = price_scraper(web_content)
    #table_of_info_scraper(web_content)

  except ConnectionError as e:
    print(e)
    price, change = [], []

  return price, change

"""#Running Stock Scraper
---
"""

Stock: list = ['NFLX', 'FB']
df = pd.DataFrame(columns=['Date','Code','Price','Change'])
print(df)
for i in range(10):
  for stock_code in Stock:
    #information: list = []

    time_stamp = datetime.datetime.now() - datetime.timedelta(hours=5)#converting our time to NY time
    time_stamp = time_stamp.strftime('%y-%m-%d %H:%M:%S')#format the time
    information: list = [time_stamp] 

    price, change = real_time_price(stock_code)
    information.extend([stock_code])
    information.extend([price])
    information.extend([change])
    df.loc[len(df)] = information#adds the information to the datatframe
    #sleep time for 10 seconds

print(df)