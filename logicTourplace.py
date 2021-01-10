import csv
import pandas as pd
import numpy as np
import datetime
import time
import pytz
#-*- coding: utf-8 -*-

user=open("C:\\Program Files\\Python39\\user1.txt",mode='r',encoding='utf-8')#메모장에 있는 나이,성별,여행날짜,출발지,도착지,여행시간,테마,주차여부 정보를 불어옴
data=pd.read_csv("C:\\python_atom\\DB_V26.csv",sep=',',engine='python')#각 관광지에 해당하는 정보DB를 불러옴

line = user.read().split('\n')#개인이 선택한 항목들을 한줄씩 불러옴
print(line)



#나이와 성별을 입력하여 해당 정보와 일치하는 칼럼을 리턴
def personal(age,gender):

    if age=='10':
        age_result=(data['10대']) #10대인 경우 10대의 관광지 검색 빈도가 있는 컬럼을 불러옴

    elif age=='20':
        age_result=(data['20대'])

    elif age=='30':
        age_result=(data['30대'])

    elif age=='40':
        age_result=(data['40대'])

    elif age=='50':
        age_result=(data['50대'])

    elif age=='60':
        age_result=(data['60대'])


    #성별에 따른 관광지 검색량 컬럼 불러오기
    if gender=='man':
        gender_result=(data['남자'])

    elif gender=='woman':
        gender_result=(data['여자'])

    return age_result,gender_result



def season(date):#여행가고자 하는 날짜를 입력하면, 해당 계절 선호에 따른 관광지 배점
    d = datetime.datetime.strptime(date,'%Y-%m-%d')
    if d.month>= 3 and d.month <=6:
        date_result=(data['봄'])#3월부터 6월에 사용자가 검색한 관광지 빈도를 불러옴

    elif d.month>=7 and d.month <=8:
        date_result=(data['여름'])#7월부터 8월에 사용자가 검색한 관광지 빈도를 불러옴

    elif d.month>=9 and d.month <=11:
        date_result=(data['가을'])#9월부터 11월에 사용자가 검색한 관광지 빈도를 불러옴

    elif d.month==1 or d.month ==2 or d.month==12:
        date_result=(data['겨울'])#12월부터 2월에 사용자가 검색한 관광지 빈도를 불러옴



    days=['월','화','수','목','금','토','일']
    r=d.weekday() #여행날짜의 요일을 구함
    day=days[r]
    data['휴일']=data['휴일'].astype(str) #여행날짜에 관광지 휴무일이 있으면 해당 관광지의 인덱스를 찾는 로직
    list_h=data['휴일'].tolist()#휴무일 관련 정보를 리스트에 담음
    i=0
    stop=[]
    while i <len(list_h):
        if day in list_h[i]:
            stop.append(i)#stop 리스트에 휴무일 관광지 인덱스가 담긴다.
        else:
            pass
        i=i+1

    return date_result,stop




def getTheme(theme):#여행테마를 입력하면 해당 테마를 가지고 있는 여향지에 추가점수 5점
    data['키워드'] = data['키워드'].astype(str)

    category = {'이국적인': ['유러피안스타일', '이국적'],
               '고급스러운' : ['고급스러운', '고급진', '근사한', '기품있는', '멋스러운', '세련된', '트렌디한', '화려한',
                         '우아한', '퀄리티있는', '웅장한'],
                '사진찍기좋은' : ['감각적인', '느낌있는', '깨끗한', '빈티지', '아기자기', '운치있는', '개성있는', '채광좋은',
                         '화사한', '사진_영상촬영'],
                '옛스런' : ['고즈넉한', '빈티지한', '옛모습'],
                '이색적인' : ['독특한분위기', '동화적인', '신비한', '재미있는', '유니크한', '신나는'],
                '낭만적인' : ['낭만적인', '따뜻한분위기', '분위기있는', '분위기좋은', '서정적인'],
                '힐링' : ['소박한', '수수한', '심플한', '아늑한', '아담한', '인심좋은', '친절하고', '친절한', '친절함',
                        '편안한', '평온한', '평화로운', '포근한', '프라이빗', '작은공간', '작은규모', '조그마한',
                        '쾌적한', '활기찬', '행복한'],
                '현대적인' : ['모던한', '캐주얼한', '트렌디한'],
                '나들이' : ['가을여행', '가족나들이', '기차여행', '나들이', '단풍구경', '드라이브', '봄꽃', '봄소풍',
                         '사진찍기', '유물', '유적', '주말나들이', '피크닉', '한강전망', '휴식', '힐링', '경치',
                         '비오는날', '숨겨진', '숨어있는', '숨은', '휴식_힐링', '가족여행', '자연경관_경치감상', '미성년자녀_동반'],
                '건강' : ['등산', '보양식', '산행', '신선한', '싱싱한', '웰빙', '유기농', '착한가격', '제철음식'],
                '즐길거리' : ['동물체험', '드라마촬영지', '자극적인', '재방문', '직업체험', '체험관', '촬영지',
                          '퓨전요리','한복체험', '체험학습', '레저_놀이'],
                '데이트' : ['기념일', '데이트', '발렌타인데이', '프로포즈', '크리스마스파티', '핫플레이스', '연인_배우자',]
                }
    k=0
    while k <844:

        if data['키워드'][data['인덱스']==k].empty:
            k+=1
            return 0
        else:
            cmp = []    #비교할 대상

            for t in theme[0].split(',')[:-1]:
                cmp.extend(category[t]) #사용자가 선택한 테마의 키워드들을 비교 리스트에 담는다.
            kwd = data['키워드'][data['인덱스']==k].iloc[0]
            for elem in kwd.split(','): # 해당 관광지의 키워드들을 하나씩 비교

                if elem.strip() in cmp:
                    total[k] += 5   #관광지의 테마키워드가 사용자가 선택한 테마의 키워드 리스트에 포함될 시에 점수 상승
            k+=1




