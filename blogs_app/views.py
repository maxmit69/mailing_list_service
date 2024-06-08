from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from blogs_app.forms import BlogForm
from blogs_app.models import Blog


# Create your views here.
class BlogListView(generic.ListView):
    model = Blog
    template_name = 'blogs_app/blog_list.html'

    def get_queryset(self):
        return Blog.objects.all()


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs_app/blog_form.html'
    success_url = reverse_lazy('blogs_app:blog_list')

    def form_valid(self, form):
        """ Только менеджер и админ может создавать блоги
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может создавать блоги")


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    fields = '__all__'
    template_name = 'blogs_app/blog_form.html'
    success_url = reverse_lazy('blogs_app:blog_list')

    def form_valid(self, form):
        """ Только менеджер и админ может редактировать блоги
        """
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseForbidden(
                f"{self.request.user} не может редактировать блоги")


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    template_name = 'blogs_app/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs_app:blog_list')

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, *args, **kwargs):
        """ Только менеджер и админ может удалять блоги
        """
        return super().dispatch(*args, **kwargs)
