from timetable.tools.consts import get_stop_list
import requests
import time
import traceback

from timetable.models import ArrivalInfo

from .apitools import get_key, parse_xml
from .consts import error_log_path

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
    if response.status_code != 200:
        time_msg = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        msg = "Fail Arrival Request!\n route:" + stop_id + \
              "TIME: " + time_msg + '\n'
        raise Exception(msg)

    # Get response text
    xml = response.text

    return xml


def iter_crawl_arrival(stop_id, page, row):
    # Request XML
    arrival_xml = request_arrival(stop_id=stop_id, page=page, row=row)

    # Parse XML
    total_cnt, info = parse_xml(arrival_xml)

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
        print("Stop: %s" % stop)
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
                err_file.write('\n\n')
                err_file.write(str(traceback.format_exc()))
                break

            if page * row < total_cnt:
                continue
            break

    err_file.close()