def parking(park):#관광지에 주차장이 있다면 추가점수 5점
    if park=='자동차':
        parkTable=data[['인덱스']][data['주차장소'].isin(['가능'])]#주차가 가능한 관광지를 찾음
        df2 = pd.DataFrame(parkTable)
        park_result = df2['인덱스'].tolist()
        for j in park_result:
            total[j]=total[j]+5
    else:
        pass


def blog():#블로그 리뷰수에 비례하여 관광지 추가점수를 부여
    blogTable=data['리뷰수'] #블로그 리뷰수를 불러옴
    df3 = pd.DataFrame(blogTable)
    blog_result = df3['리뷰수'].tolist()

    max_blog=max(blog_result)
    blog_ans=list(map(lambda x : x/max_blog*5, blog_result))# 가장 많은 리뷰수를 기준으로 5점을 부여하고 리뷰수에 비례해 점수 차등부여
    i=0
    while i <len(total):
        total[i]=total[i]+blog_ans[i]
        i=i+1




def tourMain():
    age_result,gender_result = personal(line[0],line[1])#나이와 성별 입력
    date_result,stop=season(line[2])#날짜입력
    global total
    total=((age_result*0.4)+(gender_result*0.4)+(date_result*0.2)) #관광지 토탈점수가 계산되는 식

    getTheme([line[7]])#여행테마 입력
    parking(line[6])#주차여부 확인
    blog()#리뷰개수에 따른 관광지 추가점수
    for n in stop:#여행날짜에 휴일인 관광지는 0점 처리
        total[n]=0


    m=list(total)#관광지 종합 점수들을 리스트에 넣고
    compare=list(total)#원본을 복사
    m.sort(reverse=True)#원본을 점수가 큰 순서대로 나열


    top50=[]#점수 크기 순 TOP50이 담길 리스트
    recommand=[]#TOP50 관광지의 인덱스 리스트

    num=0
    while num < 50:
        top50.append(m[num])#점수가 큰 순서대로 50개의 관광지가 top50리스트에 추가됨
        recommand.append(compare.index(top50[num]))#기존 인덱스의 관광지 순서로 recommand리스트에 추가됨
        num=num+1

    new_recommand = [] #인덱스 중복값 제거
    for v in recommand:
        if v not in new_recommand:
            new_recommand.append(v)



    #추천 인덱스에 해당하는 정보 넣기
    re=pd.DataFrame(columns =['관광지명','검색명','주소','좌표(x)','좌표 (y)','운영시간','영업시작','영업종료','주차장소','소요시간(분)','사진','설명','휴일','전화번호','홈페이지','키워드'])

    for x in new_recommand:#인덱스 순위대로 데이터프레임에 넣기
        res=data[['관광지명','검색명','주소','좌표(x)','좌표 (y)','운영시간','영업시작','영업종료','주차장소','소요시간(분)','사진','설명','휴일','전화번호','홈페이지','키워드']][data['인덱스']==x]
        re=re.append(res,ignore_index=True)

    print(new_recommand)
    print(top50)




    #6) 파일로 저장
    re.to_csv("c:\\test\\final2.csv",encoding="UTF-8",index=True)
    #7) 엑셀로 저장
    re.to_excel("c:\\test\\final2.xls",index=True)

    user.close()

tourMain()
