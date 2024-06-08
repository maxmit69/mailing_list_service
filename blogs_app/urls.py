from django.urls import path
from django.views.decorators.cache import cache_page

from blogs_app import views
from blogs_app.apps import BlogsAppConfig

app_name = BlogsAppConfig.name

urlpatterns = [
    path('', cache_page(60)(views.BlogListView.as_view()), name='blog_list'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('detail/<int:pk>/', cache_page(60)(views.BlogDetailView.as_view()), name='blog_detail'),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog_delete'),

]
