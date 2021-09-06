# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import os
from selenium import webdriver
from Nara import nara_market
from Alio import alio_bidinfo
import telegram

#function to read txt files and parse the list
def txt_reader(name):
    with open(name, 'rt', encoding="UTF-8") as f:
        lines = [line.rstrip() for line in f]

    return lines


# 크롬 옵션 세팅
csv_filename = '/home/bidding/Documents/BidCrawler/입찰공고목록.csv'
localdir = os.path.dirname(os.path.realpath(csv_filename))
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
prefs = {"download.default_directory": localdir}
chromeOptions.add_experimental_option("prefs", prefs)

# 기존 받은 파일이 있으면 삭제한다.
if os.path.isfile(csv_filename):
    os.remove(csv_filename)

# 크롬 드라이버로 크롬을 실행한다.
driver = webdriver.Chrome(executable_path='/home/bidding/Documents/BidCrawler/chromedriver', options=chromeOptions)
print('Chrome Driver launched..')

# 검색어 목록 읽기
query = txt_reader('/home/bidding/Documents/BidCrawler/BidKeywords.txt')
print('BidKeywords read')

try:
    print('Let''s go to Nara Market')
    if not nara_market(driver, query):
        print('Error for Nara Market')
except Exception as e:
    print('Error for Nara Market')

try:
    print('Let''s go to ALIO Site')
    if not alio_bidinfo(driver, query, csv_filename):
        print('Error for ALIO Bidinfo')
except Exception as e:
    print('Error for ALIO Bidinfo')

driver.close()



''' Telegram Bid Assist Bot
You will find it at t.me/NSE_BidBot. 
You can now add a description, about section and profile picture for your bot, see /help for a list of commands. 
By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. 
Just make sure the bot is fully operational before you do this.
Use this token to access the HTTP API:
1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4
Keep your token secure and store it safely, it can be used by anyone to control your bot.
Jungsup's chat_id=167233193
'''
