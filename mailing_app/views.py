from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from blogs_app.models import Blog
from config.settings import CACHE_ENABLED
from mailing_app.forms import MessageForm, MailingForm, CustomersForm
from mailing_app.models import Customers, Message, Mailing, AttemptSend
from mailing_app.services import send_mailing, schedule_task, schedule_or_send_mailing
from django.core.cache import cache


class HomePageView(TemplateView):
    """ Главная страница
    """
    template_name = 'mailing_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_list'] = Blog.objects.order_by('?')[:3]
        context['mailing_list'] = Mailing.objects.all()
        mailing_active_count = Mailing.objects.filter(status='launched').count()
        context['mailing_active_count'] = mailing_active_count  # Количество активных рассылок

        if CACHE_ENABLED:
            key = f'unique_clients_count'
            unique_clients_count = cache.get(key)

            if unique_clients_count is None:
                unique_clients_count = Customers.objects.filter(unique_clients=True).count()
                cache.set(key, unique_clients_count, 60 * 60 * 24)  # Кэшируем на 24 часа

            context['unique_clients_count'] = unique_clients_count
        else:
            unique_clients_count = Customers.objects.filter(unique_clients=True).count()
            context['unique_clients_count'] = unique_clients_count

        return context


class CustomersListView(LoginRequiredMixin, generic.ListView):
    model = Customers
    template_name = 'mailing_app/customers_list.html'

    def get_queryset(self):
        """ Если пользователь не админ, то он может просматривать только своих клиентов
        """
        if self.request.user.is_superuser:
            return Customers.objects.all()
        return Customers.objects.filter(user_customer=self.request.user)


class CustomersDetailView(LoginRequiredMixin, generic.DetailView):
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
        """ Если пользователь владелец клиента или админ, то он может его редактировать
        """
        if self.request.user == self.get_object().user_customer or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать клиента пользователя{self.get_object().user_customer}")


class CustomersDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customers
    template_name = 'mailing_app/customer_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:customers_list')

    def form_valid(self, form):
        """ Если пользователь владелец клиента или админ, то он может его удалить
        """
        if self.request.user == self.get_object().user_customer or self.request.user.is_superuser:
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


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
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
        """ Если пользователь владелец сообщения или админ, то он может его редактировать
        """
        if self.request.user == self.get_object().user_message or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать сообщение пользователя{self.get_object().user_message}")


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        """ Если пользователь владелец сообщения или админ, то он может его удалить
        """
        if self.request.user == self.get_object().user_message or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может удалить сообщение пользователя{self.get_object().user_message}")


class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'

    def get_queryset(self):
        """ Если пользователь не админ, то он может просматривать только свои рассылки
        """
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(user_mailing=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_list'] = Blog.objects.all()[:3]  # Выводим 3 блога
        return context


class MailingDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mailing
    template_name = 'mailing_app/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def get_form_kwargs(self):
        """ Вывод в форму только клиентов, созданных текущим пользователем
        """
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """ Сохраняем пользователя, который создал рассылку
        """
        mailing = form.save(commit=False)
        mailing.user_mailing = self.request.user
        mailing.save()

        # Сохраняем форму
        response = super().form_valid(form)

        # Вызываем schedule_or_send_mailing для немедленного запуска или планирования задачи
        schedule_or_send_mailing(mailing)

        return response


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        """ Если пользователь владелец рассылки или админ, то он может ее удалить
        """
        if self.request.user == self.get_object().user_mailing or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может удалить рассылку пользователя {self.get_object().user_mailing}")


class AttemptSendListView(LoginRequiredMixin, generic.ListView):
    model = AttemptSend
    template_name = 'mailing_app/attempts_list.html'
    context_object_name = 'attempt_list'

    def get_queryset(self):
        """ Вывод отчета проведенных рассылок только созданных текущим пользователем если не админ
        """
        if self.request.user.is_superuser:
            return AttemptSend.objects.all()
        return AttemptSend.objects.filter(user_attempt=self.request.user)
