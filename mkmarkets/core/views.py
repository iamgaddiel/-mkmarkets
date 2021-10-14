from django.shortcuts import redirect, render
from django.views.generic import (
    TemplateView, 
    CreateView, 
    DeleteView, 
    View
)




def dispacther(request):
    if request.user.is_supperuser:
        return redirect("core:admin_dashboard")
    return render(request, "core/user_dashboard")

class AdminDashboard(TemplateView):
    template_name = "core/index.html"

class UserDashboard(TemplateView):
    template_name = "core/index.html"

