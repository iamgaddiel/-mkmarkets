from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('_/', admin.site.urls),
    path('', include("core.urls"))
]
