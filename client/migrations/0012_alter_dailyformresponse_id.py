# Generated by Django 5.0.2 on 2024-03-04 12:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_dailyformresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyformresponse',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False),
        ),
    ]
