from typing import Any, Dict, Optional
from zipfile import ZipFile
import zipfile
from django import http
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth.models import User
from django.conf import settings
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
from .utils import get_random_string

from telethon import TelegramClient

from django.contrib.auth.hashers import make_password
from .models import Profile

from .forms import AccountGenerateForm, UserCreationForm, UserUpdateForm


def dispacther(request):
    if request.user.is_superuser:
        return redirect("core:admin_dashboard")
    return redirect('core:user_dashboard')


def delete_user(request, pk):
    User.objects.get(pk=pk).delete()
    return redirect('core:admin_dashboard')


class Index(TemplateView):
    template_name = 'core/index.html'


class AdminDashboard(ListView):
    template_name = "core/admin_dashboard.html"
    model = User
    paginate_by = 20


class CreateUser(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('core:admin_dashboard')
    template_name = 'core/user_create.html'
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


class UserDashboard(LoginRequiredMixin, View):
    template_name = "core/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {'form': AccountGenerateForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if (form := AccountGenerateForm(request.POST)).is_valid():

            context = {'form': AccountGenerateForm()}
            current_bal: int = int(request.user.profile.balance)
            account_quantity: int = int(form.data.get('accounts'))

            # telgram credentials
            telegram_session_dir: str = settings.TELEGRAM_SESSIONS_DIR
            telegram_api_id: str = settings.TELEGRAM_APP_ID
            telegram_api_hash: str = settings.TELEGRAM_HASH
            telegram_session_file = f"{telegram_session_dir}{get_random_string()}"
            telegram_session_files = []

            # todo: include lemon login details

            # * check if current bal is sufficient
            if current_bal < 14:
                context['error'] = 'insufficient balance'
                return render(request, self.template_name, context)

            else:
                # Current Balance Deduction
                required_fee: int = account_quantity * 14
                if current_bal < required_fee:
                    context['error'] = 'Not sufficient'
                    return render(request, self.template_name, context)


                # Generate required amount of telegram session files
                for _ in range(account_quantity):

                    proxy: dict = {
                        'proxy_type': 'socks5',
                        'addr': '192.111.130.2',
                        'port': 4145
                    }
                    telegram_session_files.append(telegram_session_file) #list of telegram session files
                    with TelegramClient(telegram_session_file, telegram_api_id, telegram_api_hash, proxy=proxy) as client:
                        client.loop.run_until_complete(client.session.save())

                with ZipFile(telegram_session_dir, 'w') as zip_:
                    for telegram_session_file in telegram_session_files:
                        zip_.write(telegram_session_file)

        return redirect('core:user_dashboard')
