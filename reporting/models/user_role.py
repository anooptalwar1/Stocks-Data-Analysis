from django.db import models
from rest_framework import serializers

from reporting.models.helpers.foriegn_key_code_based import ForeignKeyCodeBased
from reporting.models.role import RoleSerializer
from reporting.models.user import UserSerializer


from reporting.models import User

class UserRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, db_column="user_id", null=False)
    role = ForeignKeyCodeBased("Role", on_delete=models.CASCADE, db_column="role_code", null=False)

    class Meta:
        db_table = "user_roles"


class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    user = UserSerializer()

    class Meta:
        model = UserRole
        fields = ["id", "user", "role"]
