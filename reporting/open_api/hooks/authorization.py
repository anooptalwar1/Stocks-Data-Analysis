from reporting.open_api.hooks.securitySchemes import securitySchemes


def populate(result, generator, request, public):
    for path, methods in result["paths"].items():
        for method, value in methods.items():
            permission = value["security"][0] if "security" in value and type(value["security"][0]) == str else None
            value["security"] = []
            for scheme in securitySchemes.keys():
                value["security"].append({scheme: [permission] if permission else []})
    return result
