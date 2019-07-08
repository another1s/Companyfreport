from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

ADDRESS = 'https://sc.hkexnews.hk/TuniS/www.hkexnews.hk/index_c.htm'


def searching_action(stock_code, browser):



    return



def doc_download():
	return



search_keys = '00001'
browser = webdriver.Chrome()
browser.get(ADDRESS)
searchbar = browser.find_element_by_xpath('//*[@id="searchStockCode"]').send_keys(search_keys)
time.sleep(3)
listbox = browser.find_element_by_xpath('//*[@id="autocomplete-list-0"]/div[1]/div[1]/table/tbody/tr[1]/td[2]/span').click()
time.sleep(3)
confirmbutton = browser.find_element_by_xpath('//*[@id="tab-panel-title-search"]/form/div/div[3]/a[3]').click()
time.sleep(3)

#print(browser.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[2]'))
#while (browser.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[2]')):
#	browser.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[2]').click()
#	time.sleep(2)


html=browser.page_source


soup=BeautifulSoup(html,'lxml')
pdf_files = soup.select('div[class="doc-link"]')

pdf_url_list = list()

print(type(pdf_files))
for f in pdf_files:
	print(type(f))
	print('\n')
	print(f.a['href'])
	pdf_url_list.append(f.a['href'])
	#pdf_url = f.find_next_sibling('a')
	#print(pdf_url)

with open("长和.txt", 'w') as f:
	for pdf in pdf_url_list:
		prefix = "https://www1.hkexnews.hk"
		f.write(prefix+pdf)
		f.write('\n')

#print(button)