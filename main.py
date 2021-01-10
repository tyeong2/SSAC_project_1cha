#자동차 경로 최적화 모듈
from getOrderOptimized import *

#대중교통 경로 최적화 모듈
from logicTourplace import *

#식당 정렬 모듈
from restaurant_sort import *


if __name__ == '__main__':
    #1. 사용자 데이터 입력받음
    with open('user01.txt','r',encoding='utf-8') as user:
        userData = user.read().split('\n')        
        startTime = ''.join(userData[2].split('-'))+userData[4]+'00'


    #2. 사용자 입력 데이터를 바탕으로 추천 관광지 목록 생성
    tourMain()


    #3. 사용자가 방문하고 싶은 관광지 선택


    #4. 방문 경로 최적화
    with open('tour01.txt','r',encoding='utf-8') as tour:
        viaPoint = tour.readline().strip(', ').split(',')
        print(viaPoint)
    with open('res01.txt','r',encoding='utf-8') as food:
        foodPoint = food.readline().strip(', ').split(',')
        print(foodPoint)
    #사용자 이동수단이 '자동차'일 경우
    if userData[6] == '자동차':
        getOrderOpt(userData[3], startTime, userData[5], *viaPoint)
    #사용자 이동수단이 '대중교통'일 경우
    elif userData[6] == '대중교통':
        restaurant_Sort()

    #5. 완성된 동선을 보여준다.
