from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
)

from mailing.forms import MailingForm, MailingManagerForm
from mailing.models import Mailing, Client, Message, MailingStatus
from mailing.services import get_cached_blogs


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = "__all__"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.groups.filter(name="manager"):
            return MailingManagerForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = "__all__"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("mailing:client_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = "__all__"
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = "__all__"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class MailingStatusListView(LoginRequiredMixin, ListView):
    model = MailingStatus


class MailingStatusDetailView(LoginRequiredMixin, DetailView):
    model = MailingStatus


class HomePageView(TemplateView):
    template_name = "mailing/home_page.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Client.objects.all()
        context_data["all_mailings"] = mailings.count()
        context_data["active_mailings"] = mailings.filter(status="start").count()
        context_data["active_clients"] = clients.values("email").distinct().count()

        context_data["random_blogs"] = get_cached_blogs().order_by("?")[:3]
        return context_data
