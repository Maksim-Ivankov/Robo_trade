import requests
from bs4 import BeautifulSoup as bs
import re
import time

# def get_free_proxies():
#     url = "https://free-proxy-list.net/"
#     soup = bs(requests.get(url).content, "html.parser")
#     data = str(soup.find('textarea').contents) 
#     data = data.split(r'\n')
#     del data[0]
#     del data[0]
#     del data[0]
#     del data[len(data)-1]
#     return data

# free_proxies = get_free_proxies()
# print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
# for i in range(len(free_proxies)):
#     print(f"{i+1}) {free_proxies[i]}")

# def get_session(proxies):
#     # создать HTTP‑сеанс
#     session = requests.Session()
#     session.proxies = {"http": proxies, "https": proxies}
#     return session


# for i in range(len(free_proxies)):
#     s = get_session(i)
#     try:
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
#     except Exception as e:
#         print('Ошибка')
#         continue

# try:
#     s = get_session('114.156.77.107:8080')
#     print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
# except:
#     print('Ошибка')


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    host = []
    for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            kod = tds[2].text.strip()
            country = tds[3].text.strip()
            anon = tds[4].text.strip()
            google = tds[5].text.strip()
            Https = tds[6].text.strip()
            time_ago = tds[7].text.strip()
            host = f"{ip}|{port}|{kod}|{country}|{anon}|{google}|{Https}|{time_ago}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies[2]
free_proxies = get_free_proxies()
print(free_proxies)
# print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
# for i in range(len(free_proxies)):
#     print(f"{i+1}) {free_proxies[i]}")

    