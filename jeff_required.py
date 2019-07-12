from bs4 import BeautifulSoup
from selenium import webdriver
import time

ADDRESS = 'https://www.hkexnews.hk/index.htm'
def read_code(filename):
    res = list()
    with open(filename, 'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            #print(line)
            #data['companyname'] = line_split[1]
            res.append(line.strip('\n'))
    return res


def greedy_digging(doppler):
    try:
        loadmore = doppler.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[1]/ul/li/a')
        if loadmore:
            doppler.execute_script("arguments[0].click();", loadmore)
            greedy_digging(doppler)
    except:
        print("nothing more")


def crazydiamond(search_key):
    browser = webdriver.Chrome()
    browser.get(ADDRESS)
    # set up company name and code
    searchbar = browser.find_element_by_xpath('//*[@id="searchStockCode"]').send_keys(search_key)
    time.sleep(2)
    listbox = browser.find_element_by_xpath('//*[@id="autocomplete-list-0"]/div[1]/div[1]/table/tbody/tr[1]/td[2]/span').click()
    time.sleep(2)
    # limiting range of the searching : focus on financial statement
    openlist = browser.find_element_by_xpath('//*[@id="tier1-select"]/div/div/a').click()
    time.sleep(2)
    filetype = browser.find_element_by_link_text('Headline Category').click()
    time.sleep(2)
    opensublist = browser.find_element_by_xpath('//*[@id="rbAfter2006"]/div[1]/div/div/a').click()
    time.sleep(1)
    financial_statement = browser.find_element_by_link_text('Financial Statements/ESG Information').click()
    time.sleep(1)
    fetch_all = browser.find_elements_by_link_text('ALL')
    target = fetch_all[2].click()
    confirmbutton = browser.find_element_by_xpath('//*[@id="tab-panel-title-search"]/form/div/div[3]/a[3]').click()
    time.sleep(1)
    greedy_digging(browser)
    time.sleep(1)
    # while (browser.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[2]')):
    #	browser.find_element_by_xpath('//*[@id="recordCountPanel2"]/div[1]/div/div[2]').click()
    #	time.sleep(2)

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    pdf_files = soup.select('div[class="doc-link"]')
    pdf_url_list = list()
    #print(type(pdf_files))
    for f in pdf_files:
        #print(type(f))
        #print('\n')
        #print(f.a['href'])
        pdf_url_list.append(f.a['href'])
        # pdf_url = f.find_next_sibling('a')
        # print(pdf_url)

    with open('./fileurl/' + search_key + ".txt", 'w') as f:
        for pdf in pdf_url_list:
            prefix = "https://www1.hkexnews.hk"
            f.write(prefix + pdf)
            print(prefix+pdf)
            f.write('\n')
    browser.close()


search_keys = '00001'

comp_info = read_code('companycode.txt')

for i in comp_info:
    print(i)
    try:
        crazydiamond(i)
    except:
        pass
