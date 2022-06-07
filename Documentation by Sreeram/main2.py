import json
import re
import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame()
flag = True
mean = []
median = []
exception = "There are not enough estimates to calculate the stats"
dates = [
         datetime.strptime('02-28-2022', '%m-%d-%Y').strftime("%B"),
         datetime.strptime('03-31-2022', '%m-%d-%Y').strftime("%B"),
         datetime.strptime('04-30-2022', '%m-%d-%Y').strftime("%B"),
         datetime.strptime('05-31-2022', '%m-%d-%Y').strftime("%B"),
         datetime.strptime('06-30-2021', '%m-%d-%Y').strftime("%B"),
         datetime.strptime('07-31-2022', '%m-%d-%Y').strftime("%B")]


def open_chrome(string):
    driver = uc.Chrome()
    with driver:
        driver.get(string)
    return driver


def login(username, password):
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[1]/div[1]/div/div[2]/button[1]').click()
    time.sleep(2)
    # find username/email field and send the username itself to the input field
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[3]/input").send_keys(username)
    # find password input field and insert password as well
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[4]/div[2]/input").send_keys(password)
    # click login button
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[6]/button").click()



def get_estimates():
    global mean, median, votes
    for i in range(1, 13, 2):
        try:
            median.append(driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div[3]/div[' + str(
                    i) + ']/div[3]/div/div[2]').text[1:])
            time.sleep(2)
            driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div[3]/div[' + str(
                    i) + ']/div[3]/div/div[4]/button[2]').click()
            time.sleep(1)
            mean.append(driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div[3]/div[' + str(
                    i) + ']/div[3]/div/div[2]').text[1:])
            time.sleep(1)
            votes.append(driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div[3]/div[' + str(
                    i) + ']/div[1]/div[1]/div[2]/div[1]').text)
        except:
            print(i)


def get_links(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines


def driver_code(filename, username, password, driver):
    global df, flag, exception, dates
    lines = get_links(filename)
    for i in lines[:]:
        print(i)
        global mean, median, votes
        mean = []
        median = []
        votes = []
        total_estimates = []
        month6_mean = []
        median6_median = []
        Accruacy6 = []
        driver.get(i)
        if flag == True:
            flag = False
            try:
                login(username, password)
            except:
                pass
        
        time.sleep(5)
        get_estimates()

        try:
            total_estimates = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div').text
        except:
            pass

        try:
            sixMonth_median = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div').text
        except:
            pass

        try:
            sixMonth_mean = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div[4]/div/div[2]/div').text
        except:
            pass

        try:
            sixMonth_accuracy = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[1]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div').text
        except:
            pass

        if (len(mean) < 1):
            continue
        print(mean)
        print(median)
        print(votes)
        dictionary = dict()
        dictionary['current_date'] = datetime.now().strftime("%d-%b-%y")
        dictionary['crypto'] = i

        # nov
        try:
            dictionary[dates[0] + '_mean'] = mean[0]
        except:
            dictionary[dates[0] + '_mean'] = exception

        try:
            dictionary[dates[0] + '_median'] = median[0]
        except:
            dictionary[dates[0] + '_median'] = exception

        try:
            dictionary[dates[0] + '_votes'] = votes[0]
        except:
            dictionary[dates[0] + '_votes'] = exception
        # dec
        try:
            dictionary[dates[1] + '_mean'] = mean[1]
        except:
            dictionary[dates[1] + '_mean'] = exception

        try:
            dictionary[dates[1] + '_median'] = median[1]
        except:
            dictionary[dates[1] + '_median'] = exception

        try:
            dictionary[dates[1] + '_votes'] = votes[1]
        except:
            dictionary[dates[1] + '_votes'] = exception
        # jan
        try:
            dictionary[dates[2] + '_mean'] = mean[2]
        except:
            dictionary[dates[2] + '_mean'] = exception

        try:
            dictionary[dates[2] + '_median'] = median[2]
        except:
            dictionary[dates[2] + '_median'] = exception

        try:
            dictionary[dates[2] + '_votes'] = votes[2]
        except:
            dictionary[dates[2] + '_votes'] = exception

        # feb
        try:
            dictionary[dates[3] + '_mean'] = mean[3]
        except:
            dictionary[dates[3] + '_mean'] = exception

        try:
            dictionary[dates[3] + '_median'] = median[3]
        except:
            dictionary[dates[3] + '_median'] = exception

        try:
            dictionary[dates[3] + '_votes'] = votes[3]
        except:
            dictionary[dates[3] + '_votes'] = exception

        # mar
        try:
            dictionary[dates[4] + '_mean'] = mean[4]
        except:
            dictionary[dates[4] + '_mean'] = exception

        try:
            dictionary[dates[4] + '_median'] = median[4]
        except:
            dictionary[dates[4] + '_median'] = exception

        try:
            dictionary[dates[4] + '_votes'] = votes[4]
        except:
            dictionary[dates[4] + '_votes'] = exception

        # april
        try:
            dictionary[dates[5] + '_mean'] = mean[5]
        except:
            dictionary[dates[5] + '_mean'] = exception

        try:
            dictionary[dates[5] + '_median'] = median[5]
        except:
            dictionary[dates[5] + '_median'] = exception

        try:
            dictionary[dates[5] + '_votes'] = votes[5]
        except:
            dictionary[dates[5] + '_votes'] = exception

        dictionary['total_estimates'] = total_estimates
        dictionary['sixMonth_median'] = sixMonth_median
        dictionary['sixMonth_mean'] = sixMonth_mean
        dictionary['sixMonth_accuracy'] = sixMonth_accuracy

        df = df.append(dictionary, ignore_index=True)
        time.sleep(2)


def save_data():
    global df
    today = datetime.now()
    today = today.strftime("%d-%b-%y") + "_scraped_data.xlsx"
    df[['February_mean', 'February_median', 'February_votes',
       'March_mean', 'March_median', 'March_votes', 'April_mean',
       'April_median', 'April_votes', 'May_mean',
       'May_median', 'May_votes','June_mean',
       'June_median', 'June_votes','July_mean', 'July_median',
       'July_votes','crypto', 'current_date',
       'sixMonth_accuracy', 'sixMonth_mean', 'sixMonth_median',
       'total_estimates']].to_excel(today)


if __name__ == '__main__':
    driver = open_chrome("https://www.google.com/")

    driver_code(filename="all_links.txt", username="sreeram2306@gmail.com", password="Hydusa@1998", driver=driver)

    save_data()
