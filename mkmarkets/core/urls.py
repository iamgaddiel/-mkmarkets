from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    dispacther
)


app_name = "core"

urlpatterns = [
    path("", LoginView.as_view(template_name="core/login.html"), name="index"),
    path("dispatcher/", dispacther, name="dispacher")
]