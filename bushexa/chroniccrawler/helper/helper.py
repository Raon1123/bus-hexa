from chroniccrawler.models import *

# Get position from arrivalinfo
def get_pos_from_arrival(arr):
    pos = PosOfBus.objects.filter(bus_num=arr.vehicle_no)
    if len(pos) == 0:
        return -1
    pos = pos[0]
    
    return pos







# 1st : get arrival part
def get_arrival_list(parts):
    lanes = [p.lane_key for p in parts]
    usblanes = UlsanBus_LaneToTrack.objects.filter(route_key__in=lanes)
    arrs = UlsanBus_ArrivalInfo.objects.filter(route_key_usb__in=usblanes)
    dicts = [{'remain_second': arr.arrival_time, 'thing': {
              'remain_time': str(arr.arrival_time // 60) + '분 후',
              'stop_name': arr.current_node_name}} for arr in arrs]
    return arr

# 2nd : get position part
def get_position_list(parts, arrivals):
    nparts = []
    for part in parts:
        if part.only_departure() == False:
            nparts.append(part)

    lanes = [p.lane_key for p in nparts]
    poss = PosOfBus.objects.filter(route_key__in=lanes)
    nposs = []
    for pos in poss:
        truth = [part.in_part(pos) for part in nparts]
        if True in truth:
            nposs.append(pos)
            

# Construct information for next n bus'
def next_n_bus_from_alias(alias, n):
    count = n
    parts = LanePart.objects.filter(alias_key=alias)
    arrivals = get_arrival_list(parts)
    positions = get_position_list(parts, arrivals)
