from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    View,
    UpdateView,
    CreateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from news_app.models import Post
from blog_app.forms import PostForm, RegisterForm


class Postlist(ListView):
    model = Post
    template_name = "admindashboard/post_list.html"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")
    context_object_name = "posts"


class Draftlist(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admindashboard/draft_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=True, author=self.request.user
        ).order_by("-published_at")


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "admindashboard/post_create.html"
    context_object_name = "posts"
    success_url = reverse_lazy("news_admin:draft_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetails(DetailView):
    model = Post
    template_name = "admindashboard/post_details.html"
    context_object_name = "post"
    pk_url_kwarg = "id"

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=False)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        publish = self.object.published_at

        if self.object.image:
            self.object.image.delete(save=False)

        self.object.delete()
        if publish:
            return redirect("news_admin:post_list")
        else:
            return redirect("news_admin:draft_list")


class DraftDetails(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "admindashboard/draft_details.html"
    context_object_name = "post"
    pk_url_kwarg = "id"

    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=True)


class DraftPublished(LoginRequiredMixin, DetailView):
    def get(self, req, id):
        post = Post.objects.get(id=id, author=req.user, published_at__isnull=True)
        post.published_at = timezone.now()
        post.status = "active"
        post.save()
        return redirect("news_admin:post_list")


class PostUnpublished(LoginRequiredMixin, View):
    def get(self, req, id):
        post = Post.objects.get(id=id, published_at__isnull=False)
        post.published_at = None
        post.save()
        return redirect("news_admin:draft_list")


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "admindashboard/post_create.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        if self.object.published_at:
            return reverse_lazy("news_admin:post_detail", kwargs={"id": self.object.id})
        else:
            return reverse_lazy("news_admin:draft_detail", kwargs={"id": self.object.id})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
