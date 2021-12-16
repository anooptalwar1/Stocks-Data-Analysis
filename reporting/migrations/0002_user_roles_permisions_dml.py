from django.db import migrations

from reporting.models import User, Permission, Role, RolePermission, UserRole

permissions = {
    "stocks": {
        "instances": ["create", "update", "get", "list", "delete"],
    },
    "roles": {
        "instances": ["list"],
    },
    "users": {
        "instances": ["create", "update", "get", "list", "delete"],
    },
}

default_permissions = {
    "stocks": {
        "instances": ["get", "list"],
    },
}

roles = {
    "admin": {"name": "Administrator", "permissions": permissions},
    "stock_viewer": {"name": "Stocks Viewer", "permissions": default_permissions},
    "stock_admin": {
        "name": "Stocks Administrator",
        "permissions": {
            **default_permissions,
            **{
                "stocks": permissions["stocks"],
            },
        },
    },
    "user_admin": {
        "name": "User Administrator",
        "permissions": {
            **default_permissions,
            **{
                "roles": permissions["roles"],
                "users": permissions["users"],
            },
        },
    },
}

default_users = {
                "admin": {
                            "username": "admin",
                            "password": "admin",
                            "role": "admin"
                            },
                "viewer": {
                            "username": "viewer",
                            "password": "viewer",
                            "role": "stock_viewer"
                            }
                }

def _generate_permissions(data):
    result = []
    for resource, subresources in data.items():
        print(resource)
        for subresource, verbs in subresources.items():
            print(subresource)
            result = result + [f"{resource}.{subresource}.{verb}" for verb in verbs]
    return result


def load_roles(apps, schema_editor):
    Role.objects.bulk_create([Role(code=key, name=value["name"]) for key, value in roles.items()])


def load_permissions(apps, schema_editor):
    Permission.objects.bulk_create([Permission(code=p) for p in _generate_permissions(permissions)])


def load_role_permissions(apps, schema_editor):
    for role, value in roles.items():
        RolePermission.objects.bulk_create(
            [RolePermission(role_code=role, permission_code=p) for p in _generate_permissions(value["permissions"])]
        )


def load_default_users(apps, schema_editor):
    for user, data in default_users.items():
        if not User.objects.filter(username__iexact=user).exists():
            User.objects.create(first_name=user, last_name=user, username=data["username"], password=data["password"])
            user_data = User.objects.get(username=user)
            UserRole.objects.create(user_id=user_data.id, role_code=data["role"])
        else:
            print("Default users already exists")
    

class Migration(migrations.Migration):
    dependencies = [
        ("reporting", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_roles),
        migrations.RunPython(load_permissions),
        migrations.RunPython(load_role_permissions),
        migrations.RunPython(load_default_users),
    ]
