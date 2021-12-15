from django.db import models
import django.utils.timezone
from django_pandas.managers import DataFrameManager
from rest_framework import serializers
from reporting.models.helpers.foriegn_key_code_based import ForeignKeyCodeBased


class Stocks(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True)
    current_price = models.TextField(null=True)
    currency_id = models.TextField(null=True)
    last_update = models.DateTimeField(default=django.utils.timezone.now)
    is_active = models.BooleanField(default=True)
    quantity = models.TextField(null=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        db_column="user_id",
        db_index=True,
        null=False,
        )
    

    objects = DataFrameManager()

    class Meta:
        db_table = "stocks"

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ["id", "name", "current_price", "currency_id", "quantity", "user"]