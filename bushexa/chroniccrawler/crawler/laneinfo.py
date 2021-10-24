import itertools

from .tools.getkey import get_key
from .tools.requestor import request_dict
from .tools.listifier import element_list

from chroniccrawler.models import LaneToTrack, NodeOfLane


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = LaneToTrack.objects.all()

    return lanes

# Request lane information for a lane
def request_lane_info(lane):
    # Parse station information of one lane : start
    serviceKey = get_key()
    numOfRows = '200'
    pageNo = '1'
    cityCode = lane.city_code
    routeId = lane.route_id

    url = 'http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteAcctoThrghSttnList'

    params = {'serviceKey': serviceKey, 'numOfRows': numOfRows, 'pageNo': pageNo,
              'cityCode': cityCode, 'routeId': routeId}

    rdict = request_dict(url, params)

    count = rdict['response']['body']['totalCount']
    elem  = ['response', 'body', 'items', 'item']

    info = element_list(count, rdict, elem)

    return info


def store_lane_info(lane, info):
    new_nodes = info
    original_nodes = NodeOfLane.objects.filter(route_key=lane).order_by('node_order')
    are_the_two_different = False
    if len(original_nodes) != len(new_nodes):
        are_the_two_different = True
    else:
        for ori, new in zip(original_nodes, new_nodes):
            if ori.node_id != new['nodeid']:
                are_the_two_different = True
                break
            if ori.node_name != new['nodenm']:
                are_the_two_different = True
                break

    if are_the_two_different == True:
        NodeOfLane.objects.filter(route_key=lane).delete()
        for onenode in new_nodes:
            nodeord = onenode['nodeord']
            nodeid = onenode['nodeid']
            nodenm = onenode['nodenm']
            onenodeoflane = NodeOfLane(route_key=lane, node_order=nodeord,
                                        node_id=nodeid, node_name=nodenm)
            onenodeoflane.save()


# Call this function for crawling all lane informations
def do_laneinfo():
    lanes = get_all_lanes_to_request()

    for lane in lanes:
        info = request_lane_info(lane)
        store_lane_info(lane, info)
