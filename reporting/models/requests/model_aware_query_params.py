from reporting.models.requests.query_params import QueryParams


class ModelAwareQueryParams(QueryParams):
    def __init__(self, request, **kwargs):
        self.id = (
            kwargs["id"] if "id" in kwargs else request.query_params.get("id", None)
        )

        self.name = kwargs["name"] if "name" in kwargs else request.query_params.get("name", None)

        self.required = kwargs["required"] if "required" in kwargs else request.query_params.get("required", None)

        self.code = kwargs["code"] if "code" in kwargs else request.query_params.get("code", None)

        super().__init__(request, **kwargs)
