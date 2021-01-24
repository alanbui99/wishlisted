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