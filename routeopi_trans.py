# coding: utf-8
import time
from datetime import datetime,timedelta
import json
import ssl
import urllib.request
import requests
import itertools
import webbrowser
import urllib.parse
import pandas as pd


def goo_ttubuck(d_time,start, end) :
    mode            = "transit"
    departure_time  = str(int(d_time))
    key             = ""
    start_point     = str(start[2]) + "," + str(start[1])
    end_point       = str(end[2]) + "," + str(end[1])

    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ start_point \
            + "&destination=" + end_point \
            + "&mode=" + mode \
            + "&departure_time=" + departure_time\
            + "&language=ko" \
            + "&key=" + key

    request         = urllib.request.Request(url)
    context         = ssl._create_unverified_context()
    response        = urllib.request.urlopen(request, context=context)
    responseText    = response.read().decode('utf-8')
    responseJson    = json.loads(responseText)

    with open("./Agent_Transit_Directions.json","w") as rltStream :
        json.dump(responseJson,rltStream)
    
    with open("./Agent_Transit_Directions.json","r") as transitJson :
        wholeDict = dict(json.load(transitJson))

    path            = wholeDict["routes"][0]["legs"][0]
    duration_sec    = path["duration"]["value"]
    
    return duration_sec

def getDistanceWalk(start, end):
    url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
    appkey = ""

    start_name = start[0]
    startX = str(start[1])
    startY = str(start[2])

    end_name = end[0]
    endX = str(end[1])
    endY = str(end[2])

    headers = {
        "appkey": appkey,
        "version": "1",
        "callback": ""
    }

    payload = {
        "startX": str(startX),
        "startY": str(startY),
        "endX": str(endX),
        "endY": str(endY),
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": start_name,
        "endName": end_name,
        "searchOption" : "0"
    }

    r = requests.post(url, json=payload, headers=headers)
    jsonObj = json.loads(r.text)

    return jsonObj['features'][0]['properties']['totalTime']

def opti_ttubuck(d_time,via):
    timestamp = time.mktime(datetime.strptime(d_time, '%Y-%m-%d %H:%M:%S').timetuple())+16200
    check = [[i for i in range(len(via))] for j in range(len(via))]
    s_distance = list(itertools.combinations((list(range(len(via)))),2))
    
    for com in s_distance:
        beh = goo_ttubuck(timestamp, via[com[0]], via[com[1]])
        dobo = getDistanceWalk(via[com[0]], via[com[1]])
        
        check[com[0]][com[1]] = min(beh,dobo)
        check[com[1]][com[0]] = min(beh,dobo)
    
    combi = list(range(1,len(via)-1))
    combi_list = list(itertools.permutations((combi),len(combi)))
    
    check_time = []
    check_combi = []
    
    for c_com in combi_list:
        combi_list_set = [0] + list(c_com) + [len(via)-1]
        check_combi.append(combi_list_set)
        che_sum = 0
        for i in range(len(combi_list_set)-1):
            che_sum = che_sum + check[combi_list_set[i]][combi_list_set[i+1]]
        check_time.append(che_sum)
            
    res_idx = check_time.index(min(check_time))
    res_list = [min(check_time)]
    
    for idx in check_combi[res_idx]:
        res_list.append(via[idx][0])
    
    return res_list

def getGeocode(name):
    key = "&key="
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ko&address='
    search = urllib.parse.quote(name)
    addr = json.loads(urllib.request.urlopen(base_url + search + key).read().decode('utf-8'))
    result = addr['results'][0]['geometry']['location']
    return [result['lng'], result['lat']]

