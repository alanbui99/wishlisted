# Generated by Django 3.1.3 on 2021-01-17 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0006_item_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='first_scrape',
            field=models.BooleanField(default=False),
        ),
    ]
