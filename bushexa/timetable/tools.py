"""
출발 시간을 예쁘게 표시하는 함수
예) 1100 => 11:00
"""
def pretty_time(timestr):
    if type(timestr) is not str:
        timestr = str(timestr)

    pretty = timestr[:2] + ':' + timestr[2:]

    return pretty


"""
잔여 시간을 예쁘게 표시하는 함수
예) 123 => 2분 후
"""
def pretty_remain(timestr):
    if type(timestr) is not str:
        timestr = str(timestr)

    timeint = int(timestr)

    remainmin = timeint // 60

    if remainmin > 0:
        ans = str(remainmin) + '분 후'
    else:
        ans = '1분 이내 도착'

    return ans