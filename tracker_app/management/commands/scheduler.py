import time
import schedule
from django.core.management.base import BaseCommand
from tracker_app.models import Item
from tracker_app.scraper import scrape, send_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(self.run_scraper)
        schedule.every().day.at("06:00").do(self.run_scraper)
        schedule.every().day.at("12:00").do(self.run_scraper)
        schedule.every().day.at("18:00").do(self.run_scraper)
        while True:
            schedule.run_pending()
            time.sleep(1)
            # run every 3 hour
            
    
    def run_scraper(self):
        print('scraping...')
        try:
            all_items = Item.objects.all()
            if len(all_items) > 0:
                for item in all_items:
                    payload = self.track_and_email(item)
                    self.record(item, payload)
            else:
                print('no item to track')
        except Exception as e: 
            print(str(e))

        print('sleeping...')

    def track_and_email(self, item):
        try:
            payload = scrape(item)
                    
            if item.notify_when == 'below' and payload.get('current_price') < item.desired_price:
                send_mail(item, payload)

            elif item.notify_when == 'down' and payload.get('current_price') < item.init_price:
                send_mail(item, payload)
            
            elif item.notify_when == 'change' and payload.get('current_price') != item.init_price:
                send_mail(item, payload)

            return payload

        except Exception as e: 
            print(str(e))

    def record(self, item, payload):
        try:
            item.record_set.create(price=payload.get('current_price'), emailed = payload.get('emailed'))
        except Exception as e: 
            print(str(e))

