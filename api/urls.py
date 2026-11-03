from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"newsletters", views.NewsLettersViewSet)
router.register(r"contact", views.ContactViewSet)
router.register(r"post", views.PostViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("post-publish/", views.PostPublishViewSet.as_view(), name="post-publish-api"),
    path("draft-list/", views.DraftListViewSet.as_view(), name="draft-list-api"),
    path(
        "draft/<int:id>/", views.DraftDetailViewSet.as_view(), name="draft-details-api"
    ),
    path(
        "post-by-category/<int:category_id>/",
        views.PostListByCategory.as_view(),
        name="post-list-by-category-api",
    ),
    path(
        "post-by-tag/<int:tag_id>/",
        views.PostListByTag.as_view(),
        name="post-list-by-tag-api",
    ),
    # postcomment
    path(
        "post/<int:post_id>/comments/",
        views.CommentViewSet.as_view(),
        name="post-comment-api",
    ),
    # update delete
    path(
        "post/comments/<int:comment_id>/",
        views.CommentViewSet.as_view(),
        name="post-comment-change-api",
    ),
    path("api-admin/", include("rest_framework.urls", namespace="rest_framework")),
]
