from django.db.models import Prefetch

from news_app.models import Post, Category, Tag


def navigation(req):
    trending_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-view_count")[:3]
    published_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")
    categories = Category.objects.prefetch_related(
        Prefetch("posts", queryset=published_posts, to_attr="published_posts")
    )[:5]
    tags = Tag.objects.all()[:10]
    random_posts = Post.objects.filter(
        published_at__isnull=False, status="active", image__isnull=False
    ).order_by("?")[:6]
    footer_images = Post.objects.filter(
        published_at__isnull=False, status="active", image__isnull=False
    ).order_by("?")[:6]
    recent_posts = published_posts[:4]

    return {
        "trending_posts": trending_posts,
        "categories": categories,
        "tags": tags,
        "random_posts": random_posts,
        "footer_images": footer_images,
        "recent_posts": recent_posts,
    }
