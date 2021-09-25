import requests

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