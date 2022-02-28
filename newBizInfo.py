import pandas as pd
import requests
from bs4 import BeautifulSoup
import telegram
import urllib
import datetime
from datetime import timedelta

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

root_path = '/Users/james/Documents/GitHub/MyBots/'


query = txt_reader(root_path + 'BidKeywords.txt')
print('Debug #12')

# bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
print('BizInfo>> Bot Connected..')
bot.sendMessage(chat_id=167233193, text='>>>>> '+str(datetime.date.today())+' >>>>>>>')

for keyword in query:
    url = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?hashCode=&rowsSel=6&rows=30&cpage=1&cat=&article_seq=&pblancId=&schJrsdCodeTy=&schEndAt=N&condition=pldirJrsdCodeNm&keyword='+urllib.parse.quote(keyword)
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
                link = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/'+each.find('a')['href']
                links.append(link)
                print(link)
            except:
                pass

    df['Link'] = links

    df_new = df[df['등록일'].apply(autoconvert_datetime) > str(datetime.date.today()-timedelta(days=5))]

    print(df_new)
    if df_new.shape[0] > 0:
        bot.sendMessage(chat_id=167233193, text=keyword)
        # notify new info / within a 5days
        for idx, row in df_new.iterrows():
            bot.sendMessage(chat_id=167233193, text=row['지원사업명']+'\n'+row['Link'])

bot.sendMessage(chat_id=167233193, text='======= '+str(datetime.date.today())+' =======')