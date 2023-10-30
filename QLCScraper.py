# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:10:15 2023

@author: mreginiano
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from helpers import PM_Process as pp


def getpropertyinfo(url):
    try:
        prop_dict = {}
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        prop_dict['URL'] = url
        prop_dict['RefNo'] = soup.find('h5', class_ = 'retail-pink-small').text.strip()
        prop_dict['Type'] = soup.find('h2').text.split('in')[0]
        prop_dict['Location'] = soup.find('h2').text.split('in')[1]
        prop_dict['Location'] = prop_dict['Location'].strip()
        details_window = soup.find('div', class_ = 'col-md-6 col-lg-4 col-sm-12').find_all('div', class_ = 'row')
        prop_dict['SQM'] = details_window[0].find_all('h2', class_ = 'vat-mo')[0].text.replace('sqm', '')
        prop_dict['SQM'] = prop_dict['SQM'].strip()
        prop_dict['Price'] = details_window[0].find_all('h2', class_ = 'vat-mo')[1].text.replace('€','').replace('/mo', '').strip()
        prop_dict['Agent'] = soup.find('h3', class_ = 'agent-name-text').text.strip()
        prop_dict['PricePerSQM'] = details_window[1].find('h2', class_ = 'vat-mo').text.replace('€','')
        prop_dict['PricePerSQM'] = prop_dict['PricePerSQM'].strip()
        features_window = soup.find('div', class_ = 'features-white').find('div', class_ = 'tab-content').find_all('div', class_ = 'col-md-3 col-6')
        prop_dict['Features'] = [feat.text.strip() for feat in features_window]
        description_window = soup.find('div', class_ = 'features-white').find('div', class_ = 'tab-content').find('div', class_ = 'tab-pane fade')
        prop_dict['Description'] = description_window.text.strip()
    except:
        pass
    
    return prop_dict
        
url = 'https://qlc.com.mt/'
service = Service('/Users/michaelreginiano/Documents/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service)

driver.get(url)
time.sleep(1)
locality = driver.find_element(By.XPATH, '//*[@id="home-search-form-rent"]/div[1]/span/span[1]/span/ul/li/input')
locality.send_keys('All')
locality.send_keys(Keys.ENTER)

prop_type = driver.find_element(By.XPATH, '//*[@id="home-search-form-rent"]/div[2]/span/span[1]/span/ul/li/input')
prop_type.send_keys('Any')
prop_type.send_keys(Keys.ENTER)

searchbtn = driver.find_element(By.XPATH, '//*[@id="home-search-form-rent"]/button').click()

count = 0
#n = 1
prop_list = []
while count < 1000:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    properties = soup.find_all('div', class_ = 'col-md-4 property-count')
    prop_urls = [prop.find('a', class_ = 'properties-box').get('href') for prop in properties]
    #print('Iteration: '+str(n)+'--- Prop_urls length: '+str(len(prop_urls)))

    for i in range(count, len(prop_urls)):
        start_time = time.time()
        prop = getpropertyinfo(url+prop_urls[i])
        prop_list.append(prop)
        count+=1
        print(count)
        print('--- %s seconds ---' %(time.time() - start_time))

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(1)
    #n+=1
    
df = pd.DataFrame(prop_list)

#df['Features'] = pp.clean_Feats(df)
feats = ['air conditioning', 'ground floor', 'open plan', 'permit in hand', 'main street', 'furnished', 'lift', 'modern', 'kitchenette', 'storage', 'parking', 'cctv', 'basement']
for f in feats:
    df[f] = pp.extract_FeatList(df, f)

df.to_csv('QLC Rent - {}.csv'.format(date.today()))



# len(df['RefNo'])
# len(list(set(df['RefNo'])))

# prop_dict = {}
# r = requests.get(url+prop_urls[0])
# soup = BeautifulSoup(r.content, 'lxml')
# prop_dict['URL'] = url
# prop_dict['RefNo'] = soup.find('h5', class_ = 'retail-pink-small').text
# prop_dict['Type'] = soup.find('h2').text.split('in')[0]
# prop_dict['Location'] = soup.find('h2').text.split('in')[1]
# details_window = soup.find('div', class_ = 'col-md-6 col-lg-4 col-sm-12').find_all('div', class_ = 'row')
# prop_dict['SQM'] = details_window[0].find_all('h2', class_ = 'vat-mo')[0].text.replace('sqm', '')
# prop_dict['Price'] = details_window[0].find_all('h2', class_ = 'vat-mo')[1].text.replace('€','').replace('/mo', '')
# prop_dict['Agent'] = soup.find('h3', class_ = 'agent-name-text').text
# prop_dict['PricePerSQM'] = details_window[1].find('h2', class_ = 'vat-mo').text.replace('€','')
# features_window = soup.find('div', class_ = 'features-white').find('div', class_ = 'tab-content').find_all('div', class_ = 'col-md-3 col-6')
# features_window
# description_window = soup.find('div', class_ = 'features-white').find('div', class_ = 'tab-content').find('div', class_ = 'tab-pane fade')
# description_window.text.strip()
# prop_dict['Features'] = [feat.text for feat in features_window.find_all('div', class_ = 'col-md-3 col-6')]
# prop_dict