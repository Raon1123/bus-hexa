import requests
import xmltodict

from .tools.getkey import get_key

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

    response = requests.get(url, params=params)

    # TODO : do error check on the responses

    xml = response.text

    resdict = xmltodict.parse(xml)

    return resdict


def store_bus_pos(lane, resdict):
    ## structure of created resdict dictionary is : 
    # resdict - response - head - resultcode, resultmsg
    #                    - body - items, numofrows, pageno, totalcount
    # for thing in resdict[response][body][items][item] => each bus of response
    new_poses = None
    new_posofbus = []
    if resdict['response']['body']['totalCount'] == '0':
        PosOfBus.objects.filter(route_key=lane).delete()
        return
    elif resdict['response']['body']['totalCount'] == '1':
        new_poses = [resdict['response']['body']['items']['item']]
    else:
        new_poses = resdict['response']['body']['items']['item']

    for newbus in new_poses:
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
        resdict = request_bus_pos(lane)
        store_bus_pos(lane, resdict)
