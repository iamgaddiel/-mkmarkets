from django.contrib.auth.models import User
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    UserDashboard,
    delete_user,
    dispacther,
    AdminDashboard,
    CreateUser,
    UpdateUser,
    delete_user,
    Index
)


app_name = "core"

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("dispatcher/", dispacther, name="dispacher"),
    path('admin/dashboard/', AdminDashboard.as_view(), name="admin_dashboard"),
    path('create/user/', CreateUser.as_view(), name="user_created"),
    path('user/<int:pk>/update/', UpdateUser.as_view(), name='user_update'),
    path('user/trash/<int:pk>/', delete_user, name='user_delete'),
    path('user/dashboard/', UserDashboard.as_view(), name='user_dashboard')
]