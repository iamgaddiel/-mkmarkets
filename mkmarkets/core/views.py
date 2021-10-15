from typing import Any, Dict, Optional
from django import http
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView, 
    CreateView, 
    DeleteView, 
    View,
    ListView,
    DetailView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    UserPassesTestMixin, 
    LoginRequiredMixin
)
from django.contrib.auth.hashers import make_password
from .models import Profile

from .forms import UserCreationForm, UserUpdateForm




def dispacther(request):
    if request.user.is_superuser:
        return redirect("core:admin_dashboard")
    return render(request, "core/dashboard.html")

def delete_user(request, pk):
    User.objects.get(pk=pk).delete()
    return redirect('core:admin_dashboard')

class AdminDashboard(ListView):
    template_name = "core/admin_dashboard.html"
    model = User
    paginate_by = 20

class CreateUser(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('core:admin_dashboard')
    template_name='core/user_create.html'
    form_class = UserCreationForm

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_superuser:
            return True
        return False

    def form_valid(self, form) -> HttpResponse:
        pswd = form.instance.password
        confirm_pswd = self.request.POST.get('password_confirm')

        if pswd != confirm_pswd:
            return render(self.request, self.template_name, {
                'confirm_err': 'passwords do not match',
                'form': self.form_class
            })
        form.instance.password = make_password(pswd)
        form.save()
        return super().form_valid(form)


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'core/user_update.html'
    model = Profile
    form_class = UserUpdateForm

    def form_valid(self, form) -> HttpResponse:
        user_pk = self.kwargs.get('pk')
        form.instance.balance += Profile.objects.get(pk=user_pk).balance
        form.save()
        return redirect('core:user_update', pk=user_pk)

    def test_func(self) -> Optional[bool]:
        if self.request.user.is_superuser:
            return True
        return False

class UserDashboard(TemplateView):
    template_name = "core/index.html"

