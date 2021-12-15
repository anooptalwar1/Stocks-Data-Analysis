def drop(result, generator, request, public):
    result["paths"].pop("/api/docs/openapi")
    return result
