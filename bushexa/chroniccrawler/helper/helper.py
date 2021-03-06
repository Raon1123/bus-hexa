import sys
import datetime
import copy

from django.db.models import Exists, OuterRef

from chroniccrawler.models import *


# format 1st
def format_arrival_list(lanes):
    # add format and time
    for lane in lanes:
        lane['remain_stops'] = lane['arrival'].prev_stop_cnt
        lane['thing'] = {'remain_time': str(lane['arrival'].arrival_time // 60) + '분 후',
                         'stop_name': lane['arrival'].current_node_name,
                         'vehicle_no': lane['arrival'].vehicle_no[2:]}
    return lanes

# 1st : get arrival part
def get_arrival_list(parts):
    # add lane
    lanes = [{'part': p, 'lane': p.lane_key,} for p in parts]
    # add usblane
    usblanes = UlsanBus_LaneToTrack.objects.filter(route_key__in=[l['lane'] for l in lanes])
    for lane in lanes:
        for usbl in usblanes:
            if lane['lane'] == usbl.route_key:
                lane['usblane'] = usbl
    # add arrival
    arrs = UlsanBus_ArrivalInfo.objects.filter(route_key_usb__in=[l['usblane']for l in lanes])
    for lane in lanes:
        for arr in arrs:
            if lane['usblane'] == arr.route_key_usb:
                lane['arrival'] = arr
    # pop
    popthese = []
    for a in range(len(lanes)):
        try:
            lanes[a]['arrival'] #lol
        except KeyError:
            popthese.append(a)
    popthese.reverse()
    for a in popthese:
        lanes.pop(a)
    # format
    return format_arrival_list(lanes)


# format 2nd
def format_position_list(lanes):
    # add format and position
    for lane in lanes:
        lane['remain_stops'] = lane['part'].last_node_key.node_order - lane['pos'].node_order
        lane['thing'] = {'remain_time': str(lane['remain_stops']) + '역 전',
                         'stop_name': NodeOfLane.objects.get(route_key=lane['lane'],
                                                             node_order=lane['pos'].node_order).node_name,
                         'vehicle_no': lane['pos'].bus_num[2:]}
    return lanes

# 2nd : get position part
def get_position_list(parts):
    # filter away parts that are departure only
    nparts = []
    for part in parts:
        if part.only_departure() == False:
            nparts.append(part)
    # add lane
    lanes = [{'part': p, 'lane': p.lane_key} for p in nparts]
    # add position
    poss = PosOfBus.objects.filter(route_key__in=[l['lane'] for l in lanes])
    planes = []
    for lane in lanes:
        for pos in poss:
            if lane['lane'] == pos.route_key:
                plane = copy.deepcopy(lane)
                plane['pos'] = pos
                planes.append(plane)
    # filter away position that are out of part
    nlanes = []
    for lane in planes:
        if lane['part'].in_part(lane['pos']):
            nlanes.append(lane)
    # format
    return format_position_list(nlanes)


# 3rd : get dispatch part
def get_dispatch_list(parts, count):
    dispatches = PartOfLane.objects.raw('SELECT * FROM (SELECT * FROM (SELECT * FROM chroniccrawler_partoflane WHERE id IN ({})) AS pol INNER JOIN chroniccrawler_ulsanbus_lanetotrack AS ultt ON pol.lane_key_id=ultt.route_key_id INNER JOIN chroniccrawler_ulsanbus_timetable AS tt ON tt.route_key_usb_id=ultt.id) AS inne INNER JOIN chroniccrawler_nodeoflane AS nol ON inne.first_node_key_id=nol.id ORDER BY inne.depart_time ASC;'.format(", ".join([str(p.id) for p in parts])))

    things = []
    now = datetime.datetime.now()
    nowformat = now.hour * 100 + now.minute
    cc = 0
    for dp in dispatches:
        if cc >= count:
            break
        if int(dp.depart_time) >= nowformat:
            only_departure = dp.first_node_key == dp.last_node_key and dp.node_order == 1
            things.append(  {
                                'remain_stops': sys.maxsize,
                                'dptime': int(dp.depart_time),
                                'thing':
                                    {
                                        'bus_time': dp.depart_time[0:2]+':'+dp.depart_time[2:4],
                                        'only_departure': only_departure,
                                    },
                            })
    return things


# Cleanup duplicates inside functions
def cleanup_arrivals_and_positions(arrs, poss):
    # Find duplicate entries that are in both arrivals and positions and delete from positions
    # Fix wrong arrival info : 337 is a ############
    newarrs = []
    newposs = []

    for pos in poss:
        couple = False
        for arr in arrs:
            if arr['arrival'].vehicle_no == pos['pos'].bus_num:
                couple = True
                newarrs.append(arr)
        if not couple:
            newposs.append(pos)
    
    return newarrs, newposs# newarrivals, newpositions

# Construct information for next n bus'
def next_n_bus_from_alias(alias, n):
    count = n

    #maps = MapToAlias.objects.filter(alias_key=alias).values_list('lane_key', 'count')

     
    parts = PartOfLane.objects.filter(
                    Exists(
                            MapToAlias.objects.filter(
                                    lane_key_id=OuterRef('lane_key_id'), count=OuterRef('count'), alias_key=alias
                            )
                    )
            ).select_related('lane_key', 'first_node_key', 'last_node_key')
    
    only_departure = True
    for p in parts:
        now_only_departure = p.first_node_key == p.last_node_key and p.first_node_key.node_order == 1
        only_departure = only_departure and now_only_departure

    arrivals = get_arrival_list(parts)
    positions = get_position_list(parts)
    dispatches = get_dispatch_list(parts, count)

    if arrivals is None:
        arrivals = []
    if positions is None:
        positions = []
    if dispatches is None:
        dispatches = []

    arrivals, positions = cleanup_arrivals_and_positions(arrivals, positions)

    total = arrivals + positions + dispatches
    sort = sorted(total, key=lambda d: d['remain_stops'])
    nextn = None
    while len(sort) < n:
        sort.append({'thing': {'no_data': 'No_data'}})
    if n > 0:
        nextn = [s['thing'] for s in sort[0:n]]
    elif n == 0:
        nextn = [s['thing'] for s in sort]
    ret = {'pk': alias.id, 'bus_name': alias.alias_name, 'stop_info': nextn, 'only_departure': only_departure}
    return ret
