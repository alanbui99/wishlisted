import uuid
import time

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from ..utils.scrapers.amazon_scraper import AmazonScraper
from ..utils.email_handler import send_notify_mail

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=300, null=True)
    notify_when = models.CharField(
        max_length=50,
        choices=(
            ("below", "Below certain price"),
            ("down", "Goes down"),
            ("change", "Changes"),
            ("no", "Do not notify")
        )
    )
    desired_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    init_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    landing_image = models.URLField(max_length=500, null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    unsubscribed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #for url constructing purpose
        unique_together = (
            'user',
            'date_registered',
        )

    def __str__(self):
        return str(self.title)

    @staticmethod
    def register(form_data):
        #check new user or return user
        email_input = form_data.get('email')
        if User.objects.filter(username=email_input).exists():
            user = User.objects.filter(username=email_input).first()
        else:
            user = User.objects.create_user(email_input)
            
        #initialize new_item
        new_item = Item (
            url=form_data.get('url'),
            notify_when=form_data.get('notify_when'),
            desired_price=form_data.get('desired_price'),
            user=user
        )

        #scrape
        start_time=time.time()
        scrape_payload = None
        #retry until success or timeout
        while scrape_payload is None and time.time() - start_time < 20:
            scraper = AmazonScraper(new_item)
            scrape_payload = scraper.do_scrape(start_time)
        if not scrape_payload: return

        #add more fields and save
        new_item.title = scrape_payload.get('title')
        new_item.init_price = scrape_payload.get('current_price')
        new_item.landing_image = scrape_payload.get('landing_image')
        new_item.save()

        #send notification email if current price is already below desired price
        if new_item.notify_when == 'below' and float(new_item.init_price) < float(new_item.desired_price):
            try:
                send_notify_mail(new_item, scrape_payload)
            except Exception as e:
                print(str(e))


        #create scrape record
        new_item.record_scrape(scrape_payload, True)

        return new_item.id
    
    def record_scrape(self, scrape_payload, is_first_time = False):
        self.record_set.create(
            price=scrape_payload.get('current_price'), 
            emailed=scrape_payload.get('emailed'),
            first_scrape = is_first_time,
            exec_time=scrape_payload.get('exec_time')
        )

    @staticmethod
    def unsubscribe(item_id):
        item = Item.objects.filter(id=item_id).first()
        if not item: return
        item.unsubscribed = True
        item.save()
        return item
    
    @staticmethod
    def get_items_by_email(email):
        user = User.objects.filter(username=email).first()
        items = Item.objects.filter(user=user)
        return items
        







