# Generated by Django 2.2.12 on 2020-05-06 22:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0027_auto_20200507_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='allagentscommission',
            name='RevShareAgent',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='allagentscommission',
            name='RevShareCB',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='allagentscommission',
            name='activationDate',
            field=models.DateField(default=datetime.datetime(2020, 5, 7, 4, 16, 19, 651642)),
        ),
        migrations.AlterField(
            model_name='netellersignup',
            name='VipStatusDate',
            field=models.DateField(default=datetime.datetime(2020, 5, 7, 4, 16, 19, 651642)),
        ),
    ]
