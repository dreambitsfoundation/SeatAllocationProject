# Generated by Django 3.2.12 on 2022-03-08 10:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_studentbatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='allocated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentbatch',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 3, 8, 10, 2, 0, 649388, tzinfo=utc)),
            preserve_default=False,
        ),
    ]