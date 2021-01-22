import time
import schedule

from django.core.management.base import BaseCommand
from tracker_app.models import Item
from tracker_app.utils.scrapers.amazon_scraper import AmazonScraper
from tracker_app.utils.email_handler import send_notify_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(self.track_all)
        schedule.every().day.at("06:00").do(self.track_all)
        schedule.every().day.at("12:00").do(self.track_all)
        schedule.every().day.at("18:00").do(self.track_all)
        while True:
            schedule.run_pending()
            time.sleep(1)
            # run every 6 hour
            
    
    def track_all(self):
        print('scraping...')
        try:
            all_items = Item.objects.all()
            if len(all_items) > 0:
                for item in all_items:
                    payload = self.scrape_and_email(item)
                    self.record(item, payload)
            else:
                print('no item to track')
        except Exception as e: 
            print(str(e))

        print('sleeping...')

    def scrape_and_email(self, item):
        try:
            scraper = AmazonScraper(item)
            payload = scraper.do_scrape()
            
            if item.notify_when == 'below' and payload.get('current_price') < item.desired_price:
                send_notify_mail(item, payload)

            elif item.notify_when == 'down' and payload.get('current_price') < item.init_price:
                send_notify_mail(item, payload)
            
            elif item.notify_when == 'change' and payload.get('current_price') != item.init_price:
                send_notify_mail(item, payload)

            return payload

        except Exception as e: 
            print(str(e))

    def record(self, item, payload):
        try:
            item.record_set.create(
                price=payload.get('current_price'), 
                emailed = payload.get('emailed'),
                exec_time=payload.get('exec_time')
            )
        except Exception as e: 
            print(str(e))

