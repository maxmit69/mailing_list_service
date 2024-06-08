from django.urls import path
from mailing_app import views
from mailing_app.apps import MailingAppConfig

app_name = MailingAppConfig.name

urlpatterns = [

    # Главная страница
    path('', views.HomePageView.as_view(), name='home_page'),
    # Клиенты
    path('customers/', views.CustomersListView.as_view(), name='customers_list'),
    path('customers/create/', views.CustomersCreateView.as_view(), name='customers_create'),
    path('customers/detail/<int:pk>/', views.CustomersDetailView.as_view(), name='customers_detail'),
    path('customers/update/<int:pk>/', views.CustomersUpdateView.as_view(), name='customers_update'),
    path('customers/delete/<int:pk>/', views.CustomersDeleteView.as_view(), name='customers_delete'),

    # Сообщения
    path('message/', views.MessageListView.as_view(), name='message_list'),
    path('message/create/', views.MessageCreateView.as_view(), name='message_form'),
    path('message/detail/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),

    # Рассылки
    path('mailing/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/detail/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/delete/<int:pk>/', views.MailingDeleteView.as_view(), name='mailing_delete'),

    # Попытки отправки
    path('attempts/', views.AttemptSendListView.as_view(), name='attempts_list'),
]
