# Generated by Django 2.2.12 on 2020-04-28 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0022_auto_20200427_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='allagentscommission',
            name='activationDate',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 4, 3, 24, 736634)),
        ),
        migrations.AlterField(
            model_name='netellersignup',
            name='VipStatusDate',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 4, 3, 24, 736634)),
        ),
        migrations.AlterField(
            model_name='paymentrequests',
            name='duedate',
            field=models.DateField(),
        ),
    ]
