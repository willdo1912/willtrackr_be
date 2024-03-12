from django.db import models
from rest_framework import serializers
from .models import DailyFormResponse, Quote, Customer, TypeformResponse


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "comment",
            "term",
            "created_at",
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "email", "password", "created_at")


class TypeformResponseSerializer(serializers.ModelSerializer):
    response_id = serializers.CharField(source="id", max_length=255)

    class Meta:
        model = TypeformResponse
        fields = ("response_id", "form_id", "customer", "created_at")


class DailyFormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyFormResponse
        fields = ("id", "customer", "start_at", "submit_at")
