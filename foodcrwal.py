from bs4 import BeautifulSoup
from selenium import webdriver
import math
import time
import pandas  as pd
import re


telephone=[]
weektime=[]
pic=[]
stat=[]

#크롬드라이버를 이용하여 웹크롤링 실시
driver  =  webdriver . Chrome ( executable_path ="C:\\test\\chromedriver" )
driver.get("https://www.naver.com")
driver.implicitly_wait(1)



query  ="시작" #오류 방지를 위해서 임의의 값을 검색후 시작
element  = driver.find_element_by_id("query")
element.click()
element.send_keys(query+'\n')


x = open("c:\\test\\foodlist1.txt",'r', encoding='UTF-8')#음식점 이름목록이 담긴 텍스트 파일 호출
for list in x:#한줄씩 검색창에 입력하기
    query  = list
    driver.back()#하나의 정보를 입력해서 받아오면 웹페이지 뒤로가기
    element  = driver.find_element_by_id("query")
    element.click()
    element.send_keys(query+'\n')





    f = open("c:\\test\\foodapi1.txt",'a', encoding='UTF-8')

    #2)동기화  및 요청 건수 비교
    html  = driver.page_source   #문서화 한다.
    soup  = BeautifulSoup(html, "html.parser")

    try:#음식점사진
        pic_result = soup.find('div',class_='top_photo_area type_v4').find_all('div',class_='thumb_area')[0].find('img')
        pic.append(pic_result)
        f.write(str(pic_result))
    except:
        pic.append('NaN')
        #전화번호
    try:
        tel_result = soup.find('div',class_='list_bizinfo').find_all('div',class_='list_item')[0].find('div',class_='txt').get_text()
        telephone.append(tel_result)
        f.write(tel_result+'\t')
    except:
        telephone.append('NaN')

    try:#운영시간
        time_result = soup.find('div',class_='list_bizinfo').find_all('div',class_='list_item')[2].find('span',class_='time').find('span').get_text()
        weektime.append(time_result)
        f.write(time_result)
    except:
        weektime.append('NaN')

    try:#미디어 출연 설명

        tv=soup.find('div',class_='list_bizinfo').find_all('div',class_='list_item')[-1].find('div',class_='txt').find_all('div',class_='tv')[0].find_all('span')[0].get_text()
        stat.append(tv)

    except:
        stat.append('NaN')

    time.sleep(1)




    #5) 판다스로 연동

print(telephone)

food=pd.DataFrame()
food['사진'] =pd.Series(pic)
food['전화번호'] =pd.Series(telephone)
food['운영시간'] =pd.Series(weektime)
food['설명'] =pd.Series(stat)

    #6) 파일로 저장
food.to_csv("c:\\test\\foodapi1.csv",encoding="UTF-8",index=True)
    #7) 엑셀로 저장
food.to_excel("c:\\test\\foodapi1.xls",index=True)

    #8) 종료
driver.close()
f.close()
