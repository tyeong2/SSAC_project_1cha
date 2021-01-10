
import urllib
import json
import sys
import urllib.request
import urllib.parse

key = "&key=AIzaSyBbkgiIFQrwYw18gdSZUk8E_8fNE01OE2E"
# 지명 주소를 위/경도 주소로,
base_url ='https://maps.googleapis.com/maps/api/geocode/json?language=ko'+\
                '&address='
# 부분 주소를 통해서 찾기
x = open("c:\\test\\list.txt",'r', encoding='UTF-8')
f = open("c:\\test\\y.txt",'w', encoding='UTF-8')
h = open("c:\\test\\x.txt",'w', encoding='UTF-8')
for hanaddr in x:

    address = urllib.parse.quote(hanaddr)
    addr = json.loads(urllib.request.urlopen(base_url+address+key).read().decode('utf-8'))
    # 위치 정보만 뽑기
    for i in addr['results']:
        a = (i['geometry']['location'])
        li = list(a.values())#밸류 값만 리스트에 담긴다.


    print(li[0],file=h)#위도 저장
    print(li[1],file=f)#경도 저장


f.close
h.close
x.close
