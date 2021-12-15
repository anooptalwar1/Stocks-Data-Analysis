from django.db import models
from rest_framework import serializers


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    active = models.BooleanField(default=True)
    username = models.TextField(db_index=True)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=10000,null=True)
    
    def __init__(self, *args, **kwargs):
        self.permissions = kwargs.pop("permissions", [])
        self.roles = kwargs.pop("roles", None)
        
        kwargs.pop("is_authenticated", None)

        super(User, self).__init__(*args, **kwargs)

        self.is_authenticated = self.active

    class Meta:
        db_table = "users"

        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                name="uq_username",
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.ReadOnlyField()
    roles = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "active",
            "token",
            "permissions",
            "roles",
        ]
