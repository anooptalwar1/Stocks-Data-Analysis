from reporting.models import Role, Permission


def populate(result, generator, request, public):
    role_permissions_rs = Role.objects.raw(
        "SELECT roles.code, roles.name, rp.permission_code FROM roles INNER JOIN"
        " role_permissions rp on roles.code = rp.role_code ORDER BY roles.name"
    )

    header = ["<tr><th></th>"]
    role_permissions = {}
    for role in role_permissions_rs:
        if role.name not in role_permissions:
            role_permissions[role.name] = []
            header.append(f"<th>{role.name}</th>")
        role_permissions[role.name].append(role.permission_code)
    header.append("</tr>")

    body = []
    for permission in Permission.objects.order_by("code").all():
        body.append("<tr>")
        body.append(f"<td><strong>{permission.code}</strong></td>")
        for role in role_permissions.keys():
            body.append(f'<td>{"✓" if permission.code in role_permissions[role] else ""}</td>')
        body.append("</tr>")

    html = "<table>" + "<thead>" + "".join(header) + "</thead>" + "<tbody>" + "".join(body) + "</tbody>" + "</table>"
    result["info"]["description"] = result["info"]["description"].replace("AUTHORIZATION_PLACEHOLDER", html)
    return result
