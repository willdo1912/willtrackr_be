# Generated by Django 5.0.2 on 2024-03-03 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_customer_created_at_alter_quote_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 17, 38, 0, 286914, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='quote',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 17, 38, 0, 286914, tzinfo=datetime.timezone.utc)),
        ),
    ]
