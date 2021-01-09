import pandas as pd
import json
import urllib.request
import urllib.parse
import webbrowser

def getGeocode(name):
    key = "&key=AIzaSyBbkgiIFQrwYw18gdSZUk8E_8fNE01OE2E"
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ko&address='
    search = urllib.parse.quote(name)
    addr = json.loads(urllib.request.urlopen(base_url + search + key).read().decode('utf-8'))
    result = addr['results'][0]['geometry']['location']
    return [result['lng'], result['lat']]


def getOrderOpt(startP, endP, *viaP):
    if len(viaP) > 10:
        print("경유지는 최대 10개까지만 가능합니다.")
        return -1
    db = pd.read_excel('DB_V21.xlsx', engine='openpyxl')

    start = getGeocode(startP) #출발지 좌표
    end = getGeocode(endP) #도착지 좌표

    position = []
    pos_elem = {
        'title': startP,
        'lonlat': [start[1],start[0]],
        'stayTime' : ""
    }
    position.append(pos_elem)
    pos_elem = {
        'title': endP,
        'lonlat': [end[1],end[0]],
        'stayTime': ""
    }
    position.append(pos_elem)
    for n in viaP:
        lng, lat, stayT = db[['좌표(x)', '좌표 (y)', '소요시간(분)']][db['검색명'] == n].iloc[0]
        pos_elem = {
            'title' : n,
            'lonlat' : [lat,lng],
            'stayTime' : int(stayT*60)
        }
        position.append(pos_elem)

    with open('res.js','w',encoding='utf-8') as jsfile:
        jsfile.write('var positions = ')
        json.dump(position, jsfile, ensure_ascii=False)
        jsfile.write(';\n')

    webbrowser.open_new_tab('routeoptimizer.html')

# getOrderOpt('서울역','서울역','63스퀘어','경복궁','서울타워')