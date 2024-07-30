from django import forms

from mailing.models import Client, Message, Mailing, MailingStatus


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ClientForm(StyleMixin, forms.Form):
    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleMixin, forms.Form):
    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleMixin, forms.Form):
    class Meta:
        model = Mailing


class MailingManagerForm(StyleMixin, forms.Form):
    class Meta:
        model = Mailing
        fields = ("status",)


class MailingStatusForm(StyleMixin, forms.Form):
    class Meta:
        model = MailingStatus
