import requests
import xmltodict
import json
import time
from itertools import product

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bushexa.settings")

import django
django.setup()

from timetable.models import BusTimetable

from apitools import get_key

error_log_path = './log.txt'


"""
Ulsan API에게 출발시간 정보를 요청하는 부분

Input
- route: 버스번호 eg) 133, 233
- day: 요일구분, 0-평일, 1-토요일, 2-주말,공휴일, 3-방학평일, 4-방학토요일, 5-방학일요일
- page: 요청 페이지

Output
- xml: 받은 xml 형식의 파일
"""
def request_time(route, week=0, page=1, row=10):
    # Check input data type
    if type(route) is not str:
        route = str(route)
    if type(week) is not str:
        day = str(week)
    if type(page) is not str:
        page = str(page)
    if type(row) is not str:
        row = str(row)

    # Get API key
    key = get_key()

    # Timetalbe URL
    url = "http://openapi.its.ulsan.kr/UlsanAPI/BusTimetable.xo"

    # API parameter
    params = {'serviceKey': key,
              'pageNo': page,
              'numOfRows': row, 
              'routeNo': route,
              'dayOfWeek': week}

    # Request to API
    response = requests.get(url, params=params)
    
    # Fail timetable request
    if response.status_code is not 200:
        time_msg = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        msg = "Fail Time Request!\n route:" + route + \
                " day: " + day + "TIME: " + time_msg + '\n'
        raise Exception(msg)

    # Get response text
    xml = response.text

    return xml

"""
울산 버스 API로 부터 받은 json 파일 파싱
Input
- xml: API로 부터 받은 xml 파일

Output
- cnt: 조회된 총 timetable의 개수
- info_dict: 각 row를 dictonary를 가진 list 형태로 파싱

"""
def parse_time_xml(xml):
    # JSON parser
    js = xmltodict.parse(xml)
    js_dict = json.loads(json.dumps(js))

    # Get parsed contents
    cnt = int(js_dict['tableInfo']['totalCnt'])
    info_dict = js_dict['tableInfo']['list']['row']

    return cnt, info_dict


def iter_crawl_time(route, page, row, week):
    # Request XML
    time_xml = request_time(route=route, page=page, row=row, week=week)

    # Parse XML
    total_cnt, info = parse_time_xml(time_xml)

    # Iterate each timetable
    for r in info:
        bus_dir = r['DIRECTION']
        bus_time = r['TIME']

        # Add django table
        table = BusTimetable(bus_no=route,
                             bus_dir=bus_dir,
                             bus_time=bus_time,
                             bus_week=week)
        table.save()
    
    return total_cnt


def crawl_time():
    # Constants
    routes = [133, 733, 743, 304, 233, 337]
    weeks = [0, 1, 2, 3, 4, 5]

    # Error log file
    err_file = open(error_log_path, 'a')

    for route, week in list(product(*[routes, weeks])):
        print("Route: "+ str(route) + " Week: " + str(week))
        page = 1 # DEFAULT setting of Ulsan BIS
        row = 10 # DEFAULT setting of Ulsan BIS

        # Delete Current Table
        if week is weeks[0]:
            entries = BusTimetable.objects.filter(bus_no__exact=route)
            entries.delete()

        # For get every timetable, using iteration
        while True:
            try:
                total_cnt = iter_crawl_time(route=route,
                                            page=page,
                                            row=row,
                                            week=week)
            # Fail API call
            except Exception as e:
                err_file.write(str(e))
                break
            
            # If remain, continue
            if page * row < total_cnt:
                page = page + 1
                continue
            break

    err_file.close()


if __name__=='__main__':
    crawl_time()
