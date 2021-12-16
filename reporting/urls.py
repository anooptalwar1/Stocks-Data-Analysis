from django.urls import path
from reporting.views.users_view import UserView
from reporting.views.role_view import RoleView
from reporting.views.stock_view import StockView
from reporting.views.login_view import LoginView

app_name = "reporting"

urlpatterns = [

    path('login', LoginView.as_view({"get": "login"})),
    path("users", UserView.as_view({"get": "list", "post": "create"})),
    path("users/me", UserView.as_view({"get": "me"})),
    path("users/<user_id>", UserView.as_view({"put": "update", "delete": "delete"})),
    path("roles", RoleView.as_view({"get": "list"})),
    path('stocks', StockView.as_view({'get': 'list', 'post': 'create'})),
    path('stocks/<id>', StockView.as_view({'get': 'get', 'patch': 'update', 'delete': 'delete'})),
    
]
