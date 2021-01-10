# coding: utf-8
import time
import json
import os
import ssl
import urllib.request

def goo_ttubuck(start, end) :
    mode            = "transit"
    departure_time  = "now"
    key             = "구글키"

    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+ start \
            + "&destination=" + end \
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
    start_geo       = path["start_location"]
    end_geo         = path["end_location"]
    
    stepList = path["steps"]
    
    res = []
    
    res.append(int(duration_sec/60))
    for step in stepList:
        cnt = []
        cnt.append(step['html_instructions'])
        cnt.append({"start":[step['start_location']['lat'],step['start_location']['lng']],"end":[step['end_location']['lat'],step['end_location']['lng']]})
        res.append(cnt)
        
    return res


if __name__ == '__main__':

    start   = ["노원",37.625573966660795,127.07298186928676]
    end     = ["SSAC",37.517711633406485,126.88641194885416]
    
    ooo = goo_ttubuck(start, end)
    
    print(ooo)
    