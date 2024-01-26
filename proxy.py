import requests
import random
from bs4 import BeautifulSoup as bs
import re
import time

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, "html.parser")
    data = str(soup.find('textarea').contents) 
    data = data.split(r'\n')
    del data[0]
    del data[0]
    del data[0]
    del data[len(data)-1]
    return data

free_proxies = get_free_proxies()
# print(free_proxies)
# print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
# for i in range(len(free_proxies)):
#     print(f"{i+1}) {free_proxies[i]}")

def get_session(proxies):
    # создать HTTP‑сеанс
    session = requests.Session()
    session.proxies = {"http": proxies, "https": proxies}
    return session


# for i in range(len(free_proxies)):
#     s = get_session(i)
#     try:
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
#     except Exception as e:
#         print('Ошибка')
#         continue


s = get_session('139.162.78.109')
print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())



    