# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import datetime

import telegram
from styleframe import StyleFrame
import pandas as pd
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


def alio_bidinfo(driver, query, csv_filename):
    bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
    print('Bot Connected..')
    try:
        # 입찰정보 결과 넣을 Excel File
        writer = StyleFrame.ExcelWriter('/home/bidding/Documents/BidCrawler/ALIO_BidInfo.xlsx')

        # 입찰정보 검색 페이지로 이동
        driver.get('http://www.alio.go.kr/informationBid.do')

        driver.find_element_by_xpath("//a[contains(@onclick,'goExcelCsv')]").click()
        time.sleep(3)

        # CSV to dataframe
        alio_csv = pd.read_csv(csv_filename, header=0, engine='python', encoding='euc-kr', error_bad_lines=False)

        for keyword in query:
            # Find keywords from ALIO csv
            df = alio_csv[alio_csv['제목'].str.contains(keyword)]
            df = df[df['입찰종료일'].apply(autoconvert_datetime) > str(datetime.date.today())]

            row = df.shape[0]
            print('Found %4d Items for Keyword [%s]' % (row, keyword))
            if row > 0:
                sf = StyleFrame(df)
                # -- write an object to an Excel sheet using pd.DataFrame.to_excel()
                sf.to_excel(writer, sheet_name=keyword, na_rep='NaN', float_format="%.2f",
                            header=True, index=True, index_label="No.",
                            startrow=0, startcol=0, best_fit=['제목'])

        # bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
        bot.sendDocument(chat_id=167233193, document=open('/home/bidding/Documents/BidCrawler/ALIO_BidInfo.xlsx', 'rb'))

    except Exception as e:
        # 위 코드에서 에러가 발생한 경우 출력
        print(e)
        bot.sendMessage(chat_id=167233193, text='ALIO 공고 취합 실패!!')
        return False

    finally:
        writer.close()
        # 에러와 관계없이 실행되고, 크롬 드라이버를 종료
        return True
