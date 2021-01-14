from django.contrib import admin
from .models.item import Item
from .models.record import Record

admin.site.register(Item)
admin.site.register(Record)