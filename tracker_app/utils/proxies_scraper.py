import requests
from bs4 import BeautifulSoup

def get_proxies():
    proxies = []
    url = 'https://www.us-proxy.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    rows = table.find_all('tr')
    for row in rows[1:-1]:
        cells = row.find_all('td')
        ip = cells[0].get_text().strip()
        port = cells[1].get_text().strip()
        proxy = 'https://' + ip + ':' + port
        proxies.append(proxy)
    return proxies