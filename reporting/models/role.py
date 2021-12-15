from django.db import models
from django.utils import timezone
from rest_framework import serializers


class Role(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "roles"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["code", "name", "description"]
