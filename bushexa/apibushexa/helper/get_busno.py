import datetime

from chroniccrawler.models import *


BUSNO_HOW_MUCH_ENTRY_PER_LANE = 2


def get_all_alias():
    alias = LaneAlias.objects.raw("""
        SELECT *, map.lane_key_id as lane_key, nol.node_order as first_node_order, nol2.node_order as last_node_order
        FROM chroniccrawler_lanealias AS la
        INNER JOIN chroniccrawler_maptoalias AS map ON la.id=map.alias_key_id
        INNER JOIN chroniccrawler_partoflane AS pol ON map.lane_key_id=pol.lane_key_id AND map.count=pol.count
        INNER JOIN chroniccrawler_nodeoflane AS nol ON pol.first_node_key_id=nol.id
        INNER JOIN chroniccrawler_nodeoflane AS nol2 ON pol.last_node_key_id=nol2.id;
    """)

    alias_dict = {}

    for a in alias:
        part = {"lane_key": a.lane_key, "first_order": a.first_node_order, "last_order":a.last_node_order}
        if a.id in alias_dict:
            alias_dict[a.id]["part"].append(part)
        else:
            alias_dict[a.id] = {
                "name": a.alias_name,
                "part": [part]
            }

    return alias_dict


def get_all_arrivals():
    # We need : Lane primary key, remain_time, stop_name, vehicle_no, 
    arrivals = UlsanBus_ArrivalInfo.objects.all().select_related('route_key_usb__route_key')

    arrival_dicts = [
        {
            "route_key": arr.route_key_usb.route_key.id,
            "remain_time": arr.arrival_time,
            "stop_name": arr.current_node_name,
            "vehicle_no": arr.vehicle_no,
        }
        for arr in arrivals]

    return arrival_dicts


def build_position_dict(p):
    return {
        "prev_stop": p.ln - p.node_order,
        "vehicle_no": p.bus_num,
        "stop_name": p.nodenm,
    }


def get_all_positions():
    # We need : Lane primary key, bus name, remain_time, stop name, vehicle_no,
    positions = PosOfBus.objects.raw("""
        SELECT pos.pid AS id, pos.aid AS aid, pos.ln AS ln, pos.nodenm AS nodenm
        FROM
        (
            SELECT pob.node_id AS nid, nol.node_name AS nodenm, pob.id AS pid, pob.node_order AS no, polex.aid AS aid, 
            polex.ln AS ln, ROW_NUMBER() OVER
            (
                PARTITION BY polex.aid ORDER BY pob.node_order DESC
            ) AS seq
            FROM
            (
                SELECT *, fnol.node_order AS fn, lnol.node_order AS ln, mta.alias_key_id AS aid, pol.lane_key_id AS lid
                FROM chroniccrawler_partoflane AS pol
                INNER JOIN chroniccrawler_maptoalias AS mta
                ON mta.lane_key_id=pol.lane_key_id AND mta.count=pol.count
                INNER JOIN chroniccrawler_nodeoflane AS fnol
                ON pol.first_node_key_id=fnol.id
                INNER JOIN chroniccrawler_nodeoflane AS lnol
                ON pol.last_node_key_id=lnol.id
            ) AS polex
            INNER JOIN chroniccrawler_posofbus AS pob
            ON polex.lid=pob.route_key_id AND polex.fn <= pob.node_order AND polex.ln >= pob.node_order
            INNER JOIN chroniccrawler_nodeoflane AS nol
            ON pob.route_key_id=nol.route_key_id AND pob.node_id=nol.node_id
        ) AS pos
        WHERE pos.seq < %s
    ;""", [BUSNO_HOW_MUCH_ENTRY_PER_LANE + 1])

    pos_dict = {}
        
    for p in positions:
        if p.aid in pos_dict:
            pos_dict[p.aid].append(build_position_dict(p))
        else:
            pos_dict[p.aid] = [build_position_dict(p)]

    return pos_dict


def get_all_departures():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    four = now.strftime("%H%M")

    timetables = UlsanBus_TimeTable.objects.raw("""
        SELECT *, dep.aid AS aid
        FROM
        (
            SELECT *, mta.alias_key_id AS aid, ROW_NUMBER() OVER 
            (
                PARTITION BY mta.alias_key_id ORDER BY depart_time ASC
            ) AS seq
            FROM chroniccrawler_ulsanbus_timetable AS usbtt
            INNER JOIN chroniccrawler_ulsanbus_lanetotrack AS usbltt
            ON usbltt.id=usbtt.route_key_usb_id
            INNER JOIN chroniccrawler_lanetotrack AS ltt
            ON usbltt.route_key_id=ltt.id
            INNER JOIN chroniccrawler_maptoalias AS mta
            ON mta.lane_key_id=ltt.id
            WHERE depart_time > %s
        ) AS dep
        WHERE seq < %s
        ;
    """, [four, BUSNO_HOW_MUCH_ENTRY_PER_LANE + 1])

    tt_dict = {}
        
    for tt in timetables:
        if tt.aid in tt_dict:
            tt_dict[tt.aid].append(tt.depart_time)
        else:
            tt_dict[tt.aid] = [tt.depart_time]
    return tt_dict


def build_response_dict():

    rd ={
            "alias": get_all_alias(),
            "arrival": get_all_arrivals(),
            "position": get_all_positions(),
            "departure": get_all_departures(),
        }

    return rd
