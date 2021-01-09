import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
import time
import pandas as pd

def info_parser(kwd): #네이버 장소검색 정보 파싱
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    url = baseUrl + quote_plus(kwd)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    result = []
    result.append(kwd)

    try:
        info = soup.find('div',class_='list_bizinfo')
        infolist = info.find_all('div',class_='list_item')
        try:
            tel = info.find('div',class_='txt').text
            # print(tel)
            result.append(tel)
        except:
            result.append('Nan')

        try:
            addr = info.find('span',class_='addr').text
            # print(addr)
            result.append(addr)
        except:
            result.append('Nan')

        try:
            runtime = []
            biztime = info.find_all('div', class_="biztime")
            for r in biztime:
                runtime.append(r.text)
            # print(runtime)
            result.append(runtime)
        except:
            result.append('NaN')

        try:
            homepage = info.find('div', class_="list_item list_item_homepage").find('a', class_='biz_url').get('href')
            # print(homepage)
            result.append(homepage)
        except:
            result.append('NaN')

        try:
            if '주차' in infolist[-1].find('div', class_='txt').get_text().split(','):
                parking = '주차가능'
            else:
                parking = '주차불가'
            # print(parking)
            result.append(parking)
        except:
            result.append('NaN')
    except:
        return [kwd,'NaN','NaN','NaN','NaN','NaN']

    return result


def make_csv(): #csv 파일로 저장
    title = pd.read_csv('empty.csv')

    col_name = []
    col_tel = []
    col_addr = []
    col_runtime = []
    col_homepage = []
    col_parking = []

    for t in title['title']:
        print(t)
        res = info_parser(t)
        col_name.append(res[0])
        col_tel.append(res[1])
        col_addr.append(res[2])
        col_runtime.append(res[3])
        col_homepage.append(res[4])
        col_parking.append(res[5])

    naver = pd.DataFrame()
    naver['이름'] = pd.Series(col_name)
    naver['전화번호'] = pd.Series(col_tel)
    naver['주소'] = pd.Series(col_addr)
    naver['영업시간'] = pd.Series(col_runtime)
    naver['홈페이지'] = pd.Series(col_homepage)
    naver['주차'] = pd.Series(col_parking)

    naver.to_csv("naverparsing.csv", encoding='UTF8', index=True)

def naver_parser(kwd): #네이버 데이터랩 테마키워드 파싱
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    url = baseUrl + quote_plus(kwd)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    driver = webdriver.Chrome(executable_path="C:\\pythonProject\\chromedriver")
    try:
        title = soup.find_all('a', class_ ="api_more_theme")
        newurl = title[0].get('href')

        #셀레니움 동작
        driver.get(newurl)

        time.sleep(5)
        driver.implicitly_wait(5)

        html02 = driver.page_source  # 문서화 한다
        soup02 = BeautifulSoup(html02, 'html.parser')
        # result = soup02.find('div', class_='score_total').find('strong', class_='total').find_all('em')
        # result = soup02.find('span', class_="_3XamX")
        result = soup02.find('div', class_="place_section no_margin")
        contents = soup02.select("div > div.ps-content > div > div > div .item_search")
        name = driver.find_element_by_xpath('//*[@id="_title"]/span[1]')
        runtime = driver.find_element_by_xpath('//*[@id="app-root"]/div/div[2]/div[5]/div/div[2]/div/ul/li[4]/div/a/div[1]/div/span')
    except:
        pass

