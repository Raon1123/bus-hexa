from .tools.getkey import get_key
from .tools.requestor import request_dicts
from .tools.listifier import element_list

from chroniccrawler.models import UlsanBus_LaneToTrack, UlsanBus_TimeTable


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = UlsanBus_LaneToTrack.objects.all()

    return lanes


# Ready lists of requests
def ready_request(lanes, dayOfWeek):
    lane_url_params = []
    serviceKey = get_key()
    pageNo = '1'
    numOfRows = '255'
    url = 'http://openapi.its.ulsan.kr/UlsanAPI/BusTimetable.xo'
    for lane in lanes:
        params = {'serviceKey': serviceKey, 'pageNo': pageNo,'numOfRows': numOfRows, 
                  'routeNo': lane.route_num, 'dayOfWeek': dayOfWeek}

        lane_url_params.append((lane, url, params))

    return lane_url_params


def store_time_table(lane, info):
    ## structure of resdict :
    # resdict - tableInfo - pageno, numofrows, totalcnt, resultcode, resultmsg
    #                     - list - row - direction, time, class, rnum, routename, routeno, dptcseqno
    # for thing in resdict[tableinfo][list] => each time of response
    new_timeslist = []

    for new_time in info:
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

    l_u_ps = ready_request(lanes, dayOfWeek)

    lane_rdicts = request_dicts(l_u_ps)

    for lr in lane_rdicts:
        info = element_list(['tableInfo', 'totalCnt'], lr[1], ['tableInfo', 'list', 'row'])
        store_time_table(lr[0], info)
