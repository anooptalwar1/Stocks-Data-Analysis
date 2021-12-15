import pandas as pd
from django.http import Http404
from django.db import transaction
from reporting.models import stock
from reporting.models.stock import Stocks
from reporting.models.stock import StockSerializer



class StockService:

    def insert(self, data):
        serializer = StockSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data


    def update(self, id: int, user, role, data):
        with transaction.atomic():
            if 'admin' in role:
                stock = Stocks.objects.get(id=id)
            else:
                stock = Stocks.objects.get(id=id, user=user)
                if stock is None:
                    return
            if "name" in data:
                stock.name=data["name"]
            if "current_price" in data:
                stock.current_price=data["current_price"]
            if "currency_id" in data:
                stock.currency_id=data["currency_id"]
            if "is_active" in data:
                stock.is_active=data["is_active"]
            if "quantity" in data:
                stock.quantity=data["quantity"]
            stock.save()
        

    def get(self, id) -> dict:
        result = Stocks.objects.get(id=id)
        if result is None or (len(result) == 0 if type(result) == dict else False):
            raise Http404(f"Stock not found for '{id}'")
        return result

    def list(self):
        return Stocks.objects.all()


    def delete(self, id: int, user, role):
        if 'admin' in role:
            Stocks.objects.get(id=id).delete()
        else:
            try:
                Stocks.objects.get(id=id, user=user).delete()
            except Exception as e:
                return e

