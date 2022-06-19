# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import datetime

import telegram
from styleframe import StyleFrame
import pandas as pd
import time


bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
print('Bot Connected..')

bot.sendMessage(chat_id=-1001681320740, text='Hello~~ 안녕하세요..')
# bot.sendDocument(chat_id=-597319317, document=open('/home/bidding/Documents/BidCrawler/ALIO_BidInfo.xlsx', 'rb'))
# finger.ai 매출 채널:   -1001681320740
# NSE Bidding 채널:     -1001551112836