def write_via_js(start,end, via_list,rest):
    db_rest = pd.read_excel('DB_V27.xlsx', sheet_name=1)
    coodi_rest = []

    for y in rest:
        res=db_rest[['좌표(x)','좌표(y)']][db_rest['이름']==y]
        coodi_rest.append([res.iloc[0,0],res.iloc[0,1]])

    position = []
    #출발지
    pos_elem = {
        'title': "출발",
        'lonlat': [start[2],start[1]],
        'icon' : "https://www.flaticon.com/svg/static/icons/svg/3284/3284607.svg"
    }
    position.append(pos_elem)
    #도착지
    pos_elem = {
        'title': "도착",
        'lonlat': [end[2],end[1]],
        'icon' : "https://www.flaticon.com/svg/static/icons/svg/3942/3942104.svg"
    }
    position.append(pos_elem)
    #경유지 입력
    for n in via_list:
        pos_elem = {
            'title' : n[0],
            'lonlat' : [n[2],n[1]],
            'icon' : "https://www.flaticon.com/svg/static/icons/svg/2928/2928889.svg"
        }
        position.append(pos_elem)
    cnt = 0
    for n in rest:
        pos_elem = {
            'title' : n,
            'lonlat' : [coodi_rest[cnt][1],coodi_rest[cnt][0]],
            'icon' : "https://www.flaticon.com/svg/static/icons/svg/3170/3170733.svg"
        }
        cnt += 1
        position.append(pos_elem)

    #출발지,도착지,경유지 정보가 담긴 파일 출력
    with open('res1.js','w',encoding='utf-8') as jsfile:
        jsfile.write('var posi = ')
        json.dump(position, jsfile, ensure_ascii=False)
        jsfile.write(';\n')

def routeopi_Trans():
    user=open("via_list.txt",mode='r',encoding='utf-8')
    dpart_time = user.readline().strip('\n').split(',')[0] + " " +user.readline().strip('\n').split(',')[0] + ":00:00"
    a = user.readline().strip('\n').split(',')
    via_list = user.readline().strip('\n').split(',')[:-1]
    via_rest = user.readline().strip('\n').split(',')[:-1]
    
    start = [via_list[0]] + getGeocode(via_list[0]) #출발지 좌표
    end = [via_list[-1]] + getGeocode(via_list[-1]) #도착지 좌표
    
    db = pd.read_excel('DB_V26.xlsx', sheet_name=0)
    via_title_coodi = []
    via_time = []
    
    for n in via_list[1:len(via_list)-1]:
        lng = db[['좌표(x)']][db['검색명'] == n].iloc[0,0]
        lat = db[['좌표 (y)']][db['검색명'] == n].iloc[0,0]
        stayT = db[['소요시간(분)']][db['검색명'] == n].iloc[0,0]
        via_title_coodi.append([n,lng,lat])
        via_time.append(stayT)
    
    res_via_list = [start] + via_title_coodi + [end]
    f_res = opti_ttubuck(dpart_time,res_via_list)
    
    mark_via = []
    
    for f in f_res[2:]:
        for via_check in via_title_coodi:
            if f == via_check[0]:
                mark_via.append(via_check)
    
    for w, q in enumerate(mark_via):
        q[0] = str(w+1)+ ". " + q[0]
    
    print(via_time)
    print(type(via_time[0]))
    
    res_time = sum(via_time) + int(f_res[0]/60)
    
    s_time = datetime.strptime(dpart_time, '%Y-%m-%d %H:%M:%S')
    s_str = s_time.strftime("출발 : 20%Y년 %m월 %d일 %H:%M",)
    e_time = s_time+timedelta(minutes=int(res_time))
    e_str = e_time.strftime("도착 : 20%Y년 %m월 %d일 %H:%M",)
    total_time = str(int(res_time/60)) + "시간 " + str(int(res_time%60)) +"분"
    
    time_js = [s_str,e_str,total_time]
    
    with open('res2.js','w',encoding='utf-8') as jsfile:
        jsfile.write('var se_time = ')
        json.dump(time_js, jsfile, ensure_ascii=False)
        jsfile.write(';\n')
    write_via_js(start,end,mark_via,via_rest)
    
    webbrowser.open_new_tab('route_opit_trans.html')
