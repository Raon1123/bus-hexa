from chroniccrawler.models import *


'''
def get_all_parts():
    
    parts = PartOfLane.objects.all().values()

    lane_main = {}
    for p in parts:
        if lane_main

    return PartOfLane.objects.all()
'''

def get_all_arrivals():
    # We need : Lane primary key, remain_time, stop_name, vehicle_no, 
    arrivals = UlsanBus_ArrivalInfo.objects.all().select_related('route_key_usb__route_key')

    arrival_dicts = [
        {
            "pk": arr.route_key_usb.route_key.id,
            "remain_time": arr.arrival_time,
            "stop_name": arr.current_node_name,
            "vehicle_no": arr.vehicle_no,
        }
        for arr in arrivals]

    return arrival_dicts


def get_all_positions():
    # We need : Lane primary key, bus name, remain_time, stop name, vehicle_no,
    positions = PosOfBus.objects.all().select_related('route_key')

    position_dicts = [
        {
            "pk": pos.route_key.id,
            "bus_name": pos.route_key.bus_name,
            "remain_time": None,
            "stop_name": None,
            "vehicle_no": pos.bus_num,
        }
        for pos in positions]

    return position_dicts


def build_response_dict():
    
    # parts = get_all_parts()

    rd ={
            #"parts": str(type(list(parts.values())[0])),
            "arrival": get_all_arrivals(),
            "position": get_all_positions(),
            "departure": {
                "tbi": "tbi",
            }
        }

    return rd
