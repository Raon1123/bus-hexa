from .tools.getkey import get_key
from .tools.requestor import request_dicts
from .tools.listifier import element_list

from chroniccrawler.models import LaneToTrack, PosOfBus


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = LaneToTrack.objects.all()

    return lanes


# Ready lists of requests
def ready_request(lanes):
    lane_url_params = []
    serviceKey = get_key()
    numOfRows = '64'
    pageNo = '1'
    url = 'http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList'
    for lane in lanes:
        params = {'serviceKey': serviceKey, 'numOfRows': numOfRows, 'pageNo': pageNo,
                  '_type': 'xml', 'cityCode': lane.city_code, 'routeId': lane.route_id}

        lane_url_params.append((lane, url, params))

    return lane_url_params


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

    l_u_ps = ready_request(lanes)

    lane_rdicts = request_dicts(l_u_ps)

    for lr in lane_rdicts:
        info = element_list(['response', 'body', 'totalCount'], lr[1],
                            ['response', 'body', 'items', 'item'])
        store_bus_pos(lr[0], info)
