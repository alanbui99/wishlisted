# Generated by Django 3.1.3 on 2021-01-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]