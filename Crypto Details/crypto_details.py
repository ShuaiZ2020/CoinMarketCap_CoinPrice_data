import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

path_prefix = r"D:/Vasudev-Jingbo-Peiyu/data/Coinmarket details/"
prefix_link = 'https://coinmarketcap.com/currencies/'
coinmarket_mainpage = 'https://coinmarketcap.com'
process_count = 25
crypto_row_class = 'sc-16r8icm-0 escjiH'
details_loaded_class = 'sc-103s2w8-0 eAmmwa'
def getDriver():
    options = webdriver.FirefoxOptions()
    options.binary_location = r'C:\Users\vsridh20\AppData\Local\Mozilla Firefox\firefox.exe'
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(executable_path=r'D:\Vasudev-Jingbo-Peiyu\Programs\geckodriver.exe',
                               firefox_options=options)
    print("Got driver")
    return driver

def driverLink(driver, s):
    print("inside driver link")
    link = prefix_link + s
    driver.get(link)
    # time.sleep(5)


def scrape_header(driver, output_file, crypto, soup):
    rank = type = watchlist = website = source = whitepaper_link = tags = desc = None
    explorers = []
    community = []
    contracts = []
    audits = []
    tag_set = set()
    contract_set = set()
    tag_exclude_list = ['', 'View all']

    generic_button_class = 'link-button'
    rank_class = 'namePill namePillPrimary'
    watchlist_class = 'namePill'
    website_class = 'buttonName'
    explorer_button_class = 'sc-16r8icm-0 coGWQa'
    explorers_class = 'dropdownItem'
    source_code_class = 'buttonName'
    tags_class = 'tagBadge'
    desc_class = 'sc-16r8icm-0 jltEiJ'
    contract_class = 'sc-10up5z1-5 jlEjUY'
    contract_popup_class = 'tippy-content'
    contract_list_class = 'sc-16r8icm-0 sc-10up5z1-4 iMeCGL'
    audit_class = 'mainChainAddress'
    text_header_class = 'sc-1q9q90x-0 jCInrl h1___3QSYG'
    view_all_class = 'tagBadge___3p_Pk viewAll___2gJDj'
    see_more_class = 'sc-101ku0o-3 rAwXd'

    # base_container = driver.find_elements_by_xpath('//div[contains(@class, "grid full-width-layout")]')
    # base_container = driver.find_element_by_class_name('grid full-width-layout')
    # base_container = driver.find_element_by_xpath('//a[normalize-space()="Cryptocurrencies"]')
    # ActionChains(driver).move_to_element(base_container).perform()
    # view_all_button = driver.find_elements_by_xpath('//li[normalize-space()="View all"]')
    # print(view_all_button)
    # if len(view_all_button) > 0:
    #     ActionChains(driver).move_to_element_with_offset(view_all_button[0], -30, -30).perform()

    # Rank
    if soup.find(class_=re.compile(rank_class)):
        rank = soup.find(class_=re.compile(rank_class)).text.strip().replace('Rank #', '')
        if len(soup.find_all(class_=re.compile(watchlist_class))) >= 3:
            type = soup.find_all(class_=re.compile(watchlist_class))[1].text.strip()
            watchlist = soup.find_all(class_=re.compile(watchlist_class))[2].text.strip().replace('On', '')\
                .replace(' watchlists', '').replace(',', '')
    if soup.find(class_=re.compile(website_class)):
        website = soup.find(class_=re.compile(website_class)).text

    # Tags
    # Move cursor away so that popup does not block View all button
    # dummy = driver.find_element_by_xpath('//a[normalize-space()="Coins"]')
    # ActionChains(driver).move_to_element(dummy).perform()
    # view_all_button = driver.find_elements_by_xpath('//li[normalize-space()="View all"]')
    # print(view_all_button)
    # if len(view_all_button) > 0:
    #     ActionChains(driver).move_to_element(view_all_button[0]).click().perform()
    #     driver.implicitly_wait(1)
    #     if driver.find_element_by_class_name(tags_class):
    #         for tag in driver.find_elements_by_class_name(tags_class):
    #             if tag.text not in tag_exclude_list:
    #                 tag_set.add(tag.text)

    tags = list(tag_set)
    print(tags)
    # view_all_header = driver.find_element_by_class_name('sc-90sd2b-2 kZmzHf')
    # view_all_headers = driver.find_elements_by_xpath('//div[contains(@class, "sc-90sd2b-2 kZmzHf")]')
    # print(len(view_all_headers))
    # for view_all_header in view_all_headers:
    #     try:
    #         svg_element = view_all_header.find_element_by_css_selector("svg")
    #         ActionChains(driver).move_to_element(svg_element).click().perform()
    #         driver.implicitly_wait(1)
    #         break
    #     except WebDriverException as e:
    #         pass
            # print(e)

    # Community
    community_button = driver.find_elements_by_xpath('//button[normalize-space()="Community"]')
    # print(community_button)
    # driver.actions().move({'origin': explorers_button})
    # If it is a Community dropdown
    if len(community_button) > 0:
        ActionChains(driver).move_to_element(community_button[0]).perform()
        driver.implicitly_wait(1)
        if driver.find_element_by_name('Community'):
            # print("inside explorers")
            # print(driver.find_element_by_class_name(explorers_class))
            for row in driver.find_elements_by_name('Community'):
                # print(row.get_attribute('href'))
                community.append(row.get_attribute('href'))
    else:  # If it is not a dropdown
        buttons = driver.find_elements_by_css_selector('a')
        for button in buttons:
            if button.text == 'Community':
                community.append(button.get_attribute('href'))

    print("Community")
    print(community)
    # explorers_button = driver.find_element_by_xpath('//button[normalize-space()="Explorers"]')
    # # driver.actions().move({'origin': explorers_button})
    # ActionChains(driver).move_to_element(explorers_button).perform()
    # driver.implicitly_wait(1)
    #
    # if driver.find_element_by_class_name(explorers_class):
    #     # print("inside explorers")
    #     # print(driver.find_element_by_class_name(explorers_class))
    #     for row in driver.find_elements_by_class_name(explorers_class):
    #         # print(row.get_attribute('href'))
    #         if row.get_attribute('href'):
    #             explorers.append(row.get_attribute('href'))

    if driver.find_element_by_class_name(source_code_class):
        for b in driver.find_elements_by_class_name(source_code_class):
            if b.text == 'Source code':
                source = b.get_attribute('href')
            elif b.text == 'Whitepaper':
                whitepaper_link = b.get_attribute('href')

    if soup.find(class_=re.compile(contract_class)):
        for b in soup.find_all(class_=re.compile(contract_class)):
            link = b.select('a')
            # print(link)
            if link and len(link) > 0 and link[0]['href']:
                contract_set.add(link[0]['href'])
            elif b.find(class_=re.compile(audit_class)):
                audits.append(b.find(class_=re.compile(audit_class)).text)
            else:
                print("Neither audit nor contract")

    # contract_more_button = driver.find_elements_by_xpath('//button[normalize-space()="More"]')
    # if len(contract_more_button) > 0:
    #     ActionChains(driver).move_to_element(contract_more_button[0]).click().perform()
    #     driver.implicitly_wait(1)
    #     if len(driver.find_elements_by_class_name(contract_popup_class)) > 0:
    #         print("inside contract list")
    #         html = driver.page_source
    #         soup = BeautifulSoup(html, "html.parser")
    #         contract_popup = soup.find_all(class_=re.compile(contract_list_class))
    #         for row in contract_popup:
    #             contract_link = row.select('a')
    #             spans = row.select('span')
    #             obj = {"Name": spans[0].text}
    #             # text = "|".join([i.text for i in spans])
    #             if len(contract_link) > 0:
    #                 obj['Link'] = contract_link[0]['href']
    #                 contracts.append(obj)
    #             else:
    #                 contracts.append(obj)

    # contracts = list(contract_set)
    print(contracts)
    print(audits)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 1/2.5)")
    read_more_button = driver.find_elements_by_xpath('//button[normalize-space()="Read More"]')
    print("Read more button", read_more_button)
    if len(read_more_button) > 0:
        read_more_button[0].send_keys('Enter')
        # ActionChains(driver).move_to_element(read_more_button).perform()
        # ActionChains(driver).move_to_element(read_more_button).click().perform()
        driver.implicitly_wait(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    if soup.find(class_=re.compile(desc_class)):
        desc = soup.find(class_=re.compile(desc_class)).text
        desc = desc.replace('\n', ' ').replace('\r', ' ')
    # if driver.find_element_by_class_name(desc_class):
    #     desc = driver.find_element_by_class_name(desc_class).text
    if desc:
        print("Desc", desc[0:25])

    # print(crypto, rank, type, int(watchlist), website, source, audits, contracts, whitepaper_link, tags, explorers, community)
    return "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(crypto, rank, type, int(watchlist),website, source, audits,
                                                           json.dumps(contracts), whitepaper_link, tags, explorers, community, desc)


