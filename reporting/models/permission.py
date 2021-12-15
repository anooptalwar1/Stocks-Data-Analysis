from django.db import models
from django.utils import timezone
from rest_framework import serializers

from reporting.models.role import RoleSerializer


class Permission(models.Model):
    code = models.TextField(primary_key=True)
    description = models.TextField()
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "permissions"


class PermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = Permission
        fields = ["code", "description"]
