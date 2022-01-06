import datetime


def build_hour_select_list():
    return [(str(a), str(a)) for a in range(24)]


def build_minute_select_list():
    return [(str(a), str(a)) for a in range(60)]
