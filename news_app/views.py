from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, DetailView
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from news_app.models import Post, Category, Tag
from news_app.forms import ContactForm, CommentForm, NewsLetterForm
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


class SafePaginationMixin:
    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size)
        page_number = self.request.GET.get("page", 1)
        try:
            page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page = paginator.page(1)
        return paginator, page, page.object_list, page.has_other_pages()


class HomeView(ListView):
    model = Post
    template_name = "aznews/index.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=False, status="active")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["single_trending_post"] = self.queryset.order_by(
            "-view_count", "-published_at"
        ).first()
        context["button_trending"] = self.queryset.order_by(
            "-view_count", "-published_at"
        )[1:4]
        context["button_right"] = self.queryset.order_by("-published_at")[1:5]
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = self.queryset.filter(
            published_at__gte=one_week_ago
        ).order_by("-published_at", "-view_count")[:8]
        context["recent_posts"] = self.queryset.order_by("-published_at")[:5]
        context["whatnews_top_6"] = self.queryset.order_by("-published_at")[:6]

        return context


class AboutView(TemplateView):
    template_name = "aznews/about.html"


class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self, req):
        return render(req, self.template_name)

    def post(self, req):
        form = ContactForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "Successfully submit your data", extra_tags="contact")
            return redirect("contact")
        else:
            messages.error(req, "Cannot  submit your data", extra_tags="contact")
            return redirect("contact")


class PostListView(SafePaginationMixin, ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1
    queryset = Post.objects.filter(
        published_at__isnull=False,
        status="active",
    ).order_by("-published_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/details/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
        )
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = super().get_queryset()
        obj = self.get_object()
        obj.view_count += 1
        obj.save()
        context["previous_post"] = query.filter(id__lt=obj.id).order_by("-id").first()
        context["next_post"] = query.filter(id__gt=obj.id).order_by("id").first()
        return context


class CommentView(View):
    def post(self, req, *args, **kwargs):
        form = CommentForm(req.POST)
        post_id = req.POST.get("post")
        if form.is_valid():
            form.save()
            messages.success(req, "Your comment was posted successfully")
            return redirect("post-details", pk=post_id)
        messages.error(req, "Please correct the errors below")
        return redirect("post-details", pk=post_id)


class PostByCategory(SafePaginationMixin, ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category_id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query


class PostByTag(SafePaginationMixin, ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            tag=self.kwargs["tag_id"],
        ).order_by("-published_at")
        return query


class NewsLettersView(View):
    def post(self, req):
        form = NewsLetterForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(
                req, "Successfully submit your data", extra_tags="newsletter"
            )
        else:
            messages.error(req, "Cannot submit your data", extra_tags="newsletter")
        return redirect(req.META.get("HTTP_REFERER", "/"))


class PostSearchView(View):
    template_name = "aznews/list/list.html"

    def get(self, req, *args, **kwargs):
        query = (req.GET.get("query") or "").strip()
        post_list = Post.objects.filter(
            status="active",
            published_at__isnull=False,
        )
        if query:
            post_list = post_list.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        post_list = post_list.order_by("-published_at")
        page = req.GET.get("page", 1)
        paginate_by = 1
        paginator = Paginator(post_list, paginate_by)
        try:
            posts = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            posts = paginator.page(1)
        return render(
            req,
            self.template_name,
            {
                "query": query,
                "posts": posts,
                "page_obj": posts,
            },
        )
