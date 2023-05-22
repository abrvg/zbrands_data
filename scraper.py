import pandas as pd
import requests
from random import randint
from bs4 import BeautifulSoup
import json
from datetime import datetime

#User agents to avoid being banned
user_agents =['Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 Mobile/14G60 Safari/602.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16C101',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1']


# Select a rando user agent
def get_useragent():
  random_user = randint(1,len(user_agents)-1)
  return user_agents[random_user]

#check the connection status
def connection_status(response):
   if response.status_code == 200:
      return "Active_connection"
   else:
      return "Failed_connection"
   

# Filter the data in the htlm response
def filter_response(response):
   soup = BeautifulSoup(response.content, 'html.parser')
   s = soup.find('script', type='application/json')
   json_object = json.loads(s.contents[0])
   filt = json_object['query']['data']['mainContent']['records'][0]['allMeta']['variants']
   #stores = json_object['query']['data']['mainContent']['records'][0]['allMeta']['inStockStores']   
   
   return filt

#Once the data is filter, select the important fields and return a data frame
def get_df(response):
   filt = filter_response(response)
   execution_day = str(datetime.now())
   extract_list = []
   for i in range(len(filt)):
      product = {'skuId': filt[i]['skuId'],
                 'skuName': filt[i]['skuName'],
                 'size': filt[i]['size'],
                 'promoPrice': filt[i]['prices']['promoPrice'],
                 'salePrice': filt[i]['prices']['salePrice'],
                 'listPrice': filt[i]['prices']['listPrice'],
                 'sortPrice': filt[i]['prices']['sortPrice'],
                 'hasValidOnlineInventory': filt[i]['hasValidOnlineInventory'],
                 'thumbnailImage': filt[i]['thumbnailImage'],
                 'consultedDay': execution_day
                 }
      
      extract_list.append(product)
      df = pd.DataFrame(extract_list)
      
   return df

url_address = 'https://www.liverpool.com.mx/tienda/pdp/colchón-luuna-original-plus-confort-suave/1111799151?skuid=1111799161'
agent_header = ({'User-Agent': get_useragent(), 'Accept-language':'es-MX'})
response = requests.get(url_address,
                           headers=agent_header,
                           timeout=3)

get_df(response).to_csv("example.csv")


