from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView

from mailing.forms import MailingForm, MailingManagerForm
from mailing.models import Mailing, Client, Message, MailingStatus
from mailing.services import get_cached_blogs


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.groups.filter(name='manager'):
            return MailingManagerForm


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')


class MailingStatusListView(LoginRequiredMixin, ListView):
    model = MailingStatus


class MailingStatusDetailView(LoginRequiredMixin, DetailView):
    model = MailingStatus


class HomePageView(TemplateView):
    template_name = 'mailing/home_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Client.objects.all()
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(status='start').count()
        context_data['active_clients'] = clients.values('email').distinct().count()

        context_data['random_blogs'] = get_cached_blogs().order_by('?')[:3]
        return context_data
