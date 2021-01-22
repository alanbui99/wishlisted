import time
import random
import os

import requests
from bs4 import BeautifulSoup
from faker import Faker

fake = Faker()

class AmazonScraper:
    def __init__(self, item):
        self.item = item

    def do_scrape(self):
        start_time = time.time()
        print('Checking price...')
        payload = {}

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

        while True:
            if time.time() - start_time > 15: return 
            try:
                user_agent = fake.user_agent()
                print(user_agent)
                headers["User-Agent"] = user_agent
                page = requests.get(self.item.url, headers = headers)
                soup = BeautifulSoup(page.content, 'lxml')

                if soup.find(id = "productTitle"):
                    #for books
                    if soup.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}): 
                        payload = self.get_book_details(soup)
                    #for general items
                    else: 
                        payload = self.get_item_details(soup)

                    payload['exec_time'] = round(time.time() - start_time, 2)
                    print(payload)
                    return payload
                
            except Exception as e: 
                # delay (to avoid getting blocked), then try with the next user agent
                print(str(e))
                rest_time = random.choice([1,2,4,6])
                print('resting...', rest_time) 
                time.sleep(rest_time)    

    def get_item_details(self, soup):
        title = soup.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()
        valid_ids = ['priceblock_ourprice','priceblock_saleprice','priceblock_dealprice','rentPrice'] #possible ids of html tag with item price
        for id in valid_ids:
            try:
                # extract item price
                price_str = soup.find(id=id).get_text().strip()
                if price_str: break
            except Exception as e:
                continue

        current_price = float(price_str[1:])
        landing_image = soup.find(id= 'landingImage').get('data-old-hires').strip()

        details = {'item': title, 'current_price': current_price, 'landing_image': landing_image, 'emailed': False}
        return details

    def get_book_details(self, soup):
        title = soup.find(id = 'productTitle').get_text().strip().encode('ascii', 'replace').decode()

        try:
            price_str = soup.find('span', attrs={'class': 'a-size-base a-color-price a-color-price'}).get_text().strip()
        except Exception as e:
            print(str(e))
        
        current_price = float(price_str[1:])

        valid_book_image_ids = ['imgBlkFront', 'ebooksImgBlkFront']
        for id in valid_book_image_ids:
            try:
                landing_image = soup.find(id=id).get('src').strip()
                if landing_image: break
            except Exception as e:
                print(str(e))
                continue

        details = {'item': title, 'current_price': current_price, 'landing_image': landing_image, 'emailed': False}
        return details

    # def send_mail(item, details):
    #     while not details.get('emailed'):
    #         try:
    #             server = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
    #             server.ehlo()
    #             server.starttls()
    #             server.ehlo()

    #             # sender_email = os.environ['EMAIL_SENDER']
    #             # app_password = os.environ['EMAIL_PASSWORD']
    #             sender_email = 'abui.projects@gmail.com'
    #             app_password = 'Disboyfc@projects'
                
    #             server.login(sender_email, app_password)

    #             subject_start = 'Price change for ' if item.notify_when == 'change' else 'Lower price for '

    #             subject = subject_start + details.get('item')
    #             nl = '\n'
    #             body = f"Price for the product is now ${details.get('current_price')}.{nl} Check the Amazon link: {item.url}"

    #             msg = f"Subject: {subject}\n\n {body}"

    #             server.sendmail(sender_email, item.user.username, msg)

    #             print('HEY EMAIL HAS BEEN SENT!')

    #             details['emailed'] = True

    #             server.quit()
            
    #         except Exception as e:
    #             print(str(e))
    #             rest_time = random.choice([1,2,4,8,16,32])
    #             print('email resting...', rest_time) 
    #             time.sleep(rest_time)