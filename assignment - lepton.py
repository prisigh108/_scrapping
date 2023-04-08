#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


# In[2]:


options = webdriver.ChromeOptions()
options.add_argument("--incognito")

DRIVER_PATH = "D:\dowloads\chromedriver_win32\chromedriver.exe"
service = webdriver.chrome.service.Service(executable_path=DRIVER_PATH)

url = 'https://www.nykaa.com/nykaa-stores-and-events-copy'
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(5) # Delays execution for 5 seconds to allow the page to load
html_source = driver.page_source # Gets the HTML source code of the web page
driver.quit() # Closes the browser window and terminates the webdriver session


# In[3]:


# Parse HTML content using Beautiful Soup
soup = BeautifulSoup(html_source, 'html.parser')

# Find all store detail boxes
store_boxes = soup.find_all('div', class_='nw_thumbnail nw_left nw-store-detail-box')


# In[4]:


# Create an empty list to store the data
data = []


# In[5]:


# Loop through each store box and extract data
for store_box in store_boxes:
    # Extract store name
    store_name = store_box.find('div', {'class': 'nw-store-box-name'}).contents[0].get_text()
    
    # Extract store address
    store_address = store_box.find('div', {'class': 'nw-store-box-address'}).text.strip()
    
    # Extract store opening hours
    store_hours = store_box.find('div', {'class': 'time-text'}).text.strip()
    store_hours = store_hours.replace('Open : ', '')
    
    # Append store data to list
    data.append({'Store Name': store_name,
                 'Address': store_address,
                 'Timings': store_hours})
  


# In[6]:


# Create a pandas DataFrame from the list of store data
df = pd.DataFrame(data)


# In[7]:


# Print the DataFrame
df.head()


# In[8]:


import re

def extract_phone_number(address_string):
    phone_regex = re.compile(r'\d{2}-\d{8}|\d{3}-\d{7}')
    phone_number = re.findall(phone_regex, address_string)
    if phone_number:
        return phone_number[0]
    else:
        return None


# In[9]:


df['Phone Number'] = df['Address'].apply(lambda x: extract_phone_number(x))


# In[10]:


df.head()


# In[11]:




df.to_csv('my_data.csv', index=False)


# In[19]:


from arcgis.gis import GIS
from arcgis.geocoding import geocode


# In[20]:


def cordinate(address):
    try:
        gis = GIS()
        # geocode the address
        location = geocode(address)[0]['location']
        # extract the latitude and longitude
        latitude = location['y']
        longitude = location['x']
        return latitude, longitude
    except:
        return None


# In[21]:


df['Coordinates'] = df['Address'].apply(lambda x: cordinate(x))


# In[22]:


df.head(10)


# In[23]:


df.to_csv('my_data_final.csv', index=False)


# In[ ]:





# In[ ]:




