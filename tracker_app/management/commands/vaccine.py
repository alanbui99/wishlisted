import time
import schedule
import random

import os
import json
import concurrent.futures

import requests
import smtplib
import concurrent.futures


from bs4 import BeautifulSoup
from faker import Faker
import re

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule.every().minute.at(":00").do(self.get_providenceri_links)
        schedule.every().minute.at(":30").do(self.get_vaccinateri_pages)  
        while True:
            schedule.run_pending()
            time.sleep(1)  

    def get_vaccinateri_pages(self):
        print('attempting vaccinateri')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.get_vaccinateri_links, [i for i in range(1, 5)])


    def get_vaccinateri_links(self, page):
        try:
            urls = []
            page = requests.get('https://www.vaccinateri.org/clinic/search?page={page}'.format(page=page))
            soup = BeautifulSoup(page.content, 'lxml')
            buttons = soup.find_all('a', attrs={'class': 'button-primary px-4'})

            for button in buttons:
                path = button['href']
                urls.append('https://www.vaccinateri.org/' + path)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.scrape_clinic, urls)

        except Exception as e:
            print(str(e))
            rest_time = random.choice([1, 2, 4, 8, 16, 32])
            time.sleep(rest_time)
            self.get_vaccinateri_links()    

    def get_providenceri_links(self):
        print('attempting providenceri')
        try:
            urls = []

            page = requests.get('https://www.providenceri.gov/vaccinate/', headers=self.get_header())
            soup = BeautifulSoup(page.content, 'lxml') 

            h4s = soup.body.find_all('h4')

            for h4 in h4s:
                text = h4.get_text()
                if 'Registration Link:' in text:
                    url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
                    urls.append(url)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.scrape_clinic, urls)


        except Exception as e:
            print(str(e))
            rest_time = random.choice([1, 2, 4, 8, 16, 32])
            time.sleep(rest_time)
            self.get_providenceri_links()

    def scrape_clinic(self, url):
        try:
            url = 'https://www.vaccinateri.org//reg/0767251996'
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'lxml')

                trs = soup.findAll('tr')

                for tr in trs:
                    # status = None
                    span = tr.find('span')
                    p = tr.find('p')

                    if p:
                        status = p.get_text().strip().replace('\n', '').replace(' ', '')
                        if status != 'Noappointmentsavailable' and status != 'Someonewillcontactyouaboutyourappointment.' :
                            time = span.get_text()
                            self.email(url, time)

        except Exception as e:
            print(str(e))
            rest_time = random.choice([1, 2, 4, 8, 16, 32])
            time.sleep(rest_time)
            self.scrape_clinic(url)
    

    
    def get_header(self):
        fake = Faker()
        return {
            "User-Agent": fake.user_agent(), 
            "Accept-Encoding":"gzip, deflate, br", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9", 
            "Pragma": "no-cache",
            "DNT":"1",
            "Connection":"close", 
            "Upgrade-Insecure-Requests":"1"
        }


    def email(self, url, time):
        try:
            server = smtplib.SMTP(host='smtp.gmail.com', port=587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            sender_email = 'abui.projects@gmail.com'
            app_password = 'Disboyfc@projects'

            server.login(sender_email, app_password)


            subject = 'VACCINE SLOT AVAILABLE'

            body = f"{url}, {time}"

            msg = f"Subject: {subject}\n\n {body}"

            server.sendmail(sender_email, 'tbui1@friars.providence.edu', msg)

            print('HEY EMAIL HAS BEEN SENT!')


            server.quit()

        except Exception as e:
            print(str(e))
            rest_time = random.choice([1, 2, 4, 8, 16, 32])
            print('email resting...', rest_time)
            time.sleep(rest_time)
