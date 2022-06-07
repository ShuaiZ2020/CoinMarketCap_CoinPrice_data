#! python3
from cgitb import text
from cmath import log
from doctest import Example
from math import fabs
from optparse import Option
from bs4 import BeautifulSoup
from numpy import average
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import re 
import pandas as pd
import datetime
from selenium.webdriver.support import expected_conditions as EC



options = Options()
open('not_work_url.txt','w')
options.add_experimental_option('debuggerAddress', 'localhost:9222')
driver = webdriver.Chrome(executable_path="C:\\Users\\szhu76\\AppData\\Local\\Microsoft\\WindowsApps\\chromedriver.exe",options=options)
nubmer_of_list = 0
filename = "C:\\Users\\zhu-s\\OneDrive\\code\\Crypto\\result\\"+str(datetime.date.today().strftime('%d-%b-%y'))+'_Crypto_price.csv'
print(filename)
open(filename,'w')

def convert():
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    return soup.find_all('div',class_= 'sc-1bqm8e1-1 sc-1bqm8e1-11 jGttJY')

def get_data(i,array1):
    value_soup = i.find('div',class_ = "sc-1bqm8e1-1 sc-1bqm8e1-16 jXRFjT")
    value_list = []
    if value_soup is not None:
        for i in value_soup(text=re.compile(r'$')):
            value_list.append(i)
        array1.append(value_list[1]) 
    else:
        array1.append(None)

def click_average_button():
    average_button = driver.find_elements_by_css_selector('button.x0o17e-0.DChGS.iazzsz-1.jCFojM.landed')
    for i in average_button:
        driver.execute_script("arguments[0].click();", i)
df = pd.DataFrame()
with open('C:\\Users\\zhu-s\\OneDrive\\code\\Crypto\\all_links.txt') as file:
    all_links = file.readlines()
    all_links = [line.rstrip() for line in all_links]

def main():
    
    first = True
    for url_number in range(100):
        # time.sleep(2)
        next_url = False 
        again = True
        date = []
        votes = []
        prediction_month = []
        values = []
        values_average = []
        url = all_links[url_number]
        
        Date = [datetime.date.today().strftime("%d-%b-%y")]*6
        refresh_number = 0
        while again:
            # time.sleep(0.5)
            driver.get(url)
            # click submit button
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 500)") 
            buttons = driver.find_elements_by_css_selector('button.x0o17e-0.DChGS.submit-btn')
            print(len(buttons))

            if refresh_number>5:
                with open('not_work_url.txt','a') as file:
                    file.write(url+'\n')
                next_url = True
                break
                

            if len(buttons) != 0:
                again = False
            else:
                refresh_number = refresh_number+1
                continue

            if len(buttons)==6:
                for i in buttons:
                    if i.text == 'Submit estimate':
                        time.sleep(random.randrange(2,5,1))
                        driver.execute_script("arguments[0].click();", i)
                        time.sleep(random.randrange(2,5,1))
                        submit_button = driver.find_element_by_css_selector('button.x0o17e-0.kzspeM.sc-174yupj-6.fkhPJ')
                        time.sleep(random.randrange(2,5,1))
                        driver.execute_script("arguments[0].click();", submit_button)
                        time.sleep(random.randrange(2,5,1))
                        break
            six_block = convert()
            # median_data
            for i in six_block:
                # date
                date_soup = i.find('div',class_="sc-1bqm8e1-1 sc-1bqm8e1-14 beBRnF")
                date.append(date_soup.get_text())
                # votes
                voted_number = i.find('div',class_="sc-1bqm8e1-1 sc-1bqm8e1-15 gzFcGs")
                str_voted_number = str(voted_number.get_text())
                votes.append(str_voted_number[0:-5])
                # value
                get_data(i,values) 
            
            # average_data
            click_average_button()
            average_six_block =convert()
            for i in average_six_block:
                get_data(i,values_average)
        coin_name = driver.find_element(by=By.CSS_SELECTOR, value= 'small.nameSymbol').text
        Crypto_symbol = [coin_name]*6
        nubmer_of_list = sum(x is not None for x in values)
        if next_url == True:
            continue
        # data cleaning 
        # predication data cleaning
        formated_date= []
        for i in date:
            formated_date.append(datetime.datetime.strptime(i, '%m/%d/%Y').strftime("%B-%y"))
        
        # votes data cleaning
        for i in range(nubmer_of_list):
            votes[i] = int(votes[i].replace(',',''))

        # values data cleaning  
        for i in range(nubmer_of_list):
            values[i] = values[i].replace(',','')
            values[i] = float(values[i].replace('$',''))
        # values_average data cleaning
        for i in range(nubmer_of_list):
            values_average[i] = values_average[i].replace(',','')
            values_average[i] = float(values_average[i].replace('$',''))
        # show

        data = {
                'Date':Date,
                "Crypto_symbol":Crypto_symbol,
                'Predication_month':formated_date,
                'Votes' : votes,
                'Values_median': values,
                'Values_average': values_average
                
            }
        # print(Date,Crypto_symbol,formated_date,votes,values,values_average)
        try:
            df_coin = pd.DataFrame(data)
        except:
            print('fail to dataframe')
            continue
        print('url number:'+ str(url_number))
        
        if first:
            df_coin.to_csv(filename, mode='a',index = False,encoding='utf-8')
            first = False
        else:
            df_coin.to_csv(filename, mode='a',header=False, index = False,encoding='utf-8')
            print('----')


if __name__ == "__main__":
    main()