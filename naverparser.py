import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
import time
import pandas as pd

#네이버 장소검색 정보 파싱
def info_parser(kwd):
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    url = baseUrl + quote_plus(kwd)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    result = []
    result.append(kwd)
    
    #검색결과에서 정보가 나온다면
    try:
        info = soup.find('div',class_='list_bizinfo')
        infolist = info.find_all('div',class_='list_item')
        try:
            #전화번호
            tel = info.find('div',class_='txt').text
            result.append(tel)
        except:
            result.append('Nan')

        try:
            #주소
            addr = info.find('span',class_='addr').text            
            result.append(addr)
        except:
            result.append('Nan')

        try:
            #운영시간
            runtime = []
            biztime = info.find_all('div', class_="biztime")
            for r in biztime:
                runtime.append(r.text)            
            result.append(runtime)
        except:
            result.append('NaN')

        try:
            #홈페이지
            homepage = info.find('div', class_="list_item list_item_homepage").find('a', class_='biz_url').get('href')            
            result.append(homepage)
        except:
            result.append('NaN')

        try:
            #주차 가능 여부
            if '주차' in infolist[-1].find('div', class_='txt').get_text().split(','):
                parking = '주차가능'
            else:
                parking = '주차불가'            
            result.append(parking)
        except:
            result.append('NaN')
            
    #검색 결과에서 정보가 없다면
    except:
        return [kwd,'NaN','NaN','NaN','NaN','NaN']

    return result

#네이버 데이터랩 테마키워드 파싱
def naver_parser(kwd):
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    url = baseUrl + quote_plus(kwd)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    driver = webdriver.Chrome(executable_path="C:\\pythonProject\\chromedriver")
    try:
        #테마키워드 영역
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

