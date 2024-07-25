from django import forms

from mailing.models import Client, Message, Mailing, MailingStatus


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ClientForm(forms.Form):
    class Meta:
        model = Client


class MessageForm(forms.Form):
    class Meta:
        model = Message


class MailingForm(forms.Form):
    class Meta:
        model = Mailing


class MailingStatusForm(forms.Form):
    class Meta:
        model = MailingStatus
