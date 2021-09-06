# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
import telegram
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from styleframe import StyleFrame
import pandas as pd


def nara_market(driver, query):
    bot = telegram.Bot(token='1631327665:AAEX8hykT_WuTjQXWYnxigN1jM1WBqHAip4')
    try:
        # 입찰정보 결과 넣을 Excel File
        writer = StyleFrame.ExcelWriter('/home/bidding/Documents/BidCrawler/NaraBidInfo.xlsx')

        # 입찰정보 검색 페이지로 이동
        driver.get('http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')

        # 업무 종류 체크, '전체': 'taskClCds'
        task_dict = {'물품': 'taskClCds1', '용역': 'taskClCds5', '민간': 'taskClCds20', '기타': 'taskClCds4'}
        for task in task_dict.values():
            checkbox = driver.find_element_by_id(task)
            checkbox.click()

        # 검색 조건 체크
        option_dict = {'검색기간 1달': 'setMonth1_1', '입찰마감건 제외': 'exceptEnd', '검색건수 표시': 'useTotalCount'}
        for option in option_dict.values():
            checkbox = driver.find_element_by_id(option)
            checkbox.click()

        # 목록수 100건 선택 (드롭다운)
        recordcountperpage = driver.find_element_by_name('recordCountPerPage')
        selector = Select(recordcountperpage)
        selector.select_by_value('100')

        for keyword in query:
            # id값이 bidNm인 태그 가져오기
            bidNm = driver.find_element_by_id('bidNm')
            # 내용을 삭제 (버릇처럼 사용할 것!)
            bidNm.clear()
            # 검색어 입력후 엔터
            bidNm.send_keys(keyword)
            bidNm.send_keys(Keys.RETURN)

            # 검색 버튼 클릭
            search_button = driver.find_element_by_class_name('btn_mdl')
            search_button.click()

            # 검색 결과 확인
            elem = driver.find_element_by_class_name('results')
            div_list = elem.find_elements_by_tag_name('div')

            # column list
            columns = ['업무', '공고번호', 'URL', '분류', '공고명', 'URL2', '공고기관', '수요기관', '계약방법', '입력일시', '공동수급', '투찰']
            df = pd.DataFrame(columns=columns)

            col = 0
            row = 0
            for div in div_list:
                if col == 0:
                    df.loc[row] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                    row += 1
                df.iloc[row-1][columns[col]] = div.text
                col += 1
                a_tags = div.find_elements_by_tag_name('a')
                if a_tags:
                    for a_tag in a_tags:
                        df.iloc[row-1][columns[col]] = a_tag.get_attribute('href')
                        col += 1
                col %= 12

            print('Found %4d Items for Keyword [%s]' % (row, keyword))
            if row > 0:
                df = df.drop(['분류', 'URL2', '공고기관', '계약방법', '공동수급'], axis=1)
                columnTitles = ['업무', '공고번호', '공고명', '수요기관', '입력일시', 'URL']
                sf = StyleFrame(df.reindex(columns=columnTitles))
                # -- write an object to an Excel sheet using pd.DataFrame.to_excel()
                sf.to_excel(writer, sheet_name=keyword, na_rep='NaN', float_format="%.2f",
                            header=True, index=True, index_label="No.",
                            startrow=0, startcol=0, best_fit=['공고명', 'URL'])

            # 검색화면 이동 버튼 클릭
            search_button = driver.find_element_by_class_name('btn_mdl')
            search_button.click()

        # bot.sendMessage(chat_id=167233193, text='Hello~~ 안녕하세요..')
        bot.sendDocument(chat_id=167233193, document=open('/home/bidding/Documents/BidCrawler/NaraBidInfo.xlsx', 'rb'))

    except Exception as e:
        # 위 코드에서 에러가 발생한 경우 출력
        print(e)
        bot.sendMessage(chat_id=167233193, text='나라장터 공고 취합 실패!!')
        return False

    finally:
        writer.close()
        # 에러와 관계없이 실행되고, 크롬 드라이버를 종료
        return True
