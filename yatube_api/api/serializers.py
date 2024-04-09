from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from posts.models import Comment, Follow, Group, Post
from .fields import Base64ImageField

User = get_user_model()


class AuthorFieldSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )


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
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        followee = get_object_or_404(User, pk=value.pk)
        follower_username = self.context.get('request').user.username

        if followee.username == follower_username:
            raise serializers.ValidationError(
                settings.CANT_FOLLOW_YOURSELF,
                status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(
            user__username=follower_username,
            following__username=followee.username,
        ).exists():
            raise serializers.ValidationError(
                settings.ALREADY_FOLLOW,
                status.HTTP_400_BAD_REQUEST,
            )

        return value
