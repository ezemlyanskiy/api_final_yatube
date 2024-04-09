from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    mixins,
    pagination,
    permissions,
    status,
    viewsets,
)
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post
from .mixins import ActionPermissionsMixin
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

User = get_user_model()


class PostViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination
    max_limit = settings.MAX_LIMIT


class CommentViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post=get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        following_username = request.data.get('following')

        if following_username == request.user.username:
            return Response(
                data=settings.CANT_FOLLOW_YOURSELF,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(
            user=request.user,
            following__username=following_username,
        ).exists():
            return Response(
                data=settings.ALREADY_FOLLOW,
                status=status.HTTP_400_BAD_REQUEST,
            )

        following = get_object_or_404(User, username=following_username)
        Follow.objects.create(user=request.user, following=following)

        return Response(
            data={
                'user': request.user.username,
                'following': following_username,
            },
            status=status.HTTP_201_CREATED,
        )
