from bs4 import BeautifulSoup
import requests
from selenium import webdriver

ADDRESS = 'https://sc.hkexnews.hk/TuniS/www.hkexnews.hk/index_c.htm'


def searching_action(stock_code, browser):



    return

browser = webdriver.Chrome()
browser.get(ADDRESS)
button = browser.find_element_by_xpath('//*[@id="searchStockCode"]')
#print(button)