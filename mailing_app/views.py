from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from blogs_app.models import Blog
from mailing_app.forms import MessageForm, MailingForm, CustomersForm
from mailing_app.models import Customers, Message, Mailing, AttemptSend
from mailing_app.services import stop_mailing, start_mailing


# Create your views here.
class CustomersListView(LoginRequiredMixin, generic.ListView):
    model = Customers
    template_name = 'mailing_app/customers_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customers.objects.all()
        return Customers.objects.filter(user_customer=self.request.user)


class CustomersDetailView(generic.DetailView):
    model = Customers


class CustomersCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customers
    form_class = CustomersForm
    template_name = 'mailing_app/customers_form.html'
    success_url = reverse_lazy('mailing_app:customers_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_customer = self.request.user
        return super().form_valid(form)


class CustomersUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customers
    form_class = CustomersForm
    template_name = 'mailing_app/customers_update.html'
    success_url = reverse_lazy('mailing_app:customers_list')

    def form_valid(self, form):
        if self.request.user == self.get_object().user_customer:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать клиента пользователя{self.get_object().user_customer}")


class CustomersDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customers
    template_name = 'mailing_app/customer_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:customers_list')

    def form_valid(self, form):
        """ Если пользователь владелец клиента, то он может его удалить
        """
        if self.request.user == self.get_object().user_customer:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может удалить клиента пользователя{self.get_object().user_customer}")


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(user_message=self.request.user)


class MessageDetailView(generic.DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_message = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        """ Если пользователь владелец сообщения, то он может его редактировать
        """
        if self.request.user == self.get_object().user_message:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать сообщение пользователя{self.get_object().user_message}")


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        """ Если пользователь владелец сообщения, то он может его удалить
        """
        if self.request.user == self.get_object().user_message:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может удалить сообщение пользователя{self.get_object().user_message}")


class MailingListView(generic.ListView):
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = AttemptSend.objects.all()
        context['blogs'] = Blog.objects.all()
        return context


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = 'mailing_app/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_mailing = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:message_form')

    def form_valid(self, form):
        """ Если пользователь владелец рассылки, то он может ее редактировать
        """
        if self.request.user == self.get_object().user_mailing:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать рассылку пользователя{self.get_object().user_mailing}")


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        """ Если пользователь владелец рассылки, то он может ее удалить
        """
        if self.request.user == self.get_object().user_mailing:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может удалить рассылку пользователя{self.get_object().user_mailing}")


class AttemptSendListView(generic.ListView):
    model = AttemptSend
    template_name = 'mailing_app/attempts_list.html'


def start_mailing_view(request: object, mailing_id: int) -> object:
    """ Запуск рассылки
    :param request: запрос
    :param mailing_id: идентификатор рассылки
    :return: статус рассылки
    """
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    start_mailing(mailing)
    return render(request, 'mailing_app/mailing_started.htm', {'mailing': mailing})


def stop_mailing_view(request: object, mailing_id: int) -> object:
    """ Остановка рассылки
    :param request: запрос
    :param mailing_id: идентификатор рассылки
    :return: статус рассылки
    """
    mailing = get_object_or_404(Mailing, pk=mailing_id)
    stop_mailing(mailing)
    return render(request, 'mailing_app/mailing_stopped.html', {'mailing': mailing})
