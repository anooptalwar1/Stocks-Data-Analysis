from django.urls import path
from reporting.views.users_view import UserView
from reporting.views.role_view import RoleView
from reporting.views.stock_view import StockView
from reporting.views.login_view import LoginView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


app_name = "reporting"

urlpatterns = [
    # path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('login', LoginView.as_view({"get": "login"})),
    # path('token', UserView.as_view({"get": "getToken"})),
    # path('auth', UserView.as_view({"get": "auth"})),
    path("users", UserView.as_view({"get": "list", "post": "create"})),
    path("users/me", UserView.as_view({"get": "me"})),
    path("users/<user_id>", UserView.as_view({"put": "update", "delete": "delete"})),
    path("roles", RoleView.as_view({"get": "list"})),
    path('stocks', StockView.as_view({'get': 'list', 'post': 'create'})),
    path('stocks/<id>', StockView.as_view({'get': 'get', 'patch': 'update', 'delete': 'delete'})),
    
]
