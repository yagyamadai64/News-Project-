from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(TimeStampModel):
    name = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    status_choices = [
        ("active", "Active"),
        ("in_active", "In-Active"),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=status_choices, default="in_active"
    )
    view_count = models.PositiveBigIntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UserProfile(TimeStampModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="userprofile/%Y/%m/%d", blank=False)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Comment(TimeStampModel):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class NewsLetters(TimeStampModel):
    email = models.EmailField()

    def __str__(self):
        return self.email
