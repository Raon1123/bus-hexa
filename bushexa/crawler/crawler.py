import requests

key_file = open('./key.txt', 'r')
key = key_file.read()

url = 'http://openapi.its.ulsan.kr/UlsanAPI/AllRouteDetailInfo.xo'

params = {'stopid': '196040122',
          'pageNo': '1',
          'numOfRows': '10',
          'serviceKey': key}

response = requests.get(url, params=params)
print(response.status_code)
print(response.text)