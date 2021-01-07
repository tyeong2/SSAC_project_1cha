import requests
import json
import re
from json import loads
import pprint

def tmap_sample():
    url = 'https://apis.openapi.sk.com/tmap/routes/routeSequential30'

    #기초 셋팅
    time1 = 600  #경유지 머무는 시간 (단위 : 초)
    startTime = "202101061900"

    #출발 지역
    start_name = "은엽하우스"
    startX = "127.07298186928676"
    startY = "37.625573966660795"

    #첫번째 경유지
    loc1_name = "노량진역 9호선"
    loc1X = "126.9401285830874"
    loc1Y = "37.513475367430814"

    #두번째 경유지
    loc2_name = "신도림역 2호선"
    loc2X = "126.8912156304871"
    loc2Y = "37.508807855107904"

    #세번째 경유지
    loc3_name = "SSAC"
    loc3X = "126.88641194885416"
    loc3Y = "37.517711633406485"

    headers = {
        "appkey" : "",
        "version" : "1",
        "callback" : ""
    }

    payload = {
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": "출발 : " + str(start_name),
        "startX": str(startX),
        "startY": str(startY),
        "startTime": "202003160900",
        "endName": "도착 : " + str(start_name),
        "endX": str(startX),
        "endY": str(startY),
        "endPoiId": "",
        "searchOption": "0", #교통최적 + 추천
        "carType": "1", #승용차
        "viaPoints":
            [
                {
                    "viaPointId": "첫번째 경유지",
                    "viaPointName": str(loc1_name),
                    "viaX": str(loc1X),
                    "viaDetailAddress": str(loc1_name),
                    "viaY": str(loc1Y),
                    "viaPoiId": "",
                    "viaTime": str(time1),
                    "wishStartTime": "",
                    "wishEndTime": ""
                },
                {
                    "viaPointId": "두번째 경유지",
                    "viaPointName": str(loc2_name),
                    "viaX": str(loc2X),
                    "viaDetailAddress": str(loc2_name),
                    "viaY": str(loc2Y),
                    "viaPoiId": "",
                    "viaTime": str(time1),
                    "wishStartTime": "",
                    "wishEndTime": ""},
                {
                    "viaPointId": "세번째 경유지",
                    "viaPointName": str(loc3_name),
                    "viaX": str(loc3X),
                    "viaDetailAddress": str(loc3_name),
                    "viaY": str(loc3Y),
                    "viaPoiId": "",
                    "viaTime": str(time1),
                    "wishStartTime": "",
                    "wishEndTime": ""},

            ]

    }

    r = requests.post(url, json=payload, headers=headers)

    jsonObj = json.loads(r.text)

    # print(jsonObj)
    print("전체 거리 ",
          str(round(int(jsonObj['properties']['totalDistance']) / 100, 2)) + "km",
          "전체 소요 시간",
          str(round(int(jsonObj['properties']['totalTime']) / 60)) + "분",
          "",
          "시작 시간 : " + str(re.sub("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
                                  r"\1년\2월\3일 \4시\5분\6초",
                                  jsonObj['features'][0]['properties']['arriveTime'])),
          "",
          str(jsonObj['features'][1]['properties']['viaPointId']) + " : "
          + str(jsonObj['features'][1]['properties']['viaDetailAddress']),
    
          "도착 시간 : " + str(re.sub("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
                                  r"\1년\2월\3일 \4시\5분\6초",
                                  jsonObj['features'][2]['properties']['arriveTime'])),
          "",
          str(jsonObj['features'][3]['properties']['viaPointId']) + " : "
          + str(jsonObj['features'][3]['properties']['viaDetailAddress']),
    
          "도착 시간 : " + str(re.sub("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
                                  r"\1년\2월\3일 \4시\5분\6초",
                                  jsonObj['features'][3]['properties']['arriveTime'])),
          "",
          str(jsonObj['features'][5]['properties']['viaPointId']) + " : "
          + str(jsonObj['features'][5]['properties']['viaDetailAddress']),
    
          "도착 시간 : " + str(re.sub("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
                                  r"\1년\2월\3일 \4시\5분\6초",
                                  jsonObj['features'][5]['properties']['arriveTime'])),
          "",
          "완료 시간 : " + str(re.sub("(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
                                  r"\1년\2월\3일 \4시\5분\6초",
                                  jsonObj['features'][5]['properties']['completeTime'])),
    
          sep="\n"
          )


def getDistance(start_list, end_list):
    url = 'https://apis.openapi.sk.com/tmap/routes'

    # 출발 시간
    startTime = "202101061900"  #2021년 01월 06일 19시

    # 출발 지역
    start_name = start_list[0]
    startX = str(start_list[1])
    startY = str(start_list[2])

    # 도착지
    end_name = end_list[0]
    endX = str(end_list[1])
    endY = str(end_list[2])

    headers = {
        "appkey": "l7xx1e9d4d1d08474905a13739121fe554b7",
        "version": "1",
        "callback": ""
    }
    
    payload = {
        "appKey": "l7xx1e9d4d1d08474905a13739121fe554b7",
        "endX" : str(endX),
        "endY" : str(endY),
        "startX" : str(startX),
        "startY" : str(startY),
        "reqCoordType" : "WGS84GEO",
        "resCoordType" : "WGS84GEO",
        "tollgateFareOption" : "1",
        "roadType" : "32",
        "directionOption" : "0",
        "endPoiId" : "",
        "gpsTime" : "10000",
        "angle" : "",
        "speed" : "60",
        "uncetaintyP" : "1",
        "uncetaintyA" : "1",
        "uncetaintyAP" : "1",
        "camOption" : "0",
        "carType" : "0",
        "startName" : start_name,
        "endName" : end_name,
        "searchOption" : "0",
        "endRpFlag" : "G"
    }

    r = requests.post(url, json=payload, headers=headers)

    jsonObj = json.loads(r.text)

    print("전체 거리 ", str(round(int(jsonObj['features'][0]['properties']['totalDistance']) / 1000, 2)) + "km")
    
startList = ['노원역', 127.07298186928676, 37.625573966660795]
endList = ['SSAC', 126.88641194885416, 37.517711633406485]

getDistance(startList, endList)
