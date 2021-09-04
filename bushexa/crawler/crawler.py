import requests
import xmltodict
import json

"""
Ulsan API에게 정보를 요청하는 부분
Input
- stopid: 버스정류장 번호
Output
- 
"""
def request_API(stopid='196040122'):
    key_file = open('./key.txt', 'r')
    key = key_file.read()

    url = 'http://openapi.its.ulsan.kr/UlsanAPI/getBusArrivalInfo.xo'

    params = {'stopid': stopid,
            'pageNo': '1',
            'numOfRows': '10',
            'serviceKey': key}

    print(url)
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.text)
    xml = response.text

    return xml

def parse_xml(xml):
    js = xmltodict.parse(xml)
    info_dict = json.loads(json.dumps(js))['tableInfo']['list']['row']
    return info_dict


if __name__=='__main__':
    # xml = request_API()
    xml_file = open('./test.xml', 'r')
    xml = xml_file.read()
    d = parse_xml(xml)
    print(d[0])