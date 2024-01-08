#!/usr/bin/env python
# coding: utf-8

# In[75]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'c32c5e74-8a4a-44d7-8d3c-2c08e9ad6edf',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)



#NOTE:
# I had to go in and put "jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10"
# Into the Anaconda Prompt to change this to allow to pull data

# If that didn't work try using the local host URL as shown in the video


# In[76]:


type(data)


# In[77]:


import pandas as pd

#This allows you to see all the columns, not just like 15
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[78]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[79]:


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    #Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'c32c5e74-8a4a-44d7-8d3c-2c08e9ad6edf',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df = pd.json_normalize(data['data'])
    df['Timestamp'] = pd.Timestamp
    df
    
    if not os.path.isfile(r'C:\Users\Srushti\Desktop\Practice\API2.csv'):
        df.to_csv(r'C:\Users\Srushti\Desktop\Practice\API.csv', header='column_names')
    else:
        df.to_csv(r'C:\Users\Srushti\Desktop\Practice\API.csv', mode='a',header=False)


# In[80]:


import os 
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60) 
exit()


# In[81]:


df72 = pd.read_csv(r'C:\Users\Srushti\Desktop\Practice\API.csv')
df72


# In[82]:


df


# In[83]:


#to be able to see the numbers in this case

pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[84]:


df


# In[85]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# In[86]:


df4 = df3.stack()
df4


# In[87]:


type(df4)


# In[88]:


df5 = df4.to_frame(name='values')
df5


# In[89]:


df5.count()


# In[90]:


#Because of how it's structured above we need to set an index. I don't want to pass a column as an index for this dataframe
#So I'm going to create a range and pass that as the dataframe. You can make this more dynamic, but I'm just going to hard code it

index = pd.Index(range(90))


# Set the above DataFrame index object as the index
# using set_index() function
df6 = df5.reset_index()
df6

# If it only has the index and values try doing reset_index like "df5.reset_index()"


# In[91]:


# Change the column name

df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[92]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['24h','7d','30d','60d','90d'])
df7


# In[93]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[94]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[96]:


# Now to do something much simpler
# we are going to create a dataframe with the columns we want

df10 = df[['name','quote.USD.price','timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10


# In[97]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df10)


# In[ ]:




