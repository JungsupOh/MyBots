import pandas as pd
import requests
from bs4 import BeautifulSoup
import telegram
import urllib
import datetime
from datetime import timedelta
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def autoconvert_datetime(value):
    formats = ['%Y.%m.%d', '%m/%d/%Y', '%m-%d-%y']  # formats to try
    result_format = '%Y-%m-%d'  # output format
    for dt_format in formats:
        try:
            dt_obj = datetime.datetime.strptime(value, dt_format)
            return dt_obj.strftime(result_format)
        except Exception as e:  # throws exception when format doesn't match
            pass
    return value  # let it be if it doesn't match


#function to read txt files and parse the list
def txt_reader(name):
    with open(name, 'rt', encoding="UTF-8") as f:
        lines = [line.rstrip() for line in f]

    return lines

if sys.platform.startswith("linux"):
    root_path = '/home/tebah/MyBots/'
else:
    root_path = '/Users/james/Documents/GitHub/MyBots/'

print('root_path :: ' + root_path)

# bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
print('BizInfo>> Bot Connected..')
bot.sendMessage(chat_id=167233193, text='..')
bot.sendMessage(chat_id=167233193, text='>>> Demoday Top 10 ('+str(datetime.date.today())+') >>>')

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": root_path}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument('headless')
chromeOptions.add_argument('no-sandbox')

# 크롬 드라이버로 크롬을 실행한다.
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chromeOptions)
print('Debug #Chrome Driver Initialized')

# 입찰정보 검색 페이지로 이동
url = 'http://main.demoday.co.kr/'
driver.get(url)
print(url+ " Connected")

li_list = driver.find_elements(by=By.XPATH, value="//li[@class='ranking_rankingItem__1a-1o']")
print(li_list)
print("::Debug 12::")

rank = 1
for each in li_list:
    a_tags = each.find_elements(by=By.TAG_NAME,value='a')
    print("debug11:: " +str(rank) + ' --> '+ str(len(a_tags)))
    #[0]:data [1]:image
    link=a_tags[0].get_attribute('href')
    #bot.sendMessage(chat_id=167233193, text=str(rank)+') \n'+a_tags[0].accessible_name+'\n'+link)
    bot.sendMessage(chat_id=167233193, text=str(rank)+') \n'+link)
    rank=rank+1


bot.sendMessage(chat_id=167233193, text='======= End of Demoday =======')