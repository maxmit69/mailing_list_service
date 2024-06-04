from users_app import views
from users_app.apps import UserAppConfig
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = UserAppConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('activate/<str:token>/', views.activate_user, name='activate')]
