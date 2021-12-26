import requests
import xmltodict
import asyncio
import aiohttp


# Async task for getting response from thing_url_params and session
async def getit(t_u_p):
    async with aiohttp.request('GET', t_u_p[1], params=t_u_p[2]) as response:
        text = await response.text()
    if response.status != 200:
        raise Exception("Status not ok...")
    return (t_u_p[0], text)

# Get all
async def getall(t_u_ps):
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(getit(t_u_p)) for t_u_p in t_u_ps]
    thing_responses = await asyncio.gather(*tasks)

    return thing_responses

# Returns the response converted into a dictionary
def request_dicts(t_u_ps):
    loop = asyncio.get_event_loop()
    thing_texts = loop.run_until_complete(getall(t_u_ps))

    thing_rdicts = []

    for t_r in thing_texts:
        d = xmltodict.parse(t_r[1])
        thing_rdicts.append((t_r[0], d))

    return thing_rdicts


# OLD:Returns the response converted into a dictionary
# Old school synchronous function
def request_dict(url, params):
    r = requests.get(url, params=params)
    
    if r.status_code != 200:
        raise Exception("Abnormal response : " + str(r.status_code))

    # print(r.status_code)
    # print(r.text)

    d = xmltodict.parse(r.text)
    return d
