import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post
from .utils import get_common_slug


class AuthorFieldSerializer(serializers.Serializer):
    author = get_common_slug()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(AuthorFieldSerializer, serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'pub_date')


class CommentSerializer(AuthorFieldSerializer, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'post', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = get_common_slug()
    following = get_common_slug(read_only=False)

    class Meta:
        model = Follow
        fields = ('user', 'following')
