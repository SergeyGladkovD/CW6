import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def send_message(request):
    return render(request, "users/send_message.html")


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.view_all_users"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = super().get_queryset().exclude(pk=user.pk)
        else:
            queryset = (
                super()
                .get_queryset()
                .exclude(pk=user.pk)
                .exclude(is_superuser=True)
                .exclude(is_staff=True)
            )
        return queryset


@permission_required("users.deactivate_user")
def toggle_activity(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse("users:view_all_users"))


class UserDetailView(DetailView):
    model = User


class UserUpdateView(UpdateView):
    model = User
    fields = ("email", "avatar", "phone", "country")
    success_url = reverse_lazy("users:login")
