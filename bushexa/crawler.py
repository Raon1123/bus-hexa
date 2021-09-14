import requests
import xmltodict
import json
import time

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bushexa.settings")

import django
django.setup()

from timetable.models import BusTimetable

error_log_path = './log.txt'

"""
API key를 읽는 함수

Input
- path: API key의 위치, 기본은 bushexa/crawler/key.txt

Output
- key: API key

"""
def get_key(path='./key.txt'):
    key_file = open(path, 'r')

    key = key_file.read()
    key = requests.utils.unquote(key)

    key_file.close()

    return key


"""
Ulsan API에게 출발시간 정보를 요청하는 부분

Input
- route: 버스번호 eg) 133, 233
- day: 요일구분, 0-평일, 1-토요일, 2-주말,공휴일, 3-방학평일, 4-방학토요일, 5-방학일요일
- page: 요청 페이지

Output
- xml: 받은 xml 형식의 파일
"""
def request_time(route, day=0, page=1, row=10):
    # Check input data type
    if type(route) is not str:
        route = str(route)
    if type(day) is not str:
        day = str(day)
    if type(page) is not str:
        page = str(page)
    if type(row) is not str:
        row = str(row)

    # Get API key
    key = get_key()

    # Timetalbe URL
    url = 'http://openapi.its.ulsan.kr/UlsanAPI/BusTimetable.xo'

    # API parameter
    params = {'serviceKey': key,
              'pageNo': page,
              'numOfRows': row, 
              'routeNo': route,
              'dayOfWeek': day}

    # Request to API
    response = requests.get(url, params=params)
    
    # Fail timetable request
    if response.status_code is not 200:
        time_msg = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        msg = "Fail Time Request! route:" + route + " day: " + day + "TIME: " + time_msg
        raise Exception(msg)

    # Get response text
    xml = response.text

    return xml


def parse_time_xml(xml):
    js = xmltodict.parse(xml)
    js_dict = json.loads(json.dumps(js))

    # Get parsed contents
    cnt = int(js_dict['tableInfo']['totalCnt'])
    info_dict = js_dict['tableInfo']['list']['row']

    return cnt, info_dict


def crawl_time():
    # Constants
    routes = [133, 733, 743]

    timetable = {}

    # Error log file
    err_file = open(error_log_path, 'a')

    for route in routes:
        page = 1
        row = 10
        timetable[route] = {'1':[], '2':[]}

        # For get every timetable, using iteration
        while True:
            try:
                time_xml = request_time(route=route, page=page, row=row)
                tot, info = parse_time_xml(time_xml)

                # Iterate each timetable
                for r in info:
                    bus_dir = r['DIRECTION']
                    bus_time = r['TIME']

                    # Add django table
                    table = BusTimetable(bus_no=route,
                                         bus_dir=bus_dir,
                                         bus_time=bus_time)
                    table.save()

                page = page + 1
            except Exception as e:
                err_file.write(str(e))
                break
            
            # If remain, continue
            if page * row < tot:
                continue
            break

    err_file.close()


if __name__=='__main__':
    crawl_time()
