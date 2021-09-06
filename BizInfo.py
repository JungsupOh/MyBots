# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import datetime
from datetime import timedelta
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


def biz_info(driver, xls_filename):
    bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
    try:
        # 입찰정보 결과 넣을 Excel File
        writer = StyleFrame.ExcelWriter('/home/bidding/Documents/BidCrawler/Biz_Info.xlsx')

        # 입찰정보 검색 페이지로 이동
        driver.get('https://www.bizinfo.go.kr/see/seea/selectSEEA100.do?sportRearmCode=06&menuId=80001001001&firstYn=N')

        driver.find_element_by_xpath("//a[contains(@onclick,'fn_detailExcelOpen(1);return false;')]").click()
        time.sleep(3)


        # CSV to dataframe
        biz_xls = pd.read_excel(xls_filename, header=1, skiprows=1)

        # Find keywords from Biz_info csv
        df_global = biz_xls[biz_xls["지원사업명"].str[0] != '[']
        df_local = biz_xls[biz_xls["지원사업명"].str.contains('대전')]
        df = pd.concat([df_global, df_local])

        df_new = df[df['등록일'].apply(autoconvert_datetime) > str(datetime.date.today()-timedelta(weeks=1))]

        print('Found %4d Items for Global, Found %4d Items for Local' % (df_global.shape[0], df_local.shape[0]))

        g_row = df.shape[0]
        if g_row > 0:
            sf = StyleFrame(df_global)
            # -- write an object to an Excel sheet using pd.DataFrame.to_excel()
            sf.to_excel(writer, sheet_name='전국', na_rep='NaN', float_format="%.2f",
                        header=True, index=True, index_label="No.",
                        startrow=0, startcol=0, best_fit=['지원사업명'])

        l_row = df.shape[0]
        if l_row > 0:
            sf = StyleFrame(df_local)
            # -- write an object to an Excel sheet using pd.DataFrame.to_excel()
            sf.to_excel(writer, sheet_name='대전', na_rep='NaN', float_format="%.2f",
                        header=True, index=True, index_label="No.",
                        startrow=0, startcol=0, best_fit=['지원사업명'])

        # bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
        bot.sendDocument(chat_id=167233193, document=open('/home/bidding/Documents/BidCrawler/Biz_Info.xlsx', 'rb'))

        # notify new info / within a week
        for idx, row in df_new.iterrows():
            bot.sendMessage(chat_id=167233193, text=row['지원사업명']+'\n'+row['상세 URL'])

    except Exception as e:
        # 위 코드에서 에러가 발생한 경우 출력
        print(e)
        bot.sendMessage(chat_id=167233193, text='BizInfo 공고 취합 실패!!')
        return False

    finally:
        writer.close()
        # 에러와 관계없이 실행되고, 크롬 드라이버를 종료
        return True
