from django.shortcuts import get_object_or_404

from posts.models import Post
from .permissions import IsAuthorOrReadOnly


class ActionPermissionsMixin:
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs.get('post_id')),
        ) if 'post_id' in self.kwargs else serializer.save(
            author=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
