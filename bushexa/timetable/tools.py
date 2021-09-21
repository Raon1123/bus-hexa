from .consts import get_stop_list
import requests
import xmltodict
import json
import time
from itertools import product

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bushexa.settings")

import django
django.setup()

from timetable.models import ArrivalInfo

from apitools import get_key

error_log_path = './log.txt'


def get_busno(route_id):
    return route_id[5:8]


def request_arrival(stop_id, page=1, row=10):
    # Check input data type
    if type(stop_id) is not str:
        stop_id = str(stop_id)
    if type(page) is not str:
        page = str(page)
    if type(row) is not str:
        row = str(row)

    # Get API key
    key = get_key()

    # Arrival Time URL
    url = "http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo"

    # API parameter
    params = {'serviceKey': key,
              'pageNo': page,
              'numOfRows': row,
              'stopid': stop_id}

    # Request to API
    response = requests.get(url, params=params)
    
    # Fail timetable request
    if response.status_code is not 200:
        time_msg = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        msg = "Fail Arrival Request!\n route:" + stop_id + \
              "TIME: " + time_msg + '\n'
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
def parse_arrival_xml(xml):
    # JSON parser
    js = xmltodict.parse(xml)
    js_dict = json.loads(json.dumps(js))

    # Get parsed contents
    cnt = int(js_dict['tableInfo']['totalCnt'])
    info_dict = js_dict['tableInfo']['list']['row']

    return cnt, info_dict


def get_337_dir(vehicle_no, remain_cnt):
    ans = '3'

    # 무동 정류장 기준
    # 무동: 30434
    # remain + 3
    mudong_id = '196030434'

    arrival_xml = request_arrival(stop_id=mudong_id, page=1, row=20)
    _, info = parse_arrival_xml(arrival_xml)

    for row in info:
        mudong_vehicle_no = row['VEHICLENO']
        mudong_stop_cnt = row['PREVSTOPCNT']
        mudong_route_id = row['ROUTEID']

        if get_busno(mudong_route_id) != '337':
            continue
        
        if (mudong_vehicle_no == vehicle_no) and (int(mudong_stop_cnt) < 73):
            ans = '2'
        else:
            ans = '1'

    return ans


def iter_crawl_arrival(stop_id, page, row):
    # Request XML
    arrival_xml = request_arrival(stop_id=stop_id, page=page, row=row)

    # Parse XML
    total_cnt, info = parse_arrival_xml(arrival_xml)

    # Iterate each row
    for row in info:
        vehicle_no = row['VEHICLENO']
        route_id = row['ROUTEID']

        remain_time = row['ARRIVALTIME']
        stop_cnt = row['PREVSTOPCNT']
        stop_name = row['PRESENTSTOPNM']

        if get_busno(route_id) == '337':
            dir = get_337_dir(vehicle_no, stop_cnt)
            route_id = route_id[:-1] + dir
            
            filter337 = ArrivalInfo.objects.filter(vehicle_no__exact=vehicle_no,
                                                   stop_cnt__exact=stop_cnt)
            
            if len(filter337) != 0:
                continue
            
        table = ArrivalInfo(stop_id=stop_id,
                            vehicle_no=vehicle_no,
                            route_id=route_id,
                            remain_time=remain_time,
                            stop_cnt=stop_cnt,
                            stop_name=stop_name)
        table.save()

    return total_cnt


def crawl_arrival():
    stops = get_stop_list()

    # Error log file
    err_file = open(error_log_path, 'a')

    for stop in stops:
        page = 1
        row = 10

        # Reset Data
        entries = ArrivalInfo.objects.filter(stop_id__exact=stop)
        entries.delete()

        while True:
            try:
                total_cnt = iter_crawl_arrival(stop_id=stop,
                                               page=page,
                                               row=row)
                page += 1
            except Exception as e:
                err_file.write(str(e))
                break

            if page * row < total_cnt:
                continue
            break

    err_file.close()

"""
출발 시간을 예쁘게 표시하는 함수
예) 1100 => 11:00
"""
def pretty_time(timestr):
    if type(timestr) is not str:
        timestr = str(timestr)

    pretty = timestr[:2] + ':' + timestr[2:]

    return pretty


"""
잔여 시간을 예쁘게 표시하는 함수
예) 123 => 2분 후
"""
def pretty_remain(timestr):
    if type(timestr) is not str:
        timestr = str(timestr)

    timeint = int(timestr)

    remainmin = timeint // 60

    if remainmin > 0:
        ans = str(remainmin) + '분 후'
    else:
        ans = '1분 이내 도착'

    return ans

