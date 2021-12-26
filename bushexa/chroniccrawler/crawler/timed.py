import asyncio
import xmltodict

import chroniccrawler.crawler.buspos as buspos
import chroniccrawler.crawler.arrivalinfo as arrival

import chroniccrawler.crawler.tools.requestor as rq
import chroniccrawler.crawler.tools.listifier as ls

async def getreallyall(l_u_ps, n_u_ps):
    loop = asyncio.get_event_loop()
    l_tasks = [loop.create_task(rq.getit(l_u_p)) for l_u_p in l_u_ps]
    n_tasks = [loop.create_task(rq.getit(n_u_p)) for n_u_p in n_u_ps]

    l_resps = await asyncio.gather(*l_tasks)
    n_resps = await asyncio.gather(*n_tasks)

    return l_resps, n_resps

def do_timed():
    lanes = buspos.get_all_lanes_to_request()
    nodes = arrival.get_all_nodes_to_request()

    l_u_ps = buspos.ready_request(lanes)
    n_u_ps = arrival.ready_request(nodes)

    loop = asyncio.get_event_loop()
    l_resps, n_resps = loop.run_until_complete(getreallyall(l_u_ps, n_u_ps))

    l_rdicts = []
    n_rdicts = []

    for l_r in l_resps:
        d = xmltodict.parse(l_r[1])
        l_rdicts.append((l_r[0], d))
    for n_r in n_resps:
        d = xmltodict.parse(n_r[1])
        n_rdicts.append((n_r[0], d))

    for lr in l_rdicts:
        info = ls.element_list(['response', 'body', 'totalCount'], lr[1],
                               ['response', 'body', 'items', 'item'])
        buspos.store_bus_pos(lr[0], info)
    for nr in n_rdicts:
        info = ls.element_list(['tableInfo', 'totalCnt'], nr[1],
                               ['tableInfo', 'list', 'row'])
        arrival.store_arrival_info(nr[0], info)
