from django.urls import path
from blog_app import views

app_name = "news_admin"
urlpatterns = [
    # path("", views.post_list, name="post_list"),
    path("", views.Postlist.as_view(), name="post_list"),
    # path("post-create/", views.post_create, name="post_create"),
    path("post-create/", views.PostCreate.as_view(), name="post_create"),
    # path("post-detail/<int:id>/", views.post_detail, name="post_detail"),
    path("post-detail/<int:id>/", views.PostDetails.as_view(), name="post_detail"),
    # path("post-delete/<int:id>/", views.post_delete, name="post_delete"),
    path("post-delete/<int:id>/", views.PostDelete.as_view(), name="post_delete"),
    # path("draft/", views.draft_list, name="draft_list"),
    path("draft/", views.Draftlist.as_view(), name="draft_list"),
    # path("draft-detail/<int:id>/", views.draft_detail, name="draft_detail"),
    path("draft-detail/<int:id>/", views.DraftDetails.as_view(), name="draft_detail"),
    # path("draft-publish/<int:id>/", views.draft_published, name="draft_published"),
    path(
        "draft-publish/<int:id>/",
        views.DraftPublished.as_view(),
        name="draft_published",
    ),
    # path("post-publish/<int:id>/", views.post_unpublished, name="post_unpublished"),
    path(
        "post-publish/<int:id>/",
        views.PostUnpublished.as_view(),
        name="post_unpublished",
    ),
    # path("post-update/<int:id>/", views.post_update, name="post_update"),
    path("post-update/<int:id>/", views.PostUpdate.as_view(), name="post_update"),
    # path("register/", views.register, name="userregister"),
    path("register/", views.RegisterView.as_view(), name="userregister"),
]
