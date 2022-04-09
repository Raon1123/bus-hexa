from chroniccrawler.models import *


def build_response_dict():
    rd = {}

    lanes = LaneToTrack.objects.all()

    for lane in lanes:
        name = lane.bus_name.split('(')[0]
        if rd.get(name):
            rd[name][lane.id] = lane.bus_name
        else:
            rd[name] = {lane.id : lane.bus_name}
    
    return rd
