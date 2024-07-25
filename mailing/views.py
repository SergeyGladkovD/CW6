from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from mailing.models import Mailing, Client, Message, MailingStatus


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(CreateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailing:message_list')


class MailingStatusListView(ListView):
    model = MailingStatus


class MailingStatusDetailView(DetailView):
    model = MailingStatus


def home_page(request):
    return render(request, "mailing/home_page.html")
