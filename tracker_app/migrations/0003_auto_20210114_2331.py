# Generated by Django 3.1.3 on 2021-01-15 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0002_auto_20210114_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='notify_when',
            field=models.CharField(choices=[('below', 'Below certain price'), ('down', 'Goes down'), ('change', 'Changes'), ('no', 'Do not notify')], max_length=50),
        ),
    ]
