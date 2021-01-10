import csv
import pandas as pd
import numpy as np
import numbers
import math
from pyproj import Proj, transform

#-*- coding: utf-8 -*-

def rest_sort(j_list):
    data=pd.read_csv("DB_rest.csv")
    
    a, b = data['좌표(x)'],data['좌표(y)']
    N_point = data['평점'].values.tolist()
    
    xy_coodi = list(zip(a.tolist(),b.tolist()))
    
    if len(j_list) == 1:
        rest_distance = []
        for coodi in xy_coodi:
            rest_distance.append(abs(dot_distance(coodi,j_list[0])))
        dis_max = max(rest_distance)
        
        rest_distance_point = list(map(lambda x: int((dis_max - x)*20/dis_max),rest_distance))
        res_point = list(map(lambda x: x[0] + x[1], zip(rest_distance_point,N_point)))
        return list_ranking(res_point)[:10]
    
    else:
        rest_distance_point = []
        for step in range(len(j_list)-1):
            rest_distance = []
            for coodi2 in xy_coodi:
                rest_distance.append(line_distance(j_list[step],j_list[step+1],coodi2))
            dis_max = max(rest_distance)
            rest_distance_point.append(list(map(lambda x: (dis_max - x)*5/dis_max,rest_distance)))
        
        res_idx = []
        res_dispoint = list(map(lambda x : max(x),transpose(rest_distance_point)))
        res_point = list(map(lambda x: x[0] + x[1], zip(res_dispoint,N_point)))
        return list_ranking(res_point)[:30]
            
def list_ranking(n_list):
    enu_list = list(enumerate(n_list))
    enu_list.sort(key=lambda x:x[1],reverse = True)
    return list(map(lambda x:x[0],enu_list))

def degree2radius(degree):
    return degree * (math.pi/180)

def dot_distance(a,b, round_decimal_digits=5):        
    if a[0] is None or a[1] is None or b[0] is None or b[1] is None:
        return None
    assert isinstance(a[0], numbers.Number) and -180 <= a[0] and a[0] <= 180
    assert isinstance(a[1], numbers.Number) and  -90 <= a[1] and a[1] <=  90
    assert isinstance(b[0], numbers.Number) and -180 <= b[0] and b[0] <= 180
    assert isinstance(b[1], numbers.Number) and  -90 <= b[1] and b[1] <=  90

    R = 6371 # 지구의 반경(단위: km)
    dLon = degree2radius(b[0]-a[0])    
    dLat = degree2radius(b[1]-a[1])

    a = math.sin(dLat/2) * math.sin(dLat/2) \
        + (math.cos(degree2radius(a[1])) \
            *math.cos(degree2radius(b[1])) \
            *math.sin(dLon/2) * math.sin(dLon/2))
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * b, round_decimal_digits)

def line_distance(p1,p2,a):
    p1_2 = dot_distance(p1,p2)
    p2_a = dot_distance(p2,a)
    p1_a = dot_distance(p1,a)
    s = (p1_2+p1_a+p2_a)/2
    s_area = math.sqrt(s*(s-p1_2)*(s-p1_a)*(s-p2_a))
    return s_area*2/p1_2

def transpose(matrix):
    rows = []
    trans_matrix = []
    nrows = len(matrix)
    ncols = len(matrix[0])

    for i in range(ncols):
        for j in range(nrows):
            rows.append(matrix[j][i])
        trans_matrix.append(rows)
        rows = []

    return trans_matrix


if __name__ == "__main__":

    res_idx = rest_sort([[126.97701954045031,37.57959997444933],[126.96506706901754, 37.53570566852152]])
    
    print(res_idx)