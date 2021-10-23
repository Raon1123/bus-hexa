import requests
import xmltodict


# Returns the response converted into a dictionary
def request_dict(url, params):
    r = requests.get(url, params=params)
    
    if r.status_code != 200:
        raise Exception("Abnormal response : " + str(r.status_code))

    # print(r.status_code)
    # print(r.text)

    d = xmltodict.parse(r.text)
    return d
