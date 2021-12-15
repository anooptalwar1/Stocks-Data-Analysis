from django.http.response import JsonResponse
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, request):
        return JsonResponse({"headers": {k: request.headers[k] for k in request.headers.keys()}})
