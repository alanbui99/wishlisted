# Generated by Django 3.1.3 on 2021-01-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0004_item_landing_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='timeStamp',
            new_name='time_stamp',
        ),
        migrations.AddField(
            model_name='record',
            name='exec_time',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('item', 'time_stamp')},
        ),
    ]