import logging
import asyncio
import xmltodict

import chroniccrawler.crawler.laneinfo as laneinfo
import chroniccrawler.crawler.timetable_usb as timetable

import chroniccrawler.crawler.tools.requestor as rq
import chroniccrawler.crawler.tools.listifier as ls

from chroniccrawler.models import DayInfo


logger = logging.getLogger('bushexa')


async def get_gather(l_u_ps, ul_u_ps):
    loop = asyncio.get_event_loop()
    l_task = loop.create_task(rq.get_all(l_u_ps, timeout=100))
    ul_task = loop.create_task(rq.get_all(ul_u_ps, timeout=100))
    logger.debug("Daily task created")

    l_texts = await l_task
    ul_texts = await ul_task

    return l_texts, ul_texts


def do_daily():
    lanes = laneinfo.get_all_lanes_to_request()
    usblanes = timetable.get_all_lanes_to_request()

    todayinfo = DayInfo.objects.first()
    logger.debug("Fetch from database done")

    l_u_ps = laneinfo.ready_request(lanes)
    ul_u_ps = timetable.ready_request(usblanes, todayinfo.kind)
    logger.debug("Format to request done")

    loop = asyncio.get_event_loop()
    l_texts, ul_texts = loop.run_until_complete(get_gather(l_u_ps, ul_u_ps))
    logger.debug("Request and response done")

    lane_rdicts = []
    ul_rdicts = []

    for lt in l_texts:
        if lt[1] is not None:
            d = xmltodict.parse(lt[1])
            lane_rdicts.append((lt[0], d))
    for lt in ul_texts:
        if lt[1] is not None:
            d = xmltodict.parse(lt[1])
            ul_rdicts.append((lt[0], d))
    logger.debug("Filtered out failed requests")

    for lr in lane_rdicts:
        info = ls.element_list(['response', 'body', 'totalCount'], lr[1],
                            ['response', 'body', 'items', 'item'])
        laneinfo.store_lane_info(lr[0], info)
    for lr in ul_rdicts:
        info = ls.element_list(['tableInfo', 'totalCnt'], lr[1], ['tableInfo', 'list', 'row'])
        timetable.store_time_table(lr[0], info)
    logger.debug("Lane node and timetable saved to db")
    return
