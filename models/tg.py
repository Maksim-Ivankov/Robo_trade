import sys
import os
sys.path.insert(1,os.path.join(sys.path[0],'../'))
from config import *
import requests


def print_tg(message):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TG_API)
    data = {
        'chat_id': TG_ID,
        'text': f'{message}'
    }
    requests.post(url, data=data)