from chroniccrawler.models import *


def get_lanes(alias):
    lanes = MapToAlias.objects.filter(alias_key=alias).select_related('lane_key')\
                              .values('lane_key', 'lane_key__bus_name')
    lanesdict = {}
    for l in lanes:
        lanesdict[l['lane_key']] = l['lane_key__bus_name']
    return lanesdict
    


def build_response_dict(alias):
    rd = {
        "lanes": get_lanes(alias),
    }

    return rd
