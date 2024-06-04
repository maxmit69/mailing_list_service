from django import forms
from .models import Mailing, Message, Customers


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'content',)


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('periodicity', 'massage', 'customers')


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('full_name', 'email', 'comment',)
