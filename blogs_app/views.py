from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from blogs_app.models import Blog


# Create your views here.
class BlogListView(generic.ListView):
    model = Blog
    template_name = 'blogs_app/blog_list.html'


class BlogCreateView(generic.CreateView):
    model = Blog
    fields = '__all__'
    template_name = 'blogs_app/blog_form.html'
    success_url = reverse_lazy('blogs_app:blog_list')


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = '__all__'
    template_name = 'blogs_app/blog_form.html'
    success_url = reverse_lazy('blogs_app:blog_list')


class BlogDeleteView(generic.DeleteView):
    model = Blog
    template_name = 'blogs_app/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs_app:blog_list')
