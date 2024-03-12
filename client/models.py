from django.db import models
from django.utils import timezone
from mongo_connection import db
import uuid

# TypeformAnswer model
typeform_answer_collection = db["typeform_answer"]

# DailyFormAnswer model
daily_form_answer_collecton = db["daily_form_answer"]

# BootsPerfumeProduct model
boots_perfume_product_collection = db["boots_perfume_product"]


# Create your models here.
class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=10)
    comment = models.TextField()
    term = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)


class TypeformResponse(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, db_constraint=False
    )
    form_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)


class DailyFormResponse(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, db_constraint=False
    )
    start_at = models.DateTimeField()
    submit_at = models.DateTimeField()

    def completed_today(self):
        return self.start_at.date() == timezone.now().date()
