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
    def __init__(self, item):
        self.item = item
        self.response = None

    def do_scrape(self, start_time):
        try:
            print('scraping item...')
            #get a list from free proxies
            proxylist = get_proxies()

            #use multi-threading to try proxies until some work
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.send_request, proxylist)
            
            payload = {'title': None, 'current_price': None, 'landing_image': None, 'emailed': False}
            if self.response.find(id='productTitle') or self.response.find('span', attrs={'class': 'qa-title-text'}):
                #for books
                if self.response.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}): 
                    self.get_book_payload(payload)
                #for qa items(eg: iphone 12)
                elif self.response.find('span', attrs={'class': 'qa-title-text'}):
                    self.get_qa_payload(payload)
                #for general items
                else: 
                    self.get_item_payload(payload)

                payload['exec_time'] = round(time.time() - start_time, 2)
                print(payload)

                # abort if title or price not scraped
                if payload.get('title') is None or payload.get('current_price') is None: return
                
                return payload

        except Exception as e:
            print(str(e))

    def send_request(self, proxy):
        if self.response is not None:
            #stop trying out different proxies once response received
            return 
        
        headers = {
            "User-Agent": fake.user_agent(), 
            "Accept-Encoding":"gzip, deflate, br", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9", 
            "Pragma": "no-cache",
            "DNT":"1",
            "Connection":"close", 
            "Upgrade-Insecure-Requests":"1"
        }

        try:
            page = requests.get(self.item.url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=1)
            if page.status_code == 200:
                self.response = BeautifulSoup(page.content, 'lxml')                
                print('WORKING', proxy)
        except Exception as e:
            pass
                
    def get_item_payload(self, payload):
        try:
            payload['title'] = self.response.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()
            #possible ids of html tag with item price
            possible_ids = ['priceblock_ourprice', 'priceblock_saleprice', 'priceblock_dealprice', 'rentPrice'] 
            for id in possible_ids:
                try:
                    # extract item price
                    price_str = self.response.find(id=id).get_text().strip()
                    if price_str: break
                except Exception as e:
                    continue
            payload['current_price'] = float(price_str[1:].replace(',',''))
            try:
                payload['landing_image'] = self.response.find(id= 'landingImage').get('src').strip()
            except:
                print(str(e))

        except Exception as e:
            print(str(e))
            return

    def get_book_payload(self, payload):
        try:
            payload['title'] = self.response.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()
            price_str = self.response.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}).get_text().strip()
            payload['current_price'] = float(price_str[1:].replace(',',''))
            valid_book_image_ids = ['imgBlkFront', 'ebooksImgBlkFront']
            for id in valid_book_image_ids:
                try:
                    payload['landing_image'] = self.response.find(id=id).get('src').strip()
                    if payload.get('landing_image'): break
                except Exception as e:
                    print(str(e))
                    continue
        except Exception as e:
            print(str(e))
            return

    def get_qa_payload(self, payload):
        try:
            payload['title'] = self.response.find('span', attrs={'class': 'qa-title-text'}).get_text().strip().encode('ascii', 'replace').decode()
            price_str = self.response.find('span', attrs={'class': 'qa-price-block-our-price'}).get_text().strip()
            payload['current_price'] = float(price_str[1:].replace(',',''))
            try:
                payload['landing_image'] = self.response.find('img', attrs={'class': 'mainImage'}).get('src').strip()
            except Exception as e:
                print(str(e))
        except Exception as e:
            print(str(e))
            return