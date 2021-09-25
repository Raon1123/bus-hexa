import requests
import xmltodict
import json

"""
API key를 읽는 함수

Input
- path: API key의 위치, 기본은 bushexa/crawler/key.txt

Output
- key: API key

"""
def get_key(path='./key.txt'):
    key_file = open(path, 'r')

    key = key_file.read()
    key = requests.utils.unquote(key)

    key_file.close()

    return key


"""
울산 버스 API로 부터 받은 json 파일 파싱
Input
- xml: API로 부터 받은 xml 파일

Output
- cnt: 조회된 총 timetable의 개수
- info_dict: 각 row를 dictonary를 가진 list 형태로 파싱

"""
def parse_xml(xml):
    # JSON parser
    js = xmltodict.parse(xml)
    js_dict = json.loads(json.dumps(js))

    # Get parsed contents
    cnt = int(js_dict['tableInfo']['totalCnt'])
    info_dict = js_dict['tableInfo']['list']['row']

    return cnt, info_dict