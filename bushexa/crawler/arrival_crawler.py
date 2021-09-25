from bushexa.timetable.consts import get_stop_list
import requests
import xmltodict
import json
import time
from itertools import product

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from timetable.models import ArrivalInfo

from bushexa.api.apitools import get_key

error_log_path = './log.txt'

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


def iter_crawl_arrival(stop_id, page, row):
    # Request XML
    arrival_xml = request_arrival(stop_id=stop_id, page=page, row=row)

    # Parse XML
    total_cnt, info = parse_arrival_xml(arrival_xml)

    # Iterate each row
    for r in info:
        print(r)
        vehicle_no = r['VEHICLENO']
        route_id = r['ROUTEID']

        remain_time = r['ARRIVALTIME']
        stop_cnt = r['PREVSTOPCNT']
        stop_name = r['PRESENTSTOPNM']

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


if __name__=='__main__':
    crawl_arrival()