import requests
import xmltodict

from .tools.getkey import get_key

from chroniccrawler.models import UlsanBus_LaneToTrack, UlsanBus_TimeTable


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = UlsanBus_LaneToTrack.objects.all()

    return lanes


# Request timetable for a lane
def request_time_table(lane, dayOfWeek):
    serviceKey = get_key()

    pageNo = '1'
    numOfRows = '255'
    routeNo = lane.route_num

    url = 'http://openapi.its.ulsan.kr/UlsanAPI/BusTimetable.xo'

    params = {'serviceKey': serviceKey, 'pageNo': pageNo,
                'numOfRows': numOfRows, 'routeNo': routeNo, 'dayOfWeek': dayOfWeek}

    response = requests.get(url, params=params)

    xml = response.text

    resdict = xmltodict.parse(xml)

    return resdict


def store_time_table(lane, resdict, dayOfWeek):
    ## structure of resdict :
    # resdict - tableInfo - pageno, numofrows, totalcnt, resultcode, resultmsg
    #                     - list - row - direction, time, class, rnum, routename, routeno, dptcseqno
    # for thing in resdict[tableinfo][list] => each time of response
    new_times = None
    new_timeslist = []
    if resdict['tableInfo']['totalCnt'] == '0':
        UlsanBus_TimeTable.objects.filter(route_key_usb=lane).delete()
        return
    elif resdict['tableInfo']['totalCnt'] == '1':
        new_times = [resdict['tableInfo']['list']['row']]
    else:
        new_times = resdict['tableInfo']['list']['row']

    for new_time in new_times:
        if new_time['CLASS'] == str(lane.route_class) and new_time['DIRECTION'] == str(lane.route_direction):
            departtime = new_time['TIME']
            departseq = int(new_time['DPTCSEQNO'])
            onetime = UlsanBus_TimeTable(route_key_usb=lane, depart_time=departtime, depart_seq=departseq)
            new_timeslist.append(onetime)

    UlsanBus_TimeTable.objects.filter(route_key_usb=lane).delete()
    for newone in new_timeslist:
        newone.save()


# Call this function for crawling all bus positions
def do_timetable(dayOfWeek):
    lanes = get_all_lanes_to_request()

    for lane in lanes:
        resdict = request_time_table(lane, dayOfWeek)
        store_time_table(lane, resdict, dayOfWeek)
