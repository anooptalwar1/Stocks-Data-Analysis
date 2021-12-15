from datetime import datetime, timedelta, timezone


class QueryParams:
    def __init__(self, request, **kwargs):
        self.user = request.user
        self.limit = int(request.query_params.get("limit", 1000))
        self.page_number = int(request.query_params.get("pageNumber", 0))
        self.page_size = int(request.query_params.get("pageSize", 50))

        self._parse_boolean(request, "active")
        self._parse_start_date(request)
        self._parse_end_date(request)

    def _parse_start_date(self, request):
        start_date = request.query_params.get("start_date", None)
        if start_date is not None:
            start_date = int(start_date) / 1000 if len(start_date) == 13 else int(start_date)
            self.start_date = datetime.fromtimestamp(start_date, timezone.utc)
        else:
            self.start_date = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0) - timedelta(days=-30)

    def _parse_end_date(self, request):
        end_date = request.query_params.get("end_date", None)
        if end_date is not None:
            end_date = int(end_date) / 1000 if len(end_date) == 13 else int(end_date)
            self.end_date = datetime.fromtimestamp(end_date, timezone.utc)
        else:
            self.end_date = datetime.now().replace(microsecond=59, second=59, minute=59, hour=23)

    def _parse_boolean(self, request, key):
        value = request.query_params.get(key)
        if value is not None and (value.lower() == "true" or value.lower() == "false"):
            setattr(self, key, bool(value))
