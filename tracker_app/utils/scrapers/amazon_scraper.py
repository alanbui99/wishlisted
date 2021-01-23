import time
import random
import os
import json
import concurrent.futures

import requests
from bs4 import BeautifulSoup
from faker import Faker

from ..proxies_scraper import get_proxies

fake = Faker()

class AmazonScraper:
    def __init__(self, item, user_agent=None):
        self.item = item
        self.user_agent = user_agent
        self.response = None

    def do_scrape(self):
        print('scraping...')
        start_time = time.time()
        proxylist = get_proxies()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.send_request, proxylist)
        
        payload = {'title': None, 'current_price': None, 'landing_image': None, 'emailed': False}
        soup = self.response
        if soup.find(id='productTitle') or soup.find('span', attrs={'class': 'qa-title-text'}):
            #for books
            if soup.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}): 
                self.get_book_payload(soup, payload)
            #for qa items(eg: iphone 12)
            elif soup.find('span', attrs={'class': 'qa-title-text'}):
                self.get_qa_payload(soup, payload)
            #for general items
            else: 
                self.get_item_payload(soup, payload)

            payload['exec_time'] = round(time.time() - start_time, 2)
            print(payload)
            return payload
    
    def send_request(self, proxy):
        if self.response: return
        headers = {
            "User-Agent": None, 
            "Accept-Encoding":"gzip, deflate, br", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9", 
            "Pragma": "no-cache",
            "DNT":"1",
            "Connection":"close", 
            "Upgrade-Insecure-Requests":"1"
        }

        user_agent = fake.user_agent()
        headers["User-Agent"] = user_agent

        try:
            page = requests.get(self.item.url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=0.5)
            print(page)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'lxml')                
                self.response = soup
                print('WORKING', proxy)
            
        except Exception as e:
            pass
                
    def get_item_payload(self, soup, payload):
        payload['title'] = soup.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()

        #possible ids of html tag with item price
        possible_ids = ['priceblock_ourprice', 'priceblock_saleprice', 'priceblock_dealprice', 'rentPrice'] 
        for id in possible_ids:
            try:
                # extract item price
                price_str = soup.find(id=id).get_text().strip()
                if price_str: break
            except Exception as e:
                continue
        
        payload['current_price'] = float(price_str[1:])
        payload['landing_image'] = soup.find(id= 'landingImage').get('data-old-hires').strip()

    def get_book_payload(self, soup, payload):
        payload['title'] = soup.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()

        try:
            price_str = soup.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}).get_text().strip()
        except Exception as e:
            print(str(e))
        
        payload['current_price'] = float(price_str[1:])

        valid_book_image_ids = ['imgBlkFront', 'ebooksImgBlkFront']
        for id in valid_book_image_ids:
            try:
                payload['landing_image'] = soup.find(id=id).get('src').strip()
                if payload['landing_image']: break
            except Exception as e:
                print(str(e))
                continue

    def get_qa_payload(self, soup, payload):
        payload['title'] = soup.find('span', attrs={'class': 'qa-title-text'}).get_text().strip().encode('ascii', 'replace').decode()
        try:
            price_str = soup.find('span', attrs={'class': 'qa-price-block-our-price'}).get_text().strip()
        except Exception as e:
            print(str(e))
        
        payload['current_price'] = float(price_str[1:])
        try:
            payload['landing_image'] = soup.find('img', attrs={'class': 'mainImage'}).get('src').strip()
        except Exception as e:
            print(str(e))