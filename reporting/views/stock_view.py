import json

from django.db import transaction
from django.http import request
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, viewsets, mixins, permissions, exceptions
from rest_framework.response import Response
from rest_framework.settings import api_settings

from reporting.models.stock import StockSerializer, Stocks
from reporting.models.helpers.has_permission import has_permission
from reporting.models.requests.query_params import QueryParams
from reporting.service.stock_service import StockService



class StockView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    stock_service = StockService()
    serializer_class = StockSerializer

    @extend_schema(
        operation_id="Stock - Create",
        tags=["Stock"],
        request={"application/json": StockSerializer},
        responses={
            201: OpenApiResponse(response=StockSerializer, description="Success."),
            400: OpenApiResponse(description="Client specified an invalid argument or missing argument."),
        },
    )
    @transaction.atomic
    @has_permission("stocks.instances.create")
    def create(self, request, *args, **kwargs):
        if "id" in request.data:
            return Response(
                status=400, data={"error_code": "property_not_allowed", "message": "You are not allowed to set code."}
            )
        request.data["user"] = request.user.id
        data = self.stock_service.insert(request.data)
        return Response(status=201, data=data)

    @extend_schema(
        operation_id="Stock - Update",
        tags=["Stock"],
        request={"application/json": StockSerializer},
        responses={
            204: OpenApiResponse(response=None, description="Success."),
            404: OpenApiResponse(description="A specified resource is not found."),
        },
    )
    @transaction.atomic
    # @has_permission("stocks.instances.update")
    def update(self, request, *args, **kwargs):
        self.stock_service.update(kwargs["id"], user=request.user.id, role=request.user.roles, data=request.data)
        return Response(status=204)

    # @has_permission("stocks.instances.get")
    @extend_schema(
        operation_id="Stock - Get",
        tags=["Stock"],
        responses={
            200: OpenApiResponse(response=StockSerializer, description="Success."),
            400: OpenApiResponse(description="Client specified an invalid argument or missing argument."),
            404: OpenApiResponse(description="A specified resource is not found."),
        },
    )
    def get(self, request, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            raise ValueError("id param is missing")
        stock = self.stock_service.get(id=kwargs["id"])
        return Response(StockSerializer(stock).data)

    @has_permission("stocks.instances.list")
    @extend_schema(
        operation_id="Stock - List",
        tags=["Stock"],
        responses={
            200: OpenApiResponse(response=StockSerializer, description="Success."),
        },
    )
    @method_decorator(cache_page(1 * 60))
    def list(self, request):
        stocks = self.stock_service.list()
        return Response({"result": StockSerializer(stocks, many=True).data})

    # @has_permission("stocks.instances.delete")
    @extend_schema(
        operation_id="Stocks - DELETE",
        tags=["Stocks"],
        responses={
            204: OpenApiResponse(response=None, description="Success."),
            401: OpenApiResponse( description="Unauthorized."),
        },
    )
    def delete(self, request, **kwargs):
        if "id" not in kwargs or kwargs["id"] is None:
            raise ValueError("id param is missing")
        
        stock = self.stock_service.delete(kwargs["id"], user=request.user.id, role=request.user.roles)
        if Stocks.objects.filter(id=kwargs["id"]).exists():
            return Response(status=401)
        else:
            return Response(status=204)

   