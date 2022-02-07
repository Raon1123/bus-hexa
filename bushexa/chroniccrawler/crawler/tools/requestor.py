import asyncio
import aiohttp
import logging
import xmltodict
import requests


logger = logging.getLogger('bushexa')


# One request async function : get t_u_p as input, return thing_response pair as output
# If failed, return (t_u_p, None)
async def get_one(t_u_p):
    try:
        async with aiohttp.request('GET', t_u_p[1], params=t_u_p[2]) as response:
            text = await response.text()
            stat = response.status
        if stat == 200:
            logger.debug("Succeeded response from " + str(response.real_url))
            return (t_u_p[0], text)
        else:
            return (t_u_p, None)
    except asyncio.CancelledError:
        logger.info("Cancelled " + str(t_u_p))
        return (t_u_p, None)

# Manager Async function : get t_u_p iterable as input, return thing_response pair list as output
# Wait for 'timeout' seconds and then cancel remaining tasks
async def get_all(t_u_ps, timeout = 9):
    loop = asyncio.get_event_loop()

    logger.debug("Start requests")
    timer = loop.create_task(asyncio.sleep(timeout))
    tasks = [loop.create_task(get_one(t_u_p)) for t_u_p in t_u_ps]
    task_timer_pair = [asyncio.gather(*tasks), timer]

    await asyncio.wait(task_timer_pair, return_when=asyncio.FIRST_COMPLETED)

    timer.cancel()
    for t in tasks:
        t.cancel()
    logger.debug("Requests done")

    return await asyncio.gather(*tasks)


# Get thing_url_parameter iterable as input, return thing_dictionary pair list as output
# timeout after 'timeout' seconds, retry 'retry' times
def request_dicts(t_u_ps, timeout = 8, retry = 0):
    loop = asyncio.get_event_loop()

    thing_texts = loop.run_until_complete(get_all(t_u_ps, timeout))

    loop.close()

    return [(t_t[0], xmltodict.parse(t_t[1])) for t_t in thing_texts if t_t[1] is not None]

