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
    def get_significant_records(item):
        records = Record.objects.filter(item=item).order_by('time_stamp')
        lowest_records_per_date = []
        # group records by date & get record with lowest price in a date
        for key, group in groupby(records, key= lambda x: x.time_stamp.date()):
            records_of_date = list(group)
            if not records_of_date: continue

            lowest_price_record = None
            lowest_price = float('inf')

            for record in records_of_date:
                if record.price and record.price < lowest_price:
                    lowest_price_record = record
                    lowest_price = record.price
                    

            if lowest_price_record:
                lowest_records_per_date.append(lowest_price_record)

        # significant records are first/last records or are before/in a change
        significant_records = [record for i, record in enumerate(lowest_records_per_date) if i in [0, len(lowest_records_per_date) - 1] or not record.price == lowest_records_per_date[i-1].price == lowest_records_per_date[i+1].price]
        return significant_records