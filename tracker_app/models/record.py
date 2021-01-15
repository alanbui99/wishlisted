from itertools import groupby

from django.db import models
from django.utils import timezone
from .item import Item

class Record(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    emailed = models.BooleanField(default=False)
    first_scrape = models.BooleanField(default=False)
    exec_time = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    failed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['item', 'time_stamp']

    def __str__(self):
        return str(self.item.title)

    @staticmethod
    def get_item_chart_data(item):
        records = Record.objects.filter(item=item).order_by('time_stamp')
        dates = []
        prices = []

        # group records by date
        for key, group in groupby(records, key= lambda x: x.time_stamp.date()):
            prices_of_date = [record.price for record in list(group) if record.price]
            if not prices_of_date: continue
            dates.append(key.strftime('%b %d'))
            # only take lowest price in the day
            prices.append(str(min(prices_of_date)))

        # filter out insignificant records
        indices_to_remove = [i for i, price in enumerate(prices) if i != 0 and i != len(prices)-1 and price == prices[i-1] == prices[i+1]]
        prices = [price for i, price in enumerate(prices) if i not in indices_to_remove]
        dates = [date for i, date in enumerate(dates) if i not in indices_to_remove]
        return (dates, prices)