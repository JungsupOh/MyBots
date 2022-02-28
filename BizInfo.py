# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import datetime
from datetime import timedelta
import telegram
from styleframe import StyleFrame
import pandas as pd
import time
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



def biz_info(driver, xls_filename, query):
    try:
        root_path = '/Users/james/Documents/GitHub/MyBots/'
        
        # 입찰정보 결과 넣을 Excel File
        #writer = StyleFrame.ExcelWriter(root_path + 'Biz_Info.xlsx')
        print('Debug #1')

        # 입찰정보 검색 페이지로 이동
        driver.get('https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do')
        print('Debug #2')

        # 검색옵션 100건 선택 (드롭다운)
        searchoption = driver.find_element(by=By.XPATH, value="//div[@class='custom_select']").click()
        time.sleep(1)
        print('Debug #2-1')
        searchoption = driver.find_element(by=By.XPATH, value="//button[@data-option='pldirJrsdCodeNm']").click()
        time.sleep(1)
        print('Debug #2-2')

        # bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
        bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
        print('BizInfo>> Bot Connected..')

        for keyword in query:
            
            # id값이 bidNm인 태그 가져오기
            searchInput = driver.find_element(by=By.XPATH, value="//input[@name='keyword']")
            print('Debug #3')
            # 내용을 삭제 (버릇처럼 사용할 것!)
            searchInput.clear()
            # 검색어 입력후 엔터
            searchInput.send_keys(keyword)
            searchInput.send_keys(Keys.RETURN)
            print('Debug #3, Keyword: '+ keyword)

            # Read and Convert Web table into data frame
            webtable_df = pd.read_html(driver.find_element(by=By.XPATH, value="//div[@class='table_Type_1']").get_attribute('innerHTML'))[0]

            print(webtable_df)
            
           

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
