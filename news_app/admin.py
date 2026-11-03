from django.contrib import admin
from news_app.models import (
    Post,
    Category,
    Tag,
    Contact,
    UserProfile,
    Comment,
    NewsLetters,
)

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(NewsLetters)
