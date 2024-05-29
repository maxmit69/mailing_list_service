from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from mailing_app.models import Customers, Message, Mailing, AttemptSend


# Create your views here.
class CustomersListView(generic.ListView):
    model = Customers
    template_name = 'mailing_app/customers_list.html'


class CustomersDetailView(generic.DetailView):
    model = Customers


class CustomersCreateView(generic.CreateView):
    model = Customers
    fields = '__all__'
    template_name = 'mailing_app/customers_form.html'
    success_url = reverse_lazy('mailing_app:customers_list')


class CustomersUpdateView(generic.UpdateView):
    model = Customers
    fields = '__all__'
    template_name = 'mailing_app/customers_update.html'


class CustomersDeleteView(generic.DeleteView):
    model = Customers
    template_name = 'mailing_app/customer_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:customers_list')


class MessageListView(generic.ListView):
    model = Message


class MessageDetailView(generic.DetailView):
    model = Message


class MessageCreateView(generic.CreateView):
    model = Message
    fields = ('title', 'content',)
    success_url = reverse_lazy('mailing_app:message_list')


class MessageUpdateView(generic.UpdateView):
    model = Message
    fields = ('title', 'content',)
    success_url = reverse_lazy('mailing_app:message_list')


class MessageDeleteView(generic.DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'


class MailingListView(generic.ListView):
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = 'mailing_app/mailing_detail.html'


class MailingCreateView(generic.CreateView):
    model = Mailing
    fields = '__all__'
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    fields = '__all__'
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:message_form')


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')


class AttemptSendListView(generic.ListView):
    model = AttemptSend
