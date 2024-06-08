from django import forms
from .models import Mailing, Message, Customers


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        """ Переопределите метод __init__ формы для добавления атрибута class.
        """
        super().__init__(*args, **kwargs)
        # Добавление атрибута class к каждому полю формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'content',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'periodicity', 'status', 'massage', 'customers')

    def __init__(self, *args, **kwargs):
        """ Переопределите метод __init__ формы для фильтрации.
        """
        user = kwargs.pop('user', None)  # Получение пользователя из kwargs
        super(MailingForm, self).__init__(*args, **kwargs)
        if user:
            # Фильтрация сущностей, созданных текущим пользователем
            self.fields['customers'].queryset = Customers.objects.filter(user_customer=user)
            self.fields['massage'].queryset = Message.objects.filter(user_message=user)


class CustomersForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('full_name', 'email', 'comment', 'unique_clients')
