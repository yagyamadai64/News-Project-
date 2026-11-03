from django.contrib.auth.models import Group, User
from rest_framework import serializers
from news_app.models import Category, Tag, NewsLetters, Contact, Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {"email": {"required": True}, "first_name": {"required": True}}
        fields = [
            "id",
            "username",
            "email",
            "groups",
            "first_name",
            "is_active",
            "is_superuser",
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class NewsLettersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsLetters
        fields = "__all__"


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "image",
            "author",
            "status",
            "view_count",
            "published_at",
            "category",
            "tag",
        ]
        extra_kwargs = {
            "author": {"read_only": True},
            "published_at": {"read_only": True},
            "view_count": {"read_only": True},
        }

    def validate(self, data):
        data["author"] = self.context["request"].user
        return data


class PostPublishSerializer(serializers.Serializer):
    post = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
