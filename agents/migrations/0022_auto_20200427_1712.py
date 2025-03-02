# Generated by Django 2.2.12 on 2020-04-27 11:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0021_auto_20200427_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(max_length=100)),
                ('platform', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=10)),
                ('paymentPlatform', models.CharField(max_length=200)),
                ('paymentEmail', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
                ('paymentDetails', models.TextField()),
                ('paymentNote', models.TextField()),
                ('afterPaymentNote', models.TextField()),
                ('afterPaymentBalance', models.CharField(max_length=10)),
                ('datecreation', models.DateField(auto_now_add=True)),
                ('duedate', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='netellersignup',
            name='VipStatusDate',
            field=models.DateField(default=datetime.datetime(2020, 4, 27, 17, 12, 37, 853361)),
        ),
    ]
