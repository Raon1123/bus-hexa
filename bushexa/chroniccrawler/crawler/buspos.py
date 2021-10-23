from .tools.getkey import get_key
from .tools.requestor import request_dict
from .tools.listifier import element_list

from chroniccrawler.models import LaneToTrack, PosOfBus


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = LaneToTrack.objects.all()

    return lanes


# Request bus position for a lane
def request_bus_pos(lane):
    serviceKey = get_key()
    numOfRows = '64'
    pageNo = '1'
    cityCode = lane.city_code
    routeId = lane.route_id

    url = 'http://openapi.tago.go.kr/openapi/service/BusLcInfoInqireService/getRouteAcctoBusLcList'

    params = {'serviceKey': serviceKey, 'numOfRows': numOfRows, 'pageNo': pageNo,
              'cityCode': cityCode, 'routeId': routeId}

    rdict = request_dict(url, params)

    count = ['response', 'body', 'totalCount']
    elem  = ['response', 'body', 'items', 'item']

    info = element_list(count, rdict, elem)
    
    return info


def store_bus_pos(lane, info):
    new_posofbus = []
    for newbus in info:
        nodeid = newbus['nodeid']
        vehicleno = newbus['vehicleno']
        nodeord = newbus['nodeord']
        oneposofbus = PosOfBus(route_key=lane, node_id=nodeid,
                                bus_num=vehicleno, node_order=nodeord)
        new_posofbus.append(oneposofbus)

    PosOfBus.objects.filter(route_key=lane).delete()
    for newposofbus in new_posofbus:
        newposofbus.save()


# Call this function for crawling all bus positions
def do_buspos():
    lanes = get_all_lanes_to_request()

    for lane in lanes:
        info = request_bus_pos(lane)
        store_bus_pos(lane, info)