def scroll_to_bottom(driver, cur_page, output_file, p):
    parts = 10
    SCROLL_PAUSE_TIME = 1
    for i in range(parts+1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * " + str((cur_page-1)/cur_page + i/(cur_page * parts)) + ");")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        WebDriverWait(driver, SCROLL_PAUSE_TIME)

def scrape(driver, output_file, crypto):
    print("starting to scrape")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return scrape_header(driver, output_file, crypto, soup)


def driver_prog():
    driver = getDriver()
    header = "Crypto|Rank|Type|Watchlist|Website|Source|Audits|Contracts|Whitepaper link|Tags|Explorers|Community|Description"
    link = coinmarket_mainpage
    for i in range(1, 62):
        if i > 1:
            link = coinmarket_mainpage + "/?page=" + str(i)
        driver.get(link)
        driver.implicitly_wait(2)
        for i in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * {})".format(1/(i+1)))
            time.sleep(1)


        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # wait = WebDriverWait(driver, 60)
        # try:
        #     wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'h7vnx2-1 bFzXgL')))
        # except TimeoutException as e:
        #     print(e)
        # table = driver.find_element_by_class_name('h7vnx2-1 bFzXgL')
        # cryptos = table.find_elements_by_css_selector('td')
        # for crypto in cryptos:
        #     row = crypto.find_elements_by_class_name(crypto_row_class)
        #     print(row)
        #     if len(row) > 0:
        #         ActionChains(driver).move_to_element(crypto).click().perform()
        #         wait = WebDriverWait(driver, 60)
        #         try:
        #             wait.until(EC.element_to_be_clickable((By.CLASS_NAME, details_loaded_class)))
        #             print("present")
        #         except TimeoutException as e:
        #             print(e)

        # Test a crypto
        # crypto = 'polkadot'
        # driver.get(prefix_link + crypto)
        # output_file = path_prefix + "details.csv"
        # scrape(driver, output_file, crypto)

        table = soup.find(class_=re.compile('h7vnx2-1 bFzXgL'))
        tds = table.find_all(class_=re.compile('sc-16r8icm-0 escjiH'))
        for td in tds:
            is_header = True
            # print(td)
            links = td.find_all(class_=re.compile('cmc-link'))
            if len(links) > 0:
                print(links[0]["href"])
                driver.get(coinmarket_mainpage + links[0]["href"])
                crypto = links[0]["href"].split('/')[2]
                time.sleep(1)
                print("Loaded. Scraping ", links[0]["href"])
                output_file = path_prefix + "details.csv"
                ret = scrape(driver, output_file, crypto)
                with open(output_file, 'a', encoding="utf-8") as file:
                    if is_header:
                        file.write(header + '\n')
                        is_header = False
                    file.write(ret + '\n')

        # crypto = 'coinex-token'
        # driverLink(driver, crypto)
        # output_file = path_prefix + "details.csv"
        # print(output_file)
        # scrape(driver, output_file, crypto)
    driver.close()

driver_prog()
