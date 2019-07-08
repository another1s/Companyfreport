from bs4 import BeautifulSoup
import requests
from selenium import webdriver
<<<<<<< HEAD
=======
import time


ADDRESS = 'https://www.hkexnews.hk/index_c.htm'


driver = webdriver.Chrome()
driver.get(ADDRESS)      
time.sleep(2) 

#driver.find_element_by_name('searchStockCode').send_keys('00001')
>>>>>>> regular commit

ADDRESS = 'https://sc.hkexnews.hk/TuniS/www.hkexnews.hk/index_c.htm'


def searching_action(stock_code, browser):



    return

browser = webdriver.Chrome()
browser.get(ADDRESS)
button = browser.find_element_by_xpath('//*[@id="searchStockCode"]')
#print(button)