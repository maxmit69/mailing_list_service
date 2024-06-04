from django.urls import path
from blogs_app import views
from blogs_app.apps import BlogsAppConfig

app_name = BlogsAppConfig.name


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog_delete'),

]
