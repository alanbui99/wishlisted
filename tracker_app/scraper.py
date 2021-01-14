import requests
from bs4 import BeautifulSoup
import smtplib
import time
import random
import os
from faker import Faker
fake = Faker()

def scrape(data, init=False):
    print('Checking price...')
    while True:
        try:
            user_agent = fake.user_agent()
            headers = {"User-Agent": user_agent}
            page = requests.get(data.url, headers = headers)
            soup = BeautifulSoup(page.content, 'lxml')

            if soup.find(id = "productTitle"):
                payload = get_price(soup)                
                if init:
                    #send notification email if current price drops below desired price
                    if data.notify_when == 'below' and payload.get('current_price') < data.desired_price:
                        try:
                            send_mail(data, payload)
                        except Exception as e:
                            print(str(e))
                return payload
        except Exception as e: 
            # delay (to avoid getting blocked), then try with the next user agent
            print(str(e))
            rest_time = random.choice([1,2,4,6])
            print('resting...', rest_time) 
            time.sleep(rest_time)
            
def get_price(soup):
        title = soup.find(id = "productTitle").get_text().strip().encode('ascii', 'replace').decode()
        print(title)
        valid_ids = ['priceblock_ourprice','priceblock_saleprice','priceblock_dealprice','rentPrice', ] #possible ids of html tag with item price
        for id in valid_ids:
            try:
                # extract item price
                price = soup.find(id=id).get_text()
            except Exception as e:
                continue
                
        current_price = float(price[1:])
        print('Current Price: $', current_price)

        details = {'item': title, 'current_price': current_price, 'emailed': False}
        return details

def send_mail(item, details):
    while not details['emailed']:
        try:
            server = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            # sender_email = os.environ['EMAIL_SENDER']
            # app_password = os.environ['EMAIL_PASSWORD']
            sender_email = 'abui.projects@gmail.com'
            app_password = 'Disboyfc@projects'
            
            server.login(sender_email, app_password)

            subject_start = 'Price change for ' if item.notify_when == 'change' else 'Lower price for '

            subject = subject_start + details.get('item')
            nl = '\n'
            body = f"Price for the product is now ${details.get('current_price')}.{nl} Check the Amazon link: {item.url}"

            msg = f"Subject: {subject}\n\n {body}"

            server.sendmail(sender_email, item.user.username, msg)

            print('HEY EMAIL HAS BEEN SENT!')

            details['emailed'] = True

            server.quit()
        
        except Exception as e:
            print(str(e))
            rest_time = random.choice([1,2,4,8,16,32])
            print('email resting...', rest_time) 
            time.sleep(rest_time)