from django.contrib import admin

from mailing.models import Client, Message, Mailing, MailingStatus


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_letter', 'body_letter')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'next_date', 'end_date', 'period', 'status')


@admin.register(MailingStatus)
class MailingStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_mailing_time', 'status_mailing', 'response_mailing')
