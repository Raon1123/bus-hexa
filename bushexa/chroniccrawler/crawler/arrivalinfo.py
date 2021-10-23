import requests
import xmltodict

from .tools.getkey import get_key

from chroniccrawler.models import UlsanBus_LaneToTrack, UlsanBus_NodeToTrack, UlsanBus_ArrivalInfo


# Get all nodes to request from database
def get_all_nodes_to_request():
    nodes = UlsanBus_NodeToTrack.objects.all()
    
    return nodes


# Request bus arrival informations for a node
def request_arrival_info(node):
    key = get_key()
    nor = '32'
    pn = '1'
    
    url = 'http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo'

    params = {'serviceKey': key, 'numOfRows': nor, 'pageNo': pn,
              'stopid': node.node_id}

    response = requests.get(url, params=params)

    xml = response.text

    resdict = xmltodict.parse(xml)

    return resdict


# Store arrival information
def store_arrival_info(node, resdict):
    ## structure of created resdict dictionary is :
    # resdict - tableInfo - pageno, numofrows, totalcnt, resultcode, resultmsg
    #                     - list - row - vehicleno, rnum, prevstopcnt, arrivaltime,
    #                                    routeid, stopid, stopnm, presentstopnm, routem
    new_arrivals = None
    new_arrlist = []
    if resdict['tableInfo']['totalCnt'] == '0':
        UlsanBus_ArrivalInfo.objects.filter(node_key_usb=node).delete()
        return
    elif resdict['tableInfo']['totalCnt'] == '1':
        new_arrivals = [resdict['tableInfo']['list']['row']]
    else:
        new_arrivals = resdict['tableInfo']['list']['row']

    UlsanBus_ArrivalInfo.objects.filter(node_key_usb=node).delete()
    for new_arr in new_arrivals:
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
                                       vehicle_no=vehicleno)
        arrinfo.save()


# Call this function for getting all arrival informations
def do_arrivalinfo():
    nodes = get_all_nodes_to_request()

    for node in nodes:
        resdict = request_arrival_info(node)
        store_arrival_info(node, resdict)
