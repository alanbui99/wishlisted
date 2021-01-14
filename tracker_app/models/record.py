from django.db import models
from django.utils import timezone
from .item import Item

class Record(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    emailed = models.BooleanField()
    
    class Meta:
        unique_together = ['item', 'timeStamp']
    
    def __str__(self):
        return str(self.item.id)