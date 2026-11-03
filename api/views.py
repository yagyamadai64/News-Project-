from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import permissions, viewsets, exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.serializers import (
    GroupSerializer,
    UserSerializer,
    TagSerializer,
    CategorySerializer,
    NewsLettersSerializer,
    ContactSerializer,
    PostSerializer,
    PostPublishSerializer,
    CommentSerializer,
)
from news_app.models import Category, Tag, NewsLetters, Contact, Post, Comment


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # get(list),getbyid(retrieve),post(create),put(update),patch(patical_update),delete(destory)
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()


# category,newsletter
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()


class NewsLettersViewSet(viewsets.ModelViewSet):
    queryset = NewsLetters.objects.all()
    serializer_class = NewsLettersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.filter(status="active", published_at__isnull=False)
        return queryset

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()


class PostPublishViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostPublishSerializer

    def post(self, req, *args, **kwargs):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            post = get_object_or_404(Post, id=data["post"])
            post.published_at = timezone.now()
            post.status = "active"
            post.save()
            serializer_data = PostSerializer(post).data
            return Response(serializer_data, status=status.HTTP_200_OK)


class DraftListViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published_at__isnull=True)
        return queryset


class DraftDetailViewSet(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published_at__isnull=True)
        return queryset


class PostListByCategory(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            published_at__isnull=False,
            status="active",
            category=self.kwargs["category_id"],
        )
        return queryset


class PostListByTag(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            published_at__isnull=False,
            status="active",
            tag=self.kwargs["tag_id"],
        )
        return queryset


class CommentViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, req, post_id, *args, **kwargs):
        comments = Comment.objects.filter(post_id=post_id)
        if not comments.exists():
            return Response(
                {"message": "No comments found for this post."},
                status=status.HTTP_200_OK,
            )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, post_id, *args, **kwargs):
        payload = req.data.copy()
        payload["post"] = post_id
        serializer = CommentSerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response(
                {"message": "Comment deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, req, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            serializer = CommentSerializer(comment, data=req.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Comment Update successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )
