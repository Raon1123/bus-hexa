from .tools.getkey import get_key
from .tools.requestor import request_dicts
from .tools.listifier import element_list

from chroniccrawler.models import UlsanBus_LaneToTrack, UlsanBus_NodeToTrack, UlsanBus_ArrivalInfo


# Get all nodes to request from database
def get_all_nodes_to_request():
    nodes = UlsanBus_NodeToTrack.objects.all()
    
    return nodes


# Ready lists of requests
def ready_request(nodes):
    node_url_params = []
    key = get_key()
    nor = '32'
    pn = '1'
    url = 'http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo'
    for node in nodes:
        params = {'serviceKey': key, 'numOfRows': nor, 'pageNo': pn,
              'stopid': node.node_id}

        node_url_params.append((node, url, params))

    return node_url_params


# Store arrival information
def store_arrival_info(node, info):
    UlsanBus_ArrivalInfo.objects.filter(node_key_usb=node).delete()
    for new_arr in info:
        routekey = None
        try:
            routekey = UlsanBus_LaneToTrack.objects.get(route_id=new_arr['ROUTEID'])
        except UlsanBus_LaneToTrack.DoesNotExist:
            continue
        vehicleno = new_arr['VEHICLENO']
        arrivaltime = new_arr['ARRIVALTIME']
        stopcnt = new_arr['PREVSTOPCNT']
        stopname = new_arr['PRESENTSTOPNM']

        arrinfo = UlsanBus_ArrivalInfo(route_key_usb=routekey, node_key_usb=node,
                                       prev_stop_cnt=stopcnt, arrival_time=arrivaltime,
                                       vehicle_no=vehicleno, current_node_name=stopname)
        arrinfo.save()


# Call this function for getting all arrival informations
def do_arrivalinfo():
    nodes = get_all_nodes_to_request()

    n_u_ps = ready_request(nodes)

    thing_rdicts = request_dicts(n_u_ps)

    for tr in thing_rdicts:
        info = element_list(['tableInfo', 'totalCnt'], tr[1], ['tableInfo', 'list', 'row'])
        store_arrival_info(tr[0], info)
