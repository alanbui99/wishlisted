import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from ..scraper import scrape

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
        new_item = Item.objects.create(
            url=form_data.get('url'),
            notify_when=form_data.get('notify_when'),
            desired_price=form_data.get('desired_price'),
            user=user
        )

        #scrape
        scrape_payload = scrape(new_item, first_time=True)
        if not scrape_payload: return

        #add more fields and save
        new_item.title = scrape_payload.get('item')
        new_item.init_price = scrape_payload.get('current_price')
        new_item.landing_image = scrape_payload.get('landing_image')
        new_item.save()

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
        





