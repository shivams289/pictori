from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.
def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(
    DetailView
):  # default template it will will look for in <app>/<model>_<viewtype>.html
    model = Post


class PostCreateView(
    LoginRequiredMixin, CreateView
):  # default template it will will look for in <app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):  # default template it will will look for in <app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        return False


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):  # default template it will will look for in <app>/<model>_<viewtype>.html
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
