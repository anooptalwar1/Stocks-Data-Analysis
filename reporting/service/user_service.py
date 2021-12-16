import pandas as pd
from django.db.models import QuerySet
from rest_framework.settings import api_settings

from reporting.models import (
    UserRole,
    User,
)
from reporting.models.user import UserSerializer


class UserService:
    def __init__(self):
        pass

    def insert(self, data) -> dict:
        roles = data.pop("roles", None)

        if User.objects.filter(username__iexact=data["username"]).exists():
            raise ValueError("Already Exists")

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if roles is not None:
            user.roles = [r.role_code for r in self.map_roles(user_id=user.id, roles=roles)]

        return user

    def update(self, user_id: str, data):
        User.objects.filter(id=user_id).update(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            active=data["active"],
        )

        roles = data.pop("roles", None)

        if roles is not None:
            self.map_roles(user_id=user_id, roles=roles)

    def map_roles(self, user_id, roles):
        UserRole.objects.filter(user_id=user_id).exclude(role_code__in=roles).delete()

        result = []
        for role in roles:
            result.append(
                UserRole.objects.get_or_create(
                    user_id=user_id,
                    defaults={
                        "role_code": role,
                    },
                )[0]
            )
        return result

    def get_by_username(self, username):
        qs = User.objects.raw(
            """
            SELECT users.id AS id, users.first_name, users.last_name, users.username, users.active,
                   r.code AS role_code, p.code AS permission_code
                FROM users
                    LEFT JOIN user_roles ur on users.id = ur.user_id
                    LEFT JOIN roles r on ur.role_code = r.code
                    LEFT JOIN role_permissions ON r.code = role_permissions.role_code
                    LEFT JOIN permissions p on role_permissions.permission_code = p.code
                    WHERE users.active=true and lower(users.username)=%s
            """,
            [username.lower()],
        )

        users_df = pd.DataFrame([item.__dict__ for item in qs])
        if len(users_df) == 0:
            return []
        elif len(users_df["username"].drop_duplicates()) > 1:
            raise ValueError("Duplicate username")

        return User(
            **{
                "id": int(users_df["id"].values[0]),
                "first_name": users_df["first_name"].values[0],
                "last_name": users_df["last_name"].values[0],
                "username": users_df["username"].values[0],
                "active": bool(users_df["active"].values[0]),
                "roles": users_df["role_code"].drop_duplicates().dropna().to_list(),
                "permissions": users_df["permission_code"].drop_duplicates().dropna().to_list(),
            }
        )

    def list(self, search, include_inactive, order_by, limit=api_settings.PAGE_SIZE, offset=0):
        if offset < 0:
            offset = 0

        search = f"%{search}%".lower() if search is not None else None

        qs = User.objects.raw(
            """
            SELECT users.id AS id, users.first_name, users.last_name, users.username, users.active,
                   r.code AS role_code
                FROM users
                    LEFT JOIN user_roles ur on users.id = ur.user_id
                    LEFT JOIN roles r on ur.role_code = r.code
                    WHERE (TRUE = %(include_inactive)s OR users.active=true) AND
                        (TRUE =  %(no_search)s OR (lower(users.first_name) like %(search)s
                        OR lower(users.last_name) like %(search)s
                        OR lower(users.username) like %(search)s))
                    ORDER BY  
                        CASE %(order_by)s WHEN 'first_name' THEN users.first_name END ASC,
                        CASE %(order_by)s WHEN '-first_name' THEN users.first_name END DESC,
                        CASE %(order_by)s WHEN 'role_code' THEN r.code END ASC,
                        CASE %(order_by)s WHEN '-role_code' THEN r.code END DESC
                    LIMIT %(limit)s OFFSET %(offset)s
            """,
            {
                "include_inactive": include_inactive,
                "no_search": search is None,
                "search": search,
                "order_by": order_by,
                "limit": limit,
                "offset": offset,
            },
        )

        users_df = pd.DataFrame([item.__dict__ for item in qs])

        users = []
        if not users_df.empty:
            for user_id in users_df["id"].drop_duplicates(inplace=False):
                user_df = users_df[users_df["id"] == user_id]

                users.append(
                    User(
                        **{
                            "id": user_id,
                            "first_name": user_df["first_name"].values[0],
                            "last_name": user_df["last_name"].values[0],
                            "username": user_df["username"].values[0],
                            "active": user_df["active"].values[0],
                            "roles": user_df["role_code"].drop_duplicates().dropna().to_list()
                            # .drop_duplicates()
                            # .dropna()
                            # .to_dict("records"),
                        }
                    )
                )

        return users

    def delete(self, user_id):
        User.objects.filter(id=user_id).update(active=False)

    def exists(self, user_id, check_active: bool = False):
        qs: QuerySet = User.objects.filter(id=user_id)
        if check_active:
            qs.filter(active=True)
        return qs.exists()
