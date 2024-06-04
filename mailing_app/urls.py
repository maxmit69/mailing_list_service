from django.urls import path
from mailing_app import views
from mailing_app.apps import MailingAppConfig

app_name = MailingAppConfig.name

urlpatterns = [
    path('customers/', views.CustomersListView.as_view(), name='customers_list'),
    path('customers/create/', views.CustomersCreateView.as_view(), name='customers_create'),
    path('<int:pk>/', views.CustomersDetailView.as_view(), name='customers_detail'),
    path('<int:pk>/update/', views.CustomersUpdateView.as_view(), name='customers_update'),
    path('<int:pk>/delete/', views.CustomersDeleteView.as_view(), name='customers_delete'),
    path('message/', views.MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', views.MessageCreateView.as_view(), name='message_form'),
    path('message/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('attempts/', views.AttemptSendListView.as_view(), name='attempts_list'),
    path('start_mailing/<int:mailing_id>/', views.start_mailing_view, name='start_mailing'),
    path('stop_mailing/<int:mailing_id>/', views.stop_mailing_view, name='stop_mailing'),
]
