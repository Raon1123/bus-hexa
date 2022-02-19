import itertools

from .tools.getkey import get_key
from .tools.requestor import request_dicts
from .tools.listifier import element_list

from chroniccrawler.models import LaneToTrack, NodeOfLane


# Get all lanes to request from database
def get_all_lanes_to_request():
    lanes = LaneToTrack.objects.all()

    return lanes

# Ready lists of lane informations
def ready_request(lanes):
    lane_url_params = []
    serviceKey = get_key()
    numOfRows = '200'
    pageNo = '1'
    url = 'http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteAcctoThrghSttnList'
    for lane in lanes:
        params = {'serviceKey': serviceKey, 'numOfRows': numOfRows, 'pageNo': pageNo,
                  '_type': 'xml', 'cityCode': lane.city_code, 'routeId': lane.route_id}

        lane_url_params.append((lane, url, params))

    return lane_url_params


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

    l_u_ps = ready_request(lanes)

    lane_rdicts = request_dicts(l_u_ps)

    for lr in lane_rdicts:
        info = element_list(['response', 'body', 'totalCount'], lr[1],
                            ['response', 'body', 'items', 'item'])
        store_lane_info(lr[0], info)
