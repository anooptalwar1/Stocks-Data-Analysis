securitySchemes = {
    "AuthZ": {
        "type": "openIdConnect",
        "openIdConnectUrl": "https://stg.authorization.go.com/.well-known/openid-configuration",
    },
}


def populate(result, generator, request, public):
    result["components"]["securitySchemes"] = securitySchemes
    return result
