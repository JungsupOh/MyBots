# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import telegram
import urllib
import datetime
from datetime import timedelta
import sys
import time



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

#function to read from html and send text to bot
def readHTMLtoBot(bot, url, titelName, dateName, keyword, linkBaseAddr):
    print(url)
    df = pd.read_html(url)[0]

 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='euc-kr')
    table = soup.find('table')

    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = linkBaseAddr + each.find('a')['href']
                links.append(link)
                print(link)
                break
            except:
                pass

    if (len(links)>0) :
        df['Link'] = links

    df_new = df[df[dateName].apply(autoconvert_datetime) > str(datetime.date.today()-timedelta(days=5))]

    print(df_new)
    if df_new.shape[0] > 0:
        bot.sendMessage(chat_id=167233193, text='(('+keyword+'))')  
        #bot.sendMessage(chat_id=5290341890, text='(('+keyword+'))')  

        # notify new info / within a 5days
        for idx, row in df_new.iterrows():
            if len(links) > 0 :
                bot.sendMessage(chat_id=167233193, text=row[titelName]+'\n'+row['Link'])
                #bot.sendMessage(chat_id=5290341890, text=row[titelName]+'\n'+row['Link'])
            else :
                bot.sendMessage(chat_id=167233193, text=row[titelName])
                #bot.sendMessage(chat_id=5290341890, text=row[titelName])

#function to read from html and send text to bot
def readHTMLtoBotTop5(bot, url, titelName, dateName, keyword, linkBaseAddr):
    print(url)
    df = pd.read_html(url)[0]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser', from_encoding='euc-kr')
    table = soup.find('table')

    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = linkBaseAddr + each.find('a')['href']
                links.append(link)
                print(link)
                break
            except:
                pass

    if (len(links)>0) :
        df['Link'] = links

    df_new = df.head(5)

    print(df_new)
    if df_new.shape[0] > 0:
        bot.sendMessage(chat_id=167233193, text='(('+keyword+'))')
        #bot.sendMessage(chat_id=5290341890, text='(('+keyword+'))')
        # notify new info / within a 5days
        for idx, row in df_new.iterrows():
            if len(links) > 0 :
                bot.sendMessage(chat_id=167233193, text=row[titelName]+'\n'+'('+row[dateName]+')\n'+row['Link'])
                #bot.sendMessage(chat_id=5290341890, text=row[titelName]+'\n'+'('+row[dateName]+')\n'+row['Link'])
            else :
                bot.sendMessage(chat_id=167233193, text=row[titelName]+'\n'+'('+row[dateName]+')')
                #bot.sendMessage(chat_id=5290341890, text=row[titelName]+'\n'+'('+row[dateName]+')')



if sys.platform.startswith("linux"):
    root_path = '/home/tebah/MyBots/'
else:
    root_path = '/Users/james/Documents/GitHub/MyBots/'

print('root_path :: ' + root_path)

query = txt_reader(root_path + 'BidKeywords.txt')
print('Debug #12')

# bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
print('BizInfo>> Bot Connected..')
bot.sendMessage(chat_id=167233193, text='>>>>> '+str(datetime.date.today())+' >>>>>>>')
#bot.sendMessage(chat_id=5290341890, text='>>>>> '+str(datetime.date.today())+' >>>>>>>')

for keyword in query:
    url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?hashCode=&rowsSel=6&rows=30&cpage=1&cat=&article_seq=&pblancId=&schJrsdCodeTy=&schEndAt=N&condition=pldirJrsdCodeNm&keyword='+urllib.parse.quote(keyword)
    linkBaseAddr = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/'
    titelName = '지원사업명'
    dateName = '등록일'
    linkName = 'Link'

    readHTMLtoBot(bot, url, titelName, dateName, keyword, linkBaseAddr)

'''
    print(url)
    df = pd.read_html(url)[0]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = linkBaseAddr + each.find('a')['href']
                links.append(link)
                print(link)
            except:
                pass

    df[linkName] = links

    df_new = df[df[dateName].apply(autoconvert_datetime) > str(datetime.date.today()-timedelta(days=5))]

    print(df_new)
    if df_new.shape[0] > 0:
        bot.sendMessage(chat_id=167233193, text='(('+keyword+'))')
        # notify new info / within a 5days
        for idx, row in df_new.iterrows():
            bot.sendMessage(chat_id=167233193, text=row[titelName]+'\n'+row[linkName])
'''

time.sleep(10)
## 단순히 테이블로 되어 있는 페이지들.. 순차 방문..

#NIPA 
readHTMLtoBot(bot, 'https://www.nipa.kr/main/selectBbsNttList.do?bbsNo=2&key=122', '제목', '작성일', 'Nipa', 'https://www.nipa.kr/main/')
time.sleep(10)

#한국발명진흥회 
readHTMLtoBot(bot, 'https://www.kipa.org/kipa/notice/kw_0403_01.jsp', '제목', '등록일', '한국발명진흥회', 'https://www.kipa.org/kipa/notice/kw_0403_01.jsp')
time.sleep(10)

#대전정보문화산업진흥원
readHTMLtoBot(bot, 'http://www.dicia.or.kr/sub.do?menuIdx=MENU_000000000000056', '제목', '작성일', '대전정보문화산업진흥원', 'http://www.dicia.or.kr/')
time.sleep(10)

#대전지식재산센터 
readHTMLtoBot(bot, 'https://www2.ripc.org/regional/notice/daejeon/bizNoticeList.do', '제목', '등록일', '대전지식재산센터', 'https://www.djtp.or.kr/')
time.sleep(10)

#IITP top5
readHTMLtoBotTop5(bot, 'https://www.iitp.kr/kr/1/business/businessApiList.it?pageIndex=0&pageSize=10&searchText=&searchField=all', '공고명', '접수기간', 'IITP Top5', '')


bot.sendMessage(chat_id=167233193, text='======= '+str(datetime.date.today())+' =======')
#bot.sendMessage(chat_id=5290341890, text='======= '+str(datetime.date.today())+' =======')
