import requests
from bs4 import BeautifulSoup

def get_proxies():
    proxies = []
    url = 'https://www.us-proxy.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find(id='proxylisttable')
    rows = table.find_all('tr')
    for row in rows[1:-1]:
        cells = row.find_all('td')
        ip = cells[0].get_text().strip()
        port = cells[1].get_text().strip()
        proxy = ip + ':' + port
        # print(proxy,cells[7].get_text())
        proxies.append(proxy)
    return proxies