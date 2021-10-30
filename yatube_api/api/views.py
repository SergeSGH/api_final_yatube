from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post, User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .permissions import IsOwner, OwnerOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer, FollowSerializer)

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import LimitOffsetPagination


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, id=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('following',)

    def get_queryset(self):
        user = self.request.user
        queryset = user.following.all()
        return queryset

    def perform_create(self, serializer):
        print(self.request.data)
        following_username = self.request.data['following']
        following = get_object_or_404(User, username=following_username)
        if self.request.user == following:
            return Response(
                'Подписатья на себя нельзя!',
                status=status.HTTP_200_OK
            )
        if not Follow.objects.filter(
            user=self.request.user
        ).filter(following=following).exists():
            serializer.save(user=self.request.user, following=following)
