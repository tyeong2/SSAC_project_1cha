
import urllib
import json
import sys
import urllib.request
import urllib.parse

key = ""
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
        li = list(a.values())


    print(li[0],file=h)
    print(li[1],file=f)


f.close
h.close
x.close