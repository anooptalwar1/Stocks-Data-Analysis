from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.settings import api_settings

from reporting.models.helpers.has_permission import has_permission
from reporting.models.user import UserSerializer, User
from reporting.service.user_service import UserService


class UserView(viewsets.GenericViewSet):
    user_service = UserService()
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        operation_id="User - Create",
        tags=["User"],
        request={"application/json": UserSerializer},
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Success."),
            400: OpenApiResponse(description="Client specified an invalid argument or missing argument."),
            404: OpenApiResponse(description="A specified resource is not found."),
        },
        auth=["users.instances.create"],
    )
    @transaction.atomic
    @has_permission("users.instances.create")
    def create(self, request, **kwargs):
        site = self.user_service.insert(request.data)
        return Response(status=201, data=UserSerializer(site).data)

    @extend_schema(
        operation_id="User - Me",
        tags=["User"],
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Success."),
            401: OpenApiResponse(description="Request not authenticated due to missing, invalid, authentication info."),
        },
    )
    def me(self, request, **kwargs):
        return Response(UserSerializer(request.user).data)

    @extend_schema(
        operation_id="User - List",
        tags=["User"],
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Success."),
            401: OpenApiResponse(description="Request not authenticated due to missing, invalid, authentication info."),
        },
        auth=["users.instances.list"],
    )
    @has_permission("users.instances.list")
    def list(self, request, **kwargs):
        if request.query_params.get("service_account", False):
            return Response(
                {
                    "result": UserSerializer(
                        User.objects.all().filter(active=True).filter(service_account=True), many=True
                    ).data
                }
            )

        search = request.query_params.get("search", None)
        sort = request.query_params.get("order", None)
        limit = int(request.query_params.get("limit", api_settings.PAGE_SIZE))
        offset = int(request.query_params.get("offset", 0))
        include_inactive = request.query_params.get("include_inactive", False)

        users = self.user_service.list(search, include_inactive, sort, limit, offset)
        return Response(data={"results": UserSerializer(users, many=True).data})

    @extend_schema(
        operation_id="User - Update",
        tags=["User"],
        request={"application/json": UserSerializer},
        responses={
            204: OpenApiResponse(response=None, description="Success."),
            404: OpenApiResponse(description="A specified resource is not found."),
        },
        auth=["users.instances.update"],
    )
    @transaction.atomic
    @has_permission("users.instances.update")
    def update(self, request, **kwargs):
        request.data["id"] = int(kwargs["user_id"])

        self.user_service.update(user_id=kwargs["user_id"], data=request.data)

        # TODO: Ensure user has delete permission
        if not request.data["active"]:
            return Response(
                {"message": "User is deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=204)

    @extend_schema(
        operation_id="User - Delete",
        tags=["User"],
        responses={
            204: OpenApiResponse(response=None, description="Success."),
            404: OpenApiResponse(description="A specified resource is not found."),
        },
        auth=["users.instances.delete"],
    )
    @transaction.atomic
    @has_permission("users.instances.delete")
    def delete(self, request, **kwargs):
        user_id = int(kwargs["user_id"])

        exists = self.user_service.exists(user_id)

        if not exists:
            raise exceptions.NotFound(f"User not found for '{user_id}'.")

        self.user_service.delete(user_id)
        return Response(status=204)

