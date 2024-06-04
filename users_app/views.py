import secrets

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from config.settings import EMAIL_HOST_USER
from users_app.forms import UserRegistrationForm, UserProfileForm
from users_app.models import User


# Create your views here.
class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users_app/register.html'
    success_url = reverse_lazy('users_app:login')

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        """ Отправка письма для активации аккаунта
        """
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f'http://{host}/users/activate/{token}/'
        send_mail(
            subject='Активация аккаунта',
            message=f'Для активации аккаунта перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        user.save()
        massage = 'Письмо с инструкциями по активации аккаунта отправлено на вашу почту'
        return HttpResponse(massage)


def activate_user(request, token):
    """ Активация аккаунта
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy('users_app:login'))


class ProfileView(generic.UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users_app:profile')

    def get_object(self, queryset=None):
        return self.request.user
