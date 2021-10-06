import requests
import xmltodict

import datetime

from .getkey import get_key

from chroniccrawler.models import DayInfo


def get_time():
    return datetime.datetime.now()


def request_dayinfo(now):
    key = get_key()
    rows = '32'
    year = now.strftime("%Y")
    month = now.strftime("%m")

    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"

    params = {'serviceKey': key, 'numOfRow': rows, 'solYear': year, 'solMonth': month}

    response = requests.get(url, params=params)

    xml = response.text

    resdict = xmltodict.parse(xml)

    return resdict


def store_dayinfo(now, resdict):
    newlist = None
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    DayInfo.objects.all().delete()

    # Day name, kind setting    
    name = None
    kind = 0
    if now.strftime("%w") == "0":
        name = "일요일"
        kind = 2
    elif now.strftime("%w") == "6":
        name = "토요일"
        kind = 1
    else:
        name = "주중"
        kind = 0
    
    # Special day check
    if resdict['response']['body']['totalCount'] == '0':
        newlist = []
    elif resdict['response']['body']['totalCount'] == '1':
        newlist = [resdict['response']['body']['items']['item']]
    else:
        newlist = resdict['response']['body']['items']['item']

    for oneday in newlist:
        if oneday['locdate'] == year + month + day and oneday['isHoliday'] == 'Y':
            name = oneday['dateName']
            kind = 2

    today = DayInfo(year=year, month=month, day=day, name=name, kind=kind)
    today.save()


# Call this function for crawling information of the day
def do_dayinfo():
    now = get_time()
    resdict = request_dayinfo(now)
    store_dayinfo(now, resdict)
