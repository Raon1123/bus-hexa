# 상수들을 저장하는 파일
from datetime import datetime
from pytz import timezone, utc

"""
시간표에 해당하는 요일을 탐색하는 함수
0: 주중
1: 토요일
2: 일요일/공휴일 (공휴일의 경우 추가 구현이 필요함)
3: 방학 주중
4: 방학 토요일
5: 방학 일요일/공휴일
"""
def get_week():
    special_day = ['0921', '0922']
    now = datetime.now(timezone('Asia/Seoul'))

    weekday = now.weekday()
    if weekday < 5:
        week = 0
    elif weekday == 6:
        week = 1
    else:
        week = 2

    month = now.month
    day = now.day
    date = str(month).zfill(2) + str(day).zfill(2)

    if date in special_day:
        week = 2

    return week


"""
현재 시각을 반환하는 함수
시분을 문자열로 반환함.
예) 0915 => 09시 15분
"""
def get_now():
    timenow = datetime.now(timezone('Asia/Seoul'))

    hour = timenow.hour
    minute = timenow.now().minute
    now = str(hour).zfill(2) + str(minute).zfill(2)

    return now


"""
탐색할 정류소 ID 목록
"""
def get_stop_list():
    stops = ['196040234']
    return stops


def get_stop_string(stop_id='196040234'):
    id_dict = {
        '196040234': '울산과학기술원'
    }

    if stop_id in id_dict.keys():
        ans = id_dict[stop_id]
    else:
        ans = "잘못된 접근"

    return ans


"""
정류소별 버스 목록
"""
def get_bus_list(key='196040234'):
    if type(key) is not str:
        key = str(key)

    bus_dict = {'196040234':[
        ['133','2'],['733','2'],['743','2'],['304','1'],['304','2'],['233','3'],['337','1'],['337','2']
    ]}

    if key in bus_dict.keys():
        bus_list = bus_dict[key]
    else:
        bus_list = []

    return bus_list


"""
버스 방향별 종점 목록
"""
def get_bus_dir(bus_no, dir):
    dir_dict = {'133':{'1': '울산과학기술원 방면', '2': '꽃바위 방면'},
                '233':{'3': '농소차고지 방면'},
                '304':{'1': '율리 방면', '2': '복합웰컴센터 방면'},
                '337':{'1': '태화강역 방면', '2': '울산역 경유, 삼남신화 방면', '3': '삼남 순환'},
                '733':{'1': '울산과학기술원 방면', '2': '덕하차고지 방면'},
                '743':{'1': '울산과학기술원 방면', '2': '태화강역 방면'}}
    
    if (bus_no in dir_dict.keys()) and (dir in dir_dict[bus_no].keys()):
        ans = dir_dict[bus_no][dir]
    else:
        ans = "잘못된 조회입니다."

    return ans
        

"""
버스 방향별 경유지 목록
"""
def get_bus_via(bus_no, dir):
    via_dict = {'133':{'1': '울산과학기술원 방면', '2': '구영리, 동강병원, 삼산, 태화강역, 현대중공업 경유'},
                '733':{'1': '울산과학기술원 방면', '2': '구영리, 신복로터리, 울산대학교, 공업탑 경유'},
                '743':{'1': '울산과학기술원 방면', '2': '천상, 신복로터리, 울산대학교, 산단캠퍼스 경유'},
                '304':{'1': '천상, 신복로터리, 울산대학교 경유', '2': '울산역 경유'},
                '337':{'3': '울산역, 구영리, 태화강역 경유'},
                '233':{'1': '울산과학기술원 방면', '2':'구영리, 성남동, 울산공항 경유', '3':'구영리, 성남동, 울산공항 경유'}}
    
    if (bus_no in via_dict.keys()) and (dir in via_dict[bus_no].keys()):
        ans = via_dict[bus_no][dir]
    else:
        ans = "잘못된 조회입니다."

    return ans


def get_stop_via(stop_id='196040234'):
    stop_via_dict = {'196040234': [
        1
    ]}

    ans = {}
    
    return ans