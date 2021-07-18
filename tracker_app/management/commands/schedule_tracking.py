import time
import concurrent.futures

from django.core.management.base import BaseCommand
from tracker_app.models import Item
from tracker_app.utils.scrapers.amazon_scraper import AmazonScraper
from tracker_app.utils.email_handler import send_notify_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.track_all()
    
    def track_all(self):
        print('scheduled_tracking...')
        try:
            all_items = Item.objects.filter(unsubscribed=False)
            if len(all_items) > 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.map(self.track_each, all_items)
            else:
                print('no item to track')
        except Exception as e: 
            print(str(e))

        print('sleeping...')

    def track_each(self, item):
        try:
            payload = self.scrape_and_email(item)
            self.record(item, payload)
        except Exception as e:
            print(str(e))

    def scrape_and_email(self, item):
        try:
            #scrape
            start_time=time.time()
            payload = None
            #retry until success or timeout
            while payload is None and time.time() - start_time < 30:
                scraper = AmazonScraper(item)
                payload = scraper.do_scrape(start_time)
            if not payload: return
            
            if item.notify_when == 'below' and float(payload.get('current_price')) < float(item.desired_price):
                send_notify_mail(item, payload)

            elif item.notify_when == 'down' and float(payload.get('current_price')) < float(item.init_price):
                send_notify_mail(item, payload)
            
            elif item.notify_when == 'change' and float(payload.get('current_price')) != float(item.init_price):
                send_notify_mail(item, payload)

            return payload

        except Exception as e: 
            print(str(e))

    def record(self, item, payload):
        try:
            if not payload: 
                item.record_set.create(failed=True)
                return

            item.record_set.create(
                price=payload.get('current_price'), 
                emailed = payload.get('emailed'),
                exec_time=payload.get('exec_time')
            )
        except Exception as e: 
            print(str(e))

