from django.db import models

from reporting.models.helpers.foriegn_key_code_based import ForeignKeyCodeBased


class RolePermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = ForeignKeyCodeBased("Role", on_delete=models.CASCADE, db_column="role_code", null=False)
    permission = ForeignKeyCodeBased("Permission", on_delete=models.CASCADE, db_column="permission_code", null=False)

    class Meta:
        db_table = "role_permissions"
