# Generated by Django 5.0.2 on 2024-03-03 21:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_alter_customer_email_typeformresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeformresponse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]