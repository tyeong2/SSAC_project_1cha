# coding: utf-8
import time
from datetime import datetime
import json
import ssl
import urllib.request
import requests
from json import loads
import itertools

def goo_ttubuck(d_time,start, end) :
    mode            = "transit"
    departure_time  = str(int(d_time))
    key             = "구글키"
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
    
        wholeDict = None
    with open("./Agent_Transit_Directions.json","r") as transitJson :
        wholeDict = dict(json.load(transitJson))

    path            = wholeDict["routes"][0]["legs"][0]
    duration_sec    = path["duration"]["value"]
    
#     res = []
#     
#     res.append(int(duration_sec/60))
#     for step in stepList:
#         cnt = []
#         cnt.append(step['html_instructions'])
#         cnt.append({"start":[step['start_location']['lat'],step['start_location']['lng']],"end":[step['end_location']['lat'],step['end_location']['lng']]})
#         res.append(cnt)
        
    return duration_sec

def getDistanceWalk(start, end):
    url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
    appkey = "티맵키"

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
    timestamp = time.mktime(datetime.strptime(d_time, '%Y-%m-%d %H:%M:%S').timetuple())+32400
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
'''  
if __name__ == '__main__':

    startList = ['노원', 127.07298186928676, 37.625573966660795]
    via01 = ['덕수궁',126.9749297,37.56614867]
    via02 = ['국립중앙도서관',127.0028374,37.49797931]
    via03 = ['국립국악원',127.0088597,37.47783732]
    endList = ['SSAC', 126.88641194885416, 37.517711633406485]
    
    via_list = [startList,via01,via02,via03,endList]
    
    f_res = opti_ttubuck('2021-01-10 12:12:12',via_list)
    
    print(f_res)
'''