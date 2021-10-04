import requests
import os

def get_key():
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.txt')
    key_file = open(key_path, 'r')

    key_quote = key_file.read()
    key_unquote = requests.utils.unquote(key_quote)

    key_file.close()

    return key_unquote

