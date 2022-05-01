from chroniccrawler.models import *


def get_lanename(lane):
    return lane.bus_name


def get_landmarknodes(lane):
    lms = LandmarkOfLane.objects.get(route_key=lane).landmark_keys.all()\
                                .select_related('alias_key__alias_name')\
                                .values_list('alias_key__alias_name', flat=True).distinct()
    lmslist = [lm for lm in lms]
    return lmslist


def get_nodes(lane):
    nodes = NodeOfLane.objects.filter(route_key=lane).order_by('node_order').values('node_order', 'node_name')
    nodesdict = {}
    for n in nodes:
        nodesdict[n['node_order']] = n['node_name']
    return nodesdict


def get_timetables(lane):
    tts = UlsanBus_TimeTable.objects.filter(route_key_usb__route_key=lane).order_by('depart_seq')
    ttsdict = {}
    for tt in tts:
        ttsdict[tt.depart_seq] = tt.depart_time[:2] + ":" + tt.depart_time[2:]
    return ttsdict


def get_positions(lane):
    poss = PosOfBus.objects.filter(route_key=lane).order_by('node_order')

    posslist = [{"node_order": p.node_order,
                 "bus_num": p.bus_num,
                 "node_id": p.node_id,} for p in poss]

    return posslist


def build_response_dict(lane):
    rd = {
        "lanename": get_lanename(lane),
        "landmarknodes": get_landmarknodes(lane),
        "nodes": get_nodes(lane),
        "timetables": get_timetables(lane),
        "positions": get_positions(lane),
    }

    return rd
