from rest_framework import viewsets, mixins, permissions
from rest_framework.settings import api_settings

from reporting.models.helpers.has_permission import has_permission
from reporting.models.role import RoleSerializer, Role


class RoleView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    search_fields = ["name"]

    @has_permission("roles.instances.list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
