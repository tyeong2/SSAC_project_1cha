import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
import time
import pandas as pd

#네이버 장소검색 정보 파싱
def info_parser(kwd):
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' #검색을 하면 이동하는 주소
    url = baseUrl + quote_plus(kwd) #주소에 검색어 추가
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    result = [] #결과가 저장될 
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
def tag_parser(search):
    baseUrl = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    url = baseUrl + quote_plus(search)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')

    theme = soup.find_all('div', class_='theme_kwd_area') #테마 키워드 영역
    if theme == []: #테마 키워드가 안 나오는 경우        
        return 'NaN'
    list_theme = theme[0].find('ul', class_='list_theme')
    list_item = list_theme.find_all('li',class_='list_item')
    kwd_list = [] #키워드가 저장될 리스트
    for ul in list_item:
        li = ul.find_all('span',class_='kwd')
        for i in li:
            kwd_list.append(i.text.strip(', '))

    return str(kwd_list).strip('[]')
