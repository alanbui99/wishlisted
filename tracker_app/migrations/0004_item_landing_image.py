# Generated by Django 3.1.3 on 2021-01-15 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0003_auto_20210114_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='landing_image',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
