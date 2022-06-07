""" 
Author: Shuai Zhu 
description: scraping the coin details form coinmarketcap.

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By

def open_driver():
    options = Options()
    options.add_experimental_option('debuggerAddress', 'localhost:9222')
    driver = webdriver.Chrome(executable_path="C:\\edgedriver_win64\\chromedriver",options=options)
    return driver
def get_data(driver,url):
    driver.get(url)

def add_to_dict(source_dict,dest_dict):
    key,value = list(source_dict.items())[0]
    dest_dict[key].append(value)
    # print(dest_dict)

first = True
open('coin_detail.csv','w')


def get_basic_info(driver,url):
    driver.get(url)
    div = driver.find_element(by=By.CSS_SELECTOR, value= 'div.sc-16r8icm-0.sc-10up5z1-1.eUVvdh')
    li = div.find_elements(by=By.CSS_SELECTOR, value= 'li')
    url_list = url.split('/')
    coin_name = url_list[4]
    detail = {
        'crypto': coin_name,
        'CoinMarketCap link':url,
        'Coin link':[],
        'Explorers':[],
        'Whitepaper':[],
        'Community':[],
        'Source code':[],
        'Chat':[],
    }
    for index in range(len(li)):
        
        try:
            i = li[index]
            link_button = i.find_element(by=By.CSS_SELECTOR, value= 'a.link-button')
            button_name = i.find_element(by=By.CSS_SELECTOR, value= 'div.buttonName')
            if index == 0:
                info = {'Coin link':str(link_button.get_attribute('href'))}
            else:
                info = {str(button_name.text):str(link_button.get_attribute('href'))}

            
            add_to_dict(info,detail)
            # print(info)
            # print('---')
        except:
            try:
                
                button = i.find_element(by=By.CSS_SELECTOR, value= 'button.link-button')
                webdriver.ActionChains(driver).move_to_element(button).perform()
                # print(i.get_attribute('outerHTML')) 
                link_buttons = i.find_elements(by=By.CSS_SELECTOR, value= 'a.dropdownItem')
                
                for link_button in link_buttons:
                    # print(link_button.get_attribute('outerHTML'))
                    info = {str(link_button.get_attribute('name')):str(link_button.get_attribute('href'))}
                    add_to_dict(info,detail)
                    # print(info)
                # print('---')
            except:
                # print('---')
                continue
            
    
    for i in range(2,8):
        key,value = list(detail.items())[i]
        detail[key] = [', '.join(detail[key])]
    return detail
def write_to_csv(df):
    global first
    if first:
        df.to_csv('coin_detail.csv', mode='a',index = False,encoding='utf-8')
        first = False
    else:
        df.to_csv('coin_detail.csv', mode='a',header=False, index = False,encoding='utf-8')

def get_tag(driver,url):
    driver.get(url)
    try:
        button_viewall = driver.find_element(by = By.CSS_SELECTOR, value = 'li.tagBadge.viewAll')
        driver.execute_script("arguments[0].click();", button_viewall)
        tags = driver.find_element(by = By.CSS_SELECTOR, value = 'div.sc-16r8icm-0.csifPj')
        tags_list = tags.find_elements(by = By.CSS_SELECTOR, value = 'div.sc-16r8icm-0.hgKnTV')
        tag_dict = {}
        for tag in tags_list:
            modal_heading = tag.find_element(by = By.CSS_SELECTOR, value = 'h6.modalHeading').get_attribute('innerHTML')
            tagbage = tag.find_elements(by = By.CSS_SELECTOR, value ='div.tagBadge')
            tagbage_list = []
            for i in tagbage:
                tagbage_list.append(i.get_attribute('innerHTML'))
            tag_dict = tag_dict|{modal_heading:tagbage_list}
            # print(modal_heading)
            # print(tagbage_list)
    except:
        content = driver.find_elements(by = By.CSS_SELECTOR, value = 'div.sc-16r8icm-0.sc-10up5z1-1.gGKCJe')[-1]
        tag_dict = []
        try:
            tags_list = content.find_element(by = By.CSS_SELECTOR, value = 'ul.content').find_elements(by = By.CSS_SELECTOR, value = 'div.tagBadge')
            for tag in tags_list:
                tag_dict.append(tag.get_attribute('innerHTML'))
        except:
            print('no tags')
    return {'tag':[str(tag_dict)]}

def main():
    global first
    driver = open_driver()
    with open('all_links - Copy.txt') as file:
        all_links = file.readlines()
        all_links = [line.rstrip() for line in all_links]
    for i in range(100):
        url = all_links[i]
        basic_detail = get_basic_info(driver,url)
        tag_detail = get_tag(driver,url)
        detail = basic_detail|tag_detail
        df = pd.DataFrame(detail)
        write_to_csv(df)
        print(df)
    
        
if __name__ == "__main__":
    main()
