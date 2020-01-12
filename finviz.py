#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# The base url to search.
url = 'https://finviz.com/quote.ashx?t='

# Option to run the validation function.
validate = True

# The data to retrieve. Modify this list for the desired data.
data = ['Shs Float', 'Short Float', 'Avg Volume', 'Volume', 'ATR']

tickers = sys.argv[1:]
results = []

# Method to add validation for requirements. Returns true if all requirements are met.
def validation(ticker_data):
  shs_float_max = 25
  short_float_max = 15
  atr_min = 0.15

  shs_float = float(ticker_data['Shs Float'][:-1])
  short_float = float(ticker_data['Short Float'][:-1])
  atr = float(ticker_data['ATR'])

  return shs_float_max >= shs_float and short_float_max >= short_float and atr_min <= atr

def get_ticker_data():
  for ticker in tickers:
    page = requests.get(url + ticker)

    if(page.status_code == 200):
      ticker_results = {'Ticker': ticker}
      soup = BeautifulSoup(page.content, 'html.parser')

      for item in data:
        data_name_column = soup.find('td', text=item)
        data_name_value = data_name_column.nextSibling.text
        ticker_results[item] = data_name_value
      
      results.append(ticker_results)

def display_ticker_data(ticker_data):
  data_name = 'Name'
  data_value = 'Value'
  table = PrettyTable([data_name, data_value])
  table.align[data_name] = "r"
  table.align[data_value] = "l"

  table.add_row(['Ticker', ticker_data['Ticker'].upper()])

  for data_name in data:
    table.add_row([data_name, ticker_data[data_name]])

  print(table)
  print('\n')

def display_data():
  for ticker in results:
    if(validate):
      if(validation(ticker)):
        print('*** [PASSED VALIDATION] ***')
        display_ticker_data(ticker)
      else:
        print('*** [FAILED VALIDATION] ***')
        display_ticker_data(ticker)
    else:
      display_ticker_data(ticker)

get_ticker_data()
display_data()
