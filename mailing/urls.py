from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import home_page, ClientListView, ClientDetailView, ClientDeleteView, ClientUpdateView, \
    ClientCreateView, MessageDetailView, MessageListView, MessageDeleteView, MessageUpdateView, MessageCreateView, \
    MailingListView, MailingDetailView, MailingDeleteView, MailingUpdateView, MailingCreateView, MailingStatusListView, \
    MailingStatusDetailView

app_name = MailingConfig.name


urlpatterns = [
    # начальная страница
    path('', home_page, name='home_page'),
    # клиент
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    # письмо
    path("message/", MessageListView.as_view(), name="message_list"),
    path('message/view/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    # рассылки
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/view/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    # отчет о проведенных рассылках
    path("mailing_status/", MailingStatusListView.as_view(), name="mailing_status"),
    path('mailing_status/view/<int:pk>/', MailingStatusDetailView.as_view(), name='mailing_status_detail'),
]
